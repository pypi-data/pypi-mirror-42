import datetime
# import logging
import pprint

import ee
import pytest

import openet.ndvi as ndvi_et
import openet.ndvi.utils as utils
# TODO: import utils from openet.core
# import openet.core.utils as utils


COLL_ID = 'LANDSAT/LC08/C01/T1_TOA/'
SCENE_ID = 'LC08_044033_20170716'
SCENE_DT = datetime.datetime.strptime(SCENE_ID[-8:], '%Y%m%d')
SCENE_DATE = SCENE_DT.strftime('%Y-%m-%d')
SCENE_DOY = int(SCENE_DT.strftime('%j'))
SCENE_TIME = utils.millis(SCENE_DT)
# SCENE_TIME = utils.getinfo(ee.Date(SCENE_DATE).millis())


# Should these be test fixtures instead?
# I'm not sure how to make them fixtures and allow input parameters
def toa_image(red=0.1, nir=0.9, bt=305):
    """Construct a fake Landsat 8 TOA image with renamed bands"""
    return ee.Image.constant([red, nir, bt]) \
        .rename(['red', 'nir', 'lst']) \
        .set({
            'system:time_start': ee.Date(SCENE_DATE).millis(),
            'k1_constant': ee.Number(607.76),
            'k2_constant': ee.Number(1260.56)})


def default_image(ndvi=0.8):
    # First construct a fake 'prepped' input image
    return ee.Image.constant([ndvi]).rename(['ndvi']) \
        .set({
            'system:index': SCENE_ID,
            'system:time_start': ee.Date(SCENE_DATE).millis(),
            'system:id': COLL_ID + SCENE_ID,
    })


def test_ee_init():
    """Check that Earth Engine was initialized"""
    assert ee.Number(1).getInfo() == 1


def test_Image_default_parameters():
    n = ndvi_et.Image(default_image())
    assert n.m == 1.25
    assert n.b == 0.0
    assert n.etr_source == 'IDAHO_EPSCOR/GRIDMET'
    assert n.etr_band == 'etr'


def test_Image_calculated_properties():
    n = ndvi_et.Image(default_image())
    assert utils.getinfo(n._time_start) == SCENE_TIME
    assert utils.getinfo(n._index) == SCENE_ID


def test_Image_date_properties():
    n = ndvi_et.Image(default_image())
    assert utils.getinfo(n._date)['value'] == SCENE_TIME
    # assert utils.getinfo(n._year) == int(SCENE_DATE.split('-')[0])
    # assert utils.getinfo(n._month) == int(SCENE_DATE.split('-')[1])
    assert utils.getinfo(n._start_date)['value'] == SCENE_TIME
    assert utils.getinfo(n._end_date)['value'] == utils.millis(
        SCENE_DT + datetime.timedelta(days=1))
    # assert utils.getinfo(n._doy) == SCENE_DOY


# Test the static methods of the class first
# Do these need to be inside the TestClass?
@pytest.mark.parametrize(
    'red, nir, expected',
    [
        [0.2, 9.0 / 55, -0.1],
        [0.2, 0.2,  0.0],
        [0.1, 11.0 / 90,  0.1],
        [0.2, 0.3, 0.2],
        [0.1, 13.0 / 70, 0.3],
        [0.3, 0.7, 0.4],
        [0.2, 0.6, 0.5],
        [0.2, 0.8, 0.6],
        [0.1, 17.0 / 30, 0.7],
        [0.1, 0.9, 0.8],
    ]
)
def test_Image_static_ndvi_calculation(red, nir, expected, tol=0.000001):
    output = utils.constant_image_value(
        ndvi_et.Image._ndvi(toa_image(red=red, nir=nir)))
    assert abs(output['ndvi'] - expected) <= tol


def test_Image_static_ndvi_band_name():
    output = utils.getinfo(ndvi_et.Image._ndvi(toa_image()))
    assert output['bands'][0]['id'] == 'ndvi'


def test_Image_ndvi_band_name():
    output = utils.getinfo(ndvi_et.Image(default_image()).ndvi)
    assert output['bands'][0]['id'] == 'ndvi'


def test_Image_ndvi_properties():
    """Test if properties are set on the ndvi image"""
    output = utils.getinfo(ndvi_et.Image(default_image()).ndvi)['properties']
    assert output['system:index'] == SCENE_ID
    assert output['system:time_start'] == SCENE_TIME
    assert output['IMAGE_ID'] == COLL_ID + SCENE_ID


def test_Image_time_values():
    output = utils.constant_image_value(ndvi_et.Image(default_image()).time)
    assert output['time'] == SCENE_TIME


def test_Image_time_band_name():
    output = utils.getinfo(ndvi_et.Image(default_image()).time)
    assert output['bands'][0]['id'] == 'time'


def test_Image_time_properties():
    """Test if properties are set on the time image"""
    output = utils.getinfo(ndvi_et.Image(default_image()).time)['properties']
    assert output['system:index'] == SCENE_ID
    assert output['system:time_start'] == SCENE_TIME
    assert output['IMAGE_ID'] == COLL_ID + SCENE_ID


@pytest.mark.parametrize(
    'ndvi, m, b, expected',
    [
        [0.8, 1.25, 0, 1.0],
        [0.8, 1.0, 0, 0.8],
        [0.8, 1.0, 0.2, 1.0],
        [0.0, 1.25, 0, 0.0],
    ]
)
def test_Image_etf(ndvi, m, b, expected, tol=0.0001):
    input_args = {'image': default_image(ndvi=ndvi)}
    input_args['m'] = m
    input_args['b'] = b
    output_img = ndvi_et.Image(**input_args).etf
    output = utils.constant_image_value(output_img)
    assert abs(output['etf'] - expected) <= tol


def test_Image_etf_defaults(ndvi=0.8, expected=1.0, tol=0.0001):
    output_img = ndvi_et.Image(**{'image': default_image(ndvi=ndvi)}).etf
    output = utils.constant_image_value(output_img)
    assert abs(output['etf'] - expected) <= tol


def test_Image_etf_band_name():
    output = utils.getinfo(ndvi_et.Image(default_image()).etf)
    assert output['bands'][0]['id'] == 'etf'


def test_Image_etf_properties():
    """Test if properties are set on the ETf image"""
    output = utils.getinfo(ndvi_et.Image(default_image()).etf)['properties']
    assert output['system:index'] == SCENE_ID
    assert output['system:time_start'] == SCENE_TIME
    assert output['IMAGE_ID'] == COLL_ID + SCENE_ID


def test_Image_etr_constant(etr=10.0, expected=10.0, tol=0.0001):
    input_args = {'image': default_image(), 'etr_source': etr}
    output_img = ndvi_et.Image(**input_args).etr
    output = utils.constant_image_value(output_img)
    assert abs(output['etr'] - expected) <= tol


def test_Image_etr_band_name():
    output = utils.getinfo(ndvi_et.Image(**{'image': default_image()}).etr)
    assert output['bands'][0]['id'] == 'etr'


def test_Image_etr_properties():
    """Test if properties are set on the ETr image"""
    output = utils.getinfo(ndvi_et.Image(default_image()).etr)
    assert output['properties']['system:index'] == SCENE_ID
    assert output['properties']['system:time_start'] == SCENE_TIME
    assert output['properties']['IMAGE_ID'] == COLL_ID + SCENE_ID


def test_Image_et_constant(etr=10, expected=10, tol=0.0001):
    input_args = {'image': default_image(), 'etr_source': etr}
    output_img = ndvi_et.Image(**input_args).et
    output = utils.constant_image_value(ee.Image(output_img))
    assert abs(output['et'] - expected) <= tol


def test_Image_et_band_name():
    output = utils.getinfo(ndvi_et.Image(default_image()).et)
    assert output['bands'][0]['id'] == 'et'


def test_Image_et_properties():
    """Test if properties are set on the ET image"""
    output = utils.getinfo(ndvi_et.Image(default_image()).et)
    assert output['properties']['system:index'] == SCENE_ID
    assert output['properties']['system:time_start'] == SCENE_TIME
    assert output['properties']['IMAGE_ID'] == COLL_ID + SCENE_ID


def test_Image_calculate_variables_default():
    output = utils.getinfo(ndvi_et.Image(default_image()).calculate())
    assert set([x['id'] for x in output['bands']]) == set(['et', 'etr', 'etf'])


def test_Image_calculate_variables_custom():
    variables = set(['ndvi'])
    output = utils.getinfo(ndvi_et.Image(default_image()).calculate(variables))
    assert set([x['id'] for x in output['bands']]) == variables


def test_Image_calculate_variables_all():
    variables = set(['ndvi', 'et', 'etr', 'etf', 'time'])
    output = utils.getinfo(
        ndvi_et.Image(default_image()).calculate(variables=list(variables)))
    assert set([x['id'] for x in output['bands']]) == variables


# How should these @classmethods be tested?
def test_Image_from_landsat_c1_toa_default_image():
    """Test that the classmethod is returning a class object"""
    output = ndvi_et.Image.from_landsat_c1_toa(toa_image())
    assert type(output) == type(ndvi_et.Image(default_image()))


@pytest.mark.parametrize(
    'image_id',
    [
        'LANDSAT/LC08/C01/T1_RT_TOA/LC08_044033_20170716',
        'LANDSAT/LC08/C01/T1_TOA/LC08_044033_20170716',
        'LANDSAT/LE07/C01/T1_RT_TOA/LE07_044033_20170708',
        'LANDSAT/LE07/C01/T1_TOA/LE07_044033_20170708',
        'LANDSAT/LT05/C01/T1_TOA/LT05_044033_20110716',
        'LANDSAT/LT04/C01/T1_TOA/LT04_044033_19830812',
    ]
)
def test_Image_from_landsat_c1_toa_image_id(image_id):
    """Test instantiating the class from a Landsat image ID"""
    output = utils.getinfo(ndvi_et.Image.from_landsat_c1_toa(image_id).ndvi)
    assert output['properties']['system:index'] == image_id.split('/')[-1]


def test_Image_from_landsat_c1_toa_image():
    """Test instantiating the class from a Landsat ee.Image"""
    image_id = 'LANDSAT/LC08/C01/T1_TOA/LC08_044033_20170716'
    output = utils.getinfo(ndvi_et.Image.from_landsat_c1_toa(ee.Image(image_id)).ndvi)
    assert output['properties']['system:index'] == image_id.split('/')[-1]


def test_Image_from_landsat_c1_toa_etf():
    """Test if ETf can be built for a Landsat images"""
    image_id = 'LANDSAT/LC08/C01/T1_TOA/LC08_044033_20170716'
    output = utils.getinfo(ndvi_et.Image.from_landsat_c1_toa(image_id).etf)
    assert output['properties']['system:index'] == image_id.split('/')[-1]


def test_Image_from_landsat_c1_toa_et():
    """Test if ET can be built for a Landsat images"""
    image_id = 'LANDSAT/LC08/C01/T1_TOA/LC08_044033_20170716'
    output = utils.getinfo(ndvi_et.Image.from_landsat_c1_toa(image_id).et)
    assert output['properties']['system:index'] == image_id.split('/')[-1]


def test_Image_from_landsat_c1_toa_exception():
    """Test instantiating the class for an invalid image ID"""
    with pytest.raises(Exception):
        utils.getinfo(ndvi_et.Image.from_landsat_c1_toa(ee.Image('FOO')).index)


def test_Image_from_landsat_c1_sr_default_image():
    """Test that the classmethod is returning a class object"""
    output = ndvi_et.Image.from_landsat_c1_sr(toa_image())
    assert type(output) == type(ndvi_et.Image(default_image()))


@pytest.mark.parametrize(
    'image_id',
    [
        # 'LANDSAT/LC08/C01/T1_RT_SR/LC08_044033_20170716',
        'LANDSAT/LC08/C01/T1_SR/LC08_044033_20170716',
        # 'LANDSAT/LE07/C01/T1_RT_SR/LE07_044033_20170708',
        'LANDSAT/LE07/C01/T1_SR/LE07_044033_20170708',
        'LANDSAT/LT05/C01/T1_SR/LT05_044033_20110716',
        'LANDSAT/LT04/C01/T1_SR/LT04_044033_19830812',
    ]
)
def test_Image_from_landsat_c1_sr_image_id(image_id):
    """Test instantiating the class from a Landsat image ID"""
    output = utils.getinfo(ndvi_et.Image.from_landsat_c1_sr(image_id).ndvi)
    assert output['properties']['system:index'] == image_id.split('/')[-1]


def test_Image_from_landsat_c1_sr_image():
    """Test instantiating the class from a Landsat ee.Image"""
    image_id = 'LANDSAT/LC08/C01/T1_SR/LC08_044033_20170716'
    output = utils.getinfo(
        ndvi_et.Image.from_landsat_c1_sr(ee.Image(image_id)).ndvi)
    assert output['properties']['system:index'] == image_id.split('/')[-1]


def test_Image_from_landsat_c1_sr_etf():
    """Test if ETf can be built for a Landsat images"""
    image_id = 'LANDSAT/LC08/C01/T1_SR/LC08_044033_20170716'
    output = utils.getinfo(ndvi_et.Image.from_landsat_c1_sr(image_id).etf)
    assert output['properties']['system:index'] == image_id.split('/')[-1]


def test_Image_from_landsat_c1_sr_et():
    """Test if ET can be built for a Landsat images"""
    image_id = 'LANDSAT/LC08/C01/T1_SR/LC08_044033_20170716'
    output = utils.getinfo(ndvi_et.Image.from_landsat_c1_sr(image_id).et)
    assert output['properties']['system:index'] == image_id.split('/')[-1]


def test_Image_from_landsat_c1_sr_exception():
    """Test instantiating the class for an invalid image ID"""
    with pytest.raises(Exception):
        utils.getinfo(ndvi_et.Image.from_landsat_c1_sr(ee.Image('FOO')).ndvi)


def test_Image_from_sentinel2_toa_default_image():
    """Test that the classmethod is returning a class object"""
    output = ndvi_et.Image.from_sentinel2_toa(toa_image())
    assert type(output) == type(ndvi_et.Image(default_image()))


@pytest.mark.parametrize(
    'image_id',
    [
        'COPERNICUS/S2/20170510T184921_20170510T185915_T10SFJ',
    ]
)
def test_Image_from_sentinel2_toa_sentinel_image(image_id):
    """Test instantiating the class from real Sentinel 2 images"""
    output = utils.getinfo(
        ndvi_et.Image.from_sentinel2_toa(ee.Image(image_id)).ndvi)
    assert output['properties']['system:index'] == image_id.split('/')[-1]


def test_Image_from_sentinel2_toa_exception():
    """Test instantiating the class for an invalid image ID"""
    with pytest.raises(Exception):
        utils.getinfo(
            ndvi_et.Image.from_sentinel2_toa(ee.Image('DEADBEEF')).index)


@pytest.mark.parametrize(
    'image_id',
    [
        'LANDSAT/LC08/C01/T1_TOA/LC08_044033_20170716',
        'LANDSAT/LC08/C01/T1_SR/LC08_044033_20170716',
        'COPERNICUS/S2/20170510T184921_20170510T185915_T10SFJ',
    ]
)
def test_Image_from_image_id(image_id):
    """Test instantiating the class using the from_image_id method"""
    output = utils.getinfo(ndvi_et.Image.from_image_id(image_id).ndvi)
    assert output['properties']['system:index'] == image_id.split('/')[-1]
    assert output['properties']['IMAGE_ID'] == image_id


def test_Image_from_method_kwargs():
    """Test that the init parameters can be passed through the helper methods"""
    assert ndvi_et.Image.from_landsat_c1_toa(
        'LANDSAT/LC08/C01/T1_TOA/LC08_042035_20150713', m=0.5).m == 0.5
    assert ndvi_et.Image.from_landsat_c1_sr(
        'LANDSAT/LC08/C01/T1_SR/LC08_042035_20150713', m=0.5).m == 0.5
    assert ndvi_et.Image.from_sentinel2_toa(
        'COPERNICUS/S2/20170510T184921_20170510T185915_T10SFJ', m=0.5).m == 0.5
