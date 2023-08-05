from autofit import conf
from autolens.data import ccd
from autolens.data.array import mask as msk
from autolens.data.plotters import ccd_plotters

import os

path = '{}/../'.format(os.path.dirname(os.path.realpath(__file__)))
conf.instance = conf.Config(config_path=path+'config', output_path=path+'output')

# lens_name = 'slacs0216-0813' # Incorrect
lens_name = 'slacs0252+0039' # Works
lens_name = 'slacs0737+3216' # Works
lens_name = 'slacs0912+0029' # Works
lens_name = 'slacs0959+4410' # Bad fit phase 5 due to source demag thing
lens_name = 'slacs0959+4416' # Bad Fit because its the hard to fit lens
# lens_name = 'slacs1011+0143' # x2 lenses
# lens_name = 'slacs1205+4910' # Bad fit because foreground galaxy is fitted
# lens_name = 'slacs1250+0523' # Bad fit due to poor parametric source.
# lens_name = 'slacs1402+6321' # Bad fit and i cant even see the source :/
# lens_name = 'slacs1420+6019' # Bad fit phase 5 due to complex source.
# lens_name = 'slacs1430+4105' # Works
# lens_name = 'slacs1627+0053' # Works, but weird low res source
# lens_name = 'slacs1630+4520'
lens_name = 'slacs2238-0754'
# lens_name = 'slacs2300+0022'
# lens_name = 'slacs2303+1422'

ccd_data = ccd.load_ccd_data_from_fits(image_path=path + '/data/slacs/' + lens_name + '/F814W_image.fits',
                                       psf_path=path+'/data/slacs/'+lens_name+'/F814W_psf.fits',
                                       noise_map_path=path+'/data/slacs/'+lens_name+'/F814W_noise_map.fits',
                                       pixel_scale=0.03, resized_ccd_shape=(301, 301), resized_psf_shape=(21,21))

mask = msk.Mask.circular(shape=ccd_data.shape, pixel_scale=ccd_data.pixel_scale, radius_arcsec=3.0)

ccd_plotters.plot_ccd_subplot(ccd_data=ccd_data, mask=mask)

from workspace_jam.pipelines import lens_light_and_source_inversion

pipeline = lens_light_and_source_inversion.make_pipeline(pipeline_path='slacs/' + lens_name + '/')

pipeline.run(data=ccd_data)