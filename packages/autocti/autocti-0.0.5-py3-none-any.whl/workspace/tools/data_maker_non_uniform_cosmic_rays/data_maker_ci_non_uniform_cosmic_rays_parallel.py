from autocti.data import util
from autocti.charge_injection import ci_frame
from autocti.charge_injection import ci_pattern
from autocti.charge_injection import ci_data

from autocti.model import arctic_settings
from autocti.model import arctic_params

from workspace_jam.scripts.cosmic_rays import cosmics

import logging
logger = logging.getLogger(__name__)

import os

# This tool allows one to make simulated charge injection imaging data-sets for calibrating parallel charge transfer
# inefficiency, which can be used to test example pipelines and investigate CTI modeling on data-sets where the
# 'true' answer is known.

# The 'image_type' and 'model_type' determine the directory the output data folder, e.g:

# The image will be output as '/workspace/data/image_type/model_type/ci_image.fits'.
# The noise-map will be output as '/workspace/data/image_type/model_type/ci_noise_map.fits'.
# The pre cti ci image will be output as '/workspace/data/image_type/model_type/ci_pre_cti.fits'.

ci_data_name = 'ci_x8_images_non_uniform'
ci_data_model = 'parallel_x1_species'

shape = (2316, 2119) # The shape determines the shape of the images simulated.

# Specify the charge injection regions on the CCD, which in this case is 7 equally spaced rectangular blocks.
ci_regions = [(0, 30, 51, shape[1]-20), (330, 360, 51, shape[1]-20),
              (660, 690, 51, shape[1]-20), (990, 1020, 51, shape[1]-20),
              (1320, 1350, 51, shape[1]-20), (1650, 1680, 51, shape[1]-20),
              (1980, 2010, 51, shape[1]-20)]

# The normalization of every ci image - this size of this list thus determines how many images are simulated.
normalizations=[100.0, 500.0, 1000.0, 5000.0, 10000.0, 25000.0, 50000.0, 84700.0]

# The frame geometry of the image being simuated.
frame_geometry = ci_frame.QuadGeometryEuclid.bottom_left()
# frame_geometry = ci_frame.QuadGeometryEuclid.bottom_right()
# frame_geometry = ci_frame.QuadGeometryEuclid.top_left()
# frame_geometry = ci_frame.QuadGeometryEuclid.top_right()

# The CTI settings of arCTIc, which models the CCD read-out including CTI. For parallel ci data, we include 'charge
# injection mode' which accounts for the fact that every pixel is transferred over the full CCD.
parallel_cti_settings = arctic_settings.Settings(well_depth=84700, niter=1, express=2, n_levels=2000,
                                        charge_injection_mode=True, readout_offset=0)
cti_settings = arctic_settings.ArcticSettings(parallel=parallel_cti_settings)

# The CTI model parameters of arCTIc, which includes each trap species density / lifetime and the CCD properties for
# parallel charge transfer.
parallel_species = arctic_params.Species(trap_density=0.5, trap_lifetime=4.0)
parallel_ccd = arctic_params.CCD(well_notch_depth=1.0e-4, well_fill_beta=0.58, well_fill_gamma=0.0, well_fill_alpha=1.0)
cti_params = arctic_params.ArcticParams(parallel_species=[parallel_species], parallel_ccd=parallel_ccd)

# This function creates uniform blocks of non-charge injection lines, given an input normalization, regions and
# parameters describing its non-uniform properties.
column_deviations = [100.0]*len(normalizations)
row_slopes = [0.0]*len(normalizations)
ci_patterns = ci_pattern.non_uniform_from_lists(normalizations=normalizations, regions=ci_regions,
                                                row_slopes=row_slopes)

# Use the simulate ci patterns to generate the pre-cti charge injection images.
ci_pre_ctis = list(map(lambda ci_pattern, column_deviation :
                       ci_pattern.simulate_ci_pre_cti(shape=shape, column_deviation=column_deviation,
                                                      maximum_normalization=cti_settings.parallel.well_depth),
                       ci_patterns, column_deviations))

# We use the LA Cosmic algorithm to simulate and add cosmic rays to our ci pre cti image. This routine randomly
# generates cosmimc rays based on realistic cosmic ray rates expected. These cosmic rays will then be added to our
# ci pre-cti image in the simulaate function below, and subject to CTI according to the CTI model.
cosmic_path = '{}/../../scripts/cosmic_rays/'.format(os.path.dirname(os.path.realpath(__file__)))

cosmic_ray_maker = cosmics.CosmicRays(shape=shape, cr_fluxscaling=1.0, cr_length_file=cosmic_path + 'crlength_v2.fits',
                                      cr_distance_file=cosmic_path + 'crdist.fits', log=logger)
cosmic_ray_maker.set_ifiles()
cosmic_ray_images = list(map(lambda i : cosmic_ray_maker.drawEventsToCoveringFactor(limit=cti_settings.parallel.well_depth),
                             range(len(normalizations))))

# Use every ci pattern to simulate a ci image.
ci_datas = list(map(lambda ci_pre_cti, ci_pattern, cosmic_ray_image :
                    ci_data.simulate(ci_pre_cti=ci_pre_cti, frame_geometry=frame_geometry,
                                     ci_pattern=ci_pattern, cti_settings=cti_settings, cti_params=cti_params,
                                     read_noise=4.0, cosmic_ray_image=cosmic_ray_image),
                    ci_pre_ctis, ci_patterns, cosmic_ray_images))

# Now, lets output this simulated ccd-data to the data folder. First, we'll get a relative path.
path = '{}/../'.format(os.path.dirname(os.path.realpath(__file__)))

# Check folders of the image type and model type exists in the data folder for the images to be output. If they don't,
# make them.

ci_data_path = path +'/data/' + ci_data_name

if not os.path.exists(ci_data_path):
    os.makedirs(ci_data_path)

ci_data_path = path +'/data/' + ci_data_name + '/' + ci_data_model

if not os.path.exists(ci_data_path):
    os.makedirs(ci_data_path)

# Now, output every image to the data folder as the filename 'ci_data_#.fits'
list(map(lambda ci_data, index:
         util.numpy_array_to_fits(array=ci_data.image,
                                  file_path=ci_data_path + '/ci_image_' + str(index) + '.fits', overwrite=True),
         ci_datas, range(len(ci_datas))))

# Output every pre-cti image to the data folder as the filename 'ci_pre_cti_#.fits'. This allows the calibration
# pipeline to load these images as the model pre-cti images, which is necessary for non-uniform ci patterns.
list(map(lambda ci_data, index :
         util.numpy_array_to_fits(array=ci_data.ci_pre_cti,
                                  file_path=ci_data_path + '/ci_pre_cti_' + str(index) + '.fits', overwrite=True),
         ci_datas, range(len(ci_datas))))

# The cosmic-ray image has zeros wherever no cosmic rays are simulated, and positive values wherever they do. Thus
# the cosmic ray mask is simply all values in the cosmic ray image which are positive.
cosmic_ray_masks = list(map(lambda mask : mask > 0.0, cosmic_ray_images))

list(map(lambda cosmic_ray_mask, index :
         util.numpy_array_to_fits(array=cosmic_ray_mask,
                                  file_path=ci_data_path + '/cosmic_ray_mask_' + str(index) + '.fits', overwrite=True),
         cosmic_ray_masks, range(len(ci_datas))))