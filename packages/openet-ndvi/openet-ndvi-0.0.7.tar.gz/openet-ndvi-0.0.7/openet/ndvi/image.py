import ee

from . import utils
import openet.core.common as common
# TODO: import utils from openet.core
# import openet.core.utils as utils


def lazy_property(fn):
    """Decorator that makes a property lazy-evaluated

    https://stevenloria.com/lazy-properties/
    """
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property


class Image():
    """GEE based model for computing ET fraction as a linear function of NDVI"""

    def __init__(
            self,
            image,
            m=1.25,
            b=0.0,
            etr_source='IDAHO_EPSCOR/GRIDMET',
            etr_band='etr',
            elevation='USGS/SRTMGL1_003',
            landcover='USGS/NLCD',
            ):
        """Construct a generic NDVI based ET Image

        Parameters
        ----------
        image : ee.Image
            Must have bands: 'ndvi'
            Must have properties: 'system:time_start', 'system:index', and
                                  'system:id'
        m : float, optional
            Slope of the NDVI to ET regression (the default is 1.25).
        b : float, optional
            Offset of the NDVI to ET regression (the default is 0.0).
        etr_source : str, float, optional
            Reference ET source (the default is 'IDAHO_EPSCOR/GRIDMET').
        etr_band : str, optional
            Reference ET band name (the default is 'etr').
        elevation : str, optional
            Elevation source (the default is '').  This
        landcover : str, optional
            Landcover source (the default is '').

        Notes
        -----
        ETf = m * NDVI + b
        ET = ETf * ETr

        """
        self.image = image

        # Set as "lazy_property" below in order to return custom properties
        # self.ndvi = self.image.select(['ndvi'])

        self.m = m
        self.b = b

        # CGM - Should the parsing and checking of the ETr source and band name
        #   happen here or in the etr function?
        self.etr_source = etr_source
        self.etr_band = etr_band

        # Get system properties from the input image
        self._id = self.image.get('system:id')
        self._index = self.image.get('system:index')
        self._time_start = self.image.get('system:time_start')
        self._properties = {
            'system:index': self._index,
            'system:time_start': self._time_start,
            'IMAGE_ID': self._id,
        }

        # Build date properties from the system:time_start
        self._date = ee.Date(self._time_start)
        self._start_date = ee.Date(utils.date_to_time_0utc(self._date))
        self._end_date = self._start_date.advance(1, 'day')

    def calculate(self, variables=['et', 'etr', 'etf']):
        """Return a multiband image of calculated variables

        Parameters
        ----------
        variables : list

        Returns
        -------
        ee.Image

        """
        output_images = []
        for v in variables:
            if v.lower() == 'et':
                output_images.append(self.et)
            elif v.lower() == 'etf':
                output_images.append(self.etf)
            elif v.lower() == 'etr':
                output_images.append(self.etr)
            elif v.lower() == 'ndvi':
                output_images.append(self.ndvi)
            # elif v.lower() == 'qa':
            #     output_images.append(self.qa)
            # elif v.lower() == 'quality':
            #     output_images.append(self.quality)
            elif v.lower() == 'time':
                output_images.append(self.time)
            else:
                raise ValueError('unsupported variable: {}'.format(v))

        return ee.Image(output_images).set(self._properties)

    @lazy_property
    def ndvi(self):
        """Return NDVI image"""
        return self.image.select(['ndvi']).set(self._properties)

    @lazy_property
    def time(self):
        """Return 0 UTC time image (in milliseconds)"""
        return self.etf \
            .double().multiply(0).add(utils.date_to_time_0utc(self._date)) \
            .rename(['time']).set(self._properties)
        # return ee.Image.constant(utils.date_to_time_0utc(self._date)) \
        #     .double().rename(['time']).set(self._properties)

    @lazy_property
    def etf(self):
        """Compute fraction of reference ET from NDVI"""
        return self.ndvi.multiply(self.m).add(self.b) \
            .rename(['etf']).set(self._properties)

    @lazy_property
    def etr(self):
        """Compute reference ET for the image date"""
        if utils.is_number(self.etr_source):
            # Interpret numbers as constant images
            # CGM - Should we use the ee_types here instead?
            #   i.e. ee.ee_types.isNumber(self.etr_source)
            etr_img = ee.Image.constant(self.etr_source)
        elif type(self.etr_source) is str:
            # Assume a string source is an image collection ID (not an image ID)
            etr_img = ee.Image(
                ee.ImageCollection(self.etr_source) \
                    .filterDate(self._start_date, self._end_date) \
                    .select([self.etr_band]) \
                    .first())
        # elif type(self.etr_source) is list:
        #     # Interpret as list of image collection IDs to composite/mosaic
        #     #   i.e. Spatial CIMIS and GRIDMET
        #     # CGM - Need to check the order of the collections
        #     etr_coll = ee.ImageCollection([])
        #     for coll_id in self.etr_source:
        #         coll = ee.ImageCollection(coll_id) \
        #             .select([self.etr_band]) \
        #             .filterDate(self._start_date, self._end_date)
        #         etr_img = etr_coll.merge(coll)
        #     etr_img = etr_coll.mosaic()
        # elif isinstance(self.etr_source, computedobject.ComputedObject):
        #     # Interpret computed objects as image collections
        #     etr_coll = ee.ImageCollection(self.etr_source) \
        #         .select([self.etr_band]) \
        #         .filterDate(self._start_date, self._end_date)
        else:
            raise ValueError('unsupported etr_source: {}'.format(
                self.etr_source))

        # Map ETr values directly to the input (i.e. Landsat) image pixels
        # The benefit of this is the ETr image is now in the same crs as the
        #   input image.  Not all models may want this though.
        # CGM - Should the output band name match the input ETr band name?
        return self.ndvi.multiply(0).add(etr_img) \
            .rename(['etr']).set(self._properties)

    @lazy_property
    def et(self):
        """Compute actual ET as fraction of reference times reference"""
        return self.etf.multiply(self.etr) \
            .rename(['et']).set(self._properties)

    # @lazy_property
    # def quality(self):
    #     """Set quality to 1 for all active pixels (for now)"""
    #     return self.etf.multiply(0).add(1) \
    #         .rename(['quality']).set(self._properties)

    @classmethod
    def from_image_id(cls, image_id, **kwargs):
        """Constructs an NDVI-ET Image instance from an image ID

        Parameters
        ----------
        image_id : str
            An earth engine image ID.
            (i.e. 'LANDSAT/LC08/C01/T1_SR/LC08_044033_20170716')
        kwargs
            Keyword arguments to pass through to model init.

        Returns
        -------
        new instance of Image class

        """
        # DEADBEEF - Should the supported image collection IDs and helper
        # function mappings be set in a property or method of the Image class?
        collection_methods = {
            'LANDSAT/LC08/C01/T1_RT_TOA': 'from_landsat_c1_toa',
            'LANDSAT/LE07/C01/T1_RT_TOA': 'from_landsat_c1_toa',
            'LANDSAT/LC08/C01/T1_TOA': 'from_landsat_c1_toa',
            'LANDSAT/LE07/C01/T1_TOA': 'from_landsat_c1_toa',
            'LANDSAT/LT05/C01/T1_TOA': 'from_landsat_c1_toa',
            'LANDSAT/LT04/C01/T1_TOA': 'from_landsat_c1_toa',
            'LANDSAT/LC08/C01/T1_SR': 'from_landsat_c1_sr',
            'LANDSAT/LE07/C01/T1_SR': 'from_landsat_c1_sr',
            'LANDSAT/LT05/C01/T1_SR': 'from_landsat_c1_sr',
            'LANDSAT/LT04/C01/T1_SR': 'from_landsat_c1_sr',
            'COPERNICUS/S2': 'from_sentinel2_toa',
        }

        try:
            method_name = collection_methods[image_id.rsplit('/', 1)[0]]
        except KeyError:
            raise ValueError('unsupported collection ID: {}'.format(image_id))
        except Exception as e:
            raise Exception('unhandled exception: {}'.format(e))

        method = getattr(Image, method_name)

        return method(ee.Image(image_id), **kwargs)

    @classmethod
    def from_landsat_c1_toa(cls, toa_image, **kwargs):
        """Constructs an NDVI-ET Image instance from a Landsat TOA image

        Parameters
        ----------
        toa_image : ee.Image, str
            A raw Landsat Collection 1 TOA image or image ID.
        kwargs : dict
            Keyword arguments to pass through to model init.

        Returns
        -------
        new instance of Image class

        """
        if type(toa_image) is str:
            toa_image = ee.Image(toa_image)

        # Use the SPACECRAFT_ID property identify each Landsat type
        spacecraft_id = ee.String(toa_image.get('SPACECRAFT_ID'))

        # Rename bands to generic names
        input_bands = ee.Dictionary({
            'LANDSAT_4': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B6', 'BQA'],
            'LANDSAT_5': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B6', 'BQA'],
            'LANDSAT_7': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B6_VCID_1', 'BQA'],
            'LANDSAT_8': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'BQA'],
        })
        output_bands = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'lst',
                        'BQA']
        prep_image = toa_image.select(input_bands.get(spacecraft_id),
                                      output_bands)

        # Build the input image
        # Eventually send the BQA band or a cloud mask through also
        input_image = ee.Image([
            cls._ndvi(prep_image)
        ])

        # Apply the cloud mask and add properties
        input_image = input_image \
            .updateMask(common.landsat_c1_toa_cloud_mask(toa_image)) \
            .set({
                'system:index': toa_image.get('system:index'),
                'system:time_start': toa_image.get('system:time_start'),
                'system:id': toa_image.get('system:id'),
            })

        # Instantiate the class
        return cls(input_image, **kwargs)

    @classmethod
    def from_landsat_c1_sr(cls, sr_image, **kwargs):
        """Constructs an NDVI-ET Image instance from a Landsat SR image

        Parameters
        ----------
        sr_image : ee.Image, str
            A raw Landsat Collection 1 SR image or image ID.
        kwargs : dict
            Keyword arguments to pass through to model init.

        Returns
        -------
        new instance of Image class

        """
        sr_image = ee.Image(sr_image)

        # Use the SATELLITE property identify each Landsat type
        spacecraft_id = ee.String(sr_image.get('SATELLITE'))

        # Rename bands to generic names
        input_bands = ee.Dictionary({
            'LANDSAT_4': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B6', 'pixel_qa'],
            'LANDSAT_5': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B6', 'pixel_qa'],
            'LANDSAT_7': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B6', 'pixel_qa'],
            'LANDSAT_8': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'pixel_qa'],
        })
        output_bands = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'lst',
                        'pixel_qa']
        prep_image = sr_image.select(input_bands.get(spacecraft_id),
                                     output_bands)

        # Build the input image
        # Eventually send the BQA band or a cloud mask through also
        input_image = ee.Image([
            cls._ndvi(prep_image)
        ])

        # Apply the cloud mask and add properties
        input_image = input_image \
            .updateMask(common.landsat_c1_sr_cloud_mask(sr_image)) \
            .set({
                'system:index': sr_image.get('system:index'),
                'system:time_start': sr_image.get('system:time_start'),
                'system:id': sr_image.get('system:id'),
            })

        # Instantiate the class
        return cls(input_image, **kwargs)

    @classmethod
    def from_sentinel2_toa(cls, toa_image, **kwargs):
        """Constructs an NDVI-ET Image instance from a Sentinel 2 TOA image

        Parameters
        ----------
        toa_image : ee.Image, str
            A raw Sentinel 2 TOA image or image ID.
        kwargs : dict
            Keyword arguments to pass through to model init.

        Returns
        -------
        new instance of Image class

        """
        toa_image = ee.Image(toa_image)

        # Don't distinguish between Sentinel-2 A and B for now
        # Rename bands to generic names
        # Scale bands to 0-1 (from 0-10000)
        input_bands = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12', 'QA60']
        output_bands = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'QA60']
        prep_image = toa_image \
            .select(input_bands, output_bands) \
            .divide(10000.0)

        # Build the input image
        # Eventually send the BQA band or a cloud mask through also
        input_image = ee.Image([
            cls._ndvi(prep_image)
        ])

        # Apply the cloud mask and add properties
        input_image = input_image \
            .updateMask(common.sentinel2_toa_cloud_mask(toa_image)) \
            .set({
                'system:index': toa_image.get('system:index'),
                'system:time_start': toa_image.get('system:time_start'),
                'system:id': toa_image.get('system:id'),
            })

        # Instantiate the class
        return cls(input_image, **kwargs)

    @staticmethod
    def _ndvi(toa_image):
        """Compute NDVI

        Parameters
        ----------
        toa_image : ee.Image
            Renamed TOA image with 'nir' and 'red bands.

        Returns
        -------
        ee.Image

        """
        return toa_image.normalizedDifference(['nir', 'red']) \
            .rename(['ndvi'])
