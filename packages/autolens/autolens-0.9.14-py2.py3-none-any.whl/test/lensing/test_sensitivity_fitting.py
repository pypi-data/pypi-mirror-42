import numpy as np
import pytest

from autolens.data import ccd
from autolens.data.array import mask as mask
from autolens.model.galaxy import galaxy as g
from autolens.data.fitting import fitting_util
from autolens.lens import lens_data
from autolens.lens import sensitivity_fit
from autolens.lens import ray_tracing
from autolens.model.profiles import light_profiles as lp, mass_profiles as mp


@pytest.fixture(name="sersic")
def make_sersic():
    return lp.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=1.0, effective_radius=0.6, sersic_index=4.0)

@pytest.fixture(name="galaxy_light", scope='function')
def make_galaxy_light(sersic):
    return g.Galaxy(light_profile=sersic)

@pytest.fixture(name='si_blur')
def make_si_blur():
    psf = ccd.PSF(array=(np.array([[1.0, 1.0, 1.0],
                                   [1.0, 1.0, 1.0],
                                   [1.0, 1.0, 1.0]])), pixel_scale=1.0, renormalize=False)
    im = ccd.CCDData(image=5.0 * np.ones((4, 4)), pixel_scale=1.0, psf=psf, noise_map=np.ones((4, 4)),
                     exposure_time_map=3.0 * np.ones((4, 4)), background_sky_map=4.0 * np.ones((4, 4)))

    ma = np.array([[True, True, True, True],
                   [True, False, False, True],
                   [True, False, False, True],
                   [True, True, True, True]])
    ma = mask.Mask(array=ma, pixel_scale=1.0)

    return lens_data.LensData(im, ma, sub_grid_size=2)




class TestSensitivityProfileFit:

    def test__tracer_and_tracer_sensitive_are_identical__added__likelihood_is_noise_term(self, si_blur):

        g0 = g.Galaxy(mass_profile=mp.SphericalIsothermal(einstein_radius=1.0))
        g1 = g.Galaxy(light_profile=lp.EllipticalSersic(intensity=2.0))

        tracer = ray_tracing.TracerImageSourcePlanes(lens_galaxies=[g0], source_galaxies=[g1],
                                                     image_plane_grid_stack=[si_blur.grids])

        fit = sensitivity_fit.SensitivityProfileFit(lensing_image=[si_blur], tracer_normal=tracer,
                                                    tracer_sensitive=tracer)

        assert (fit.fit_normal.datas_[0] == si_blur).all()
        assert (fit.fit_normal.noise_maps_[0] == si_blur.noise_map_).all()

        model_datas_ = fitting_util.blur_image_including_blurring_region(image_=[tracer.image_plane_images_1d[0]],
                                                                         blurring_image_=[tracer.image_plane_blurring_images_1d[0]],
                                                                         convolver=[si_blur.convolver_image])

        assert (fit.fit_normal.model_datas_[0] == model_datas_[0]).all()

        residuals_ = fitting_util.residual_map_from_data_mask_and_model_data(data=[si_blur],
                                                                             model_data=[model_datas_])
        assert (fit.fit_normal.residuals_[0] == residuals_[0]).all()

        chi_squareds_ = fitting_util.chi_squared_map_from_residual_map_mask_and_noise_map(residual_map=residuals_,
                                                                                          noise_map=[si_blur.noise_map_])
        assert (fit.fit_normal.chi_squareds_[0] == chi_squareds_).all()



        assert (fit.fit_sensitive.datas_[0] == si_blur).all()
        assert (fit.fit_sensitive.noise_maps_[0] == si_blur.noise_map_).all()

        model_datas_ = fitting_util.blur_image_including_blurring_region(image_=[tracer.image_plane_images_1d[0]],
                                                                         blurring_image_=[
                                                                          tracer.image_plane_blurring_images_1d[0]],
                                                                         convolver=[si_blur.convolver_image])

        assert (fit.fit_sensitive.model_datas_[0] == model_datas_[0]).all()

        residuals_ = fitting_util.residual_map_from_data_mask_and_model_data(data=[si_blur],
                                                                             model_data=[model_datas_])
        assert (fit.fit_sensitive.residuals_[0] == residuals_[0]).all()

        chi_squareds_ = fitting_util.chi_squared_map_from_residual_map_mask_and_noise_map(residual_map=residuals_,
                                                                                          noise_map=[si_blur.noise_map_])
        assert (fit.fit_sensitive.chi_squareds_[0] == chi_squareds_).all()

        chi_squared_term = sum(fitting_util.chi_squared_from_chi_squared_map(chi_squared_map=chi_squareds_))
        noise_term = sum(fitting_util.noise_normalization_from_mask_and_noise_map(noise_map=[si_blur.noise_map_]))
        assert fit.fit_normal.figure_of_merit == -0.5 * (chi_squared_term + noise_term)
        assert fit.fit_sensitive.figure_of_merit == -0.5 * (chi_squared_term + noise_term)

        assert fit.figure_of_merit == 0.0

        fast_likelihood = sensitivity_fit.SensitivityProfileFit.fast_fit(
            sensitivity_images=[si_blur], tracer_normal=tracer, tracer_sensitive=tracer)

        assert fit.figure_of_merit == fast_likelihood

    def test__tracers_are_different__likelihood_is_non_zero(self, si_blur):

        g0 = g.Galaxy(mass_profile=mp.SphericalIsothermal(einstein_radius=1.0))
        g0_subhalo = g.Galaxy(subhalo=mp.SphericalIsothermal(einstein_radius=0.1))
        g1 = g.Galaxy(light_profile=lp.EllipticalSersic(intensity=2.0))

        tracer_normal = ray_tracing.TracerImageSourcePlanes(lens_galaxies=[g0], source_galaxies=[g1],
                                                            image_plane_grid_stack=[si_blur.grids])

        tracer_sensitive = ray_tracing.TracerImageSourcePlanes(lens_galaxies=[g0, g0_subhalo], source_galaxies=[g1],
                                                               image_plane_grid_stack=[si_blur.grids])

        fit = sensitivity_fit.SensitivityProfileFit(lensing_image=[si_blur], tracer_normal=tracer_normal,
                                                    tracer_sensitive=tracer_sensitive)

        assert (fit.fit_normal.datas_[0] == si_blur).all()
        assert (fit.fit_normal.noise_maps_[0] == si_blur.noise_map_).all()

        model_datas_ = fitting_util.blur_image_including_blurring_region(
            image_=[tracer_normal.image_plane_images_1d[0]],
            blurring_image_=[tracer_normal.image_plane_blurring_images_1d[0]],
            convolver=[si_blur.convolver_image])

        assert (fit.fit_normal.model_datas_[0] == model_datas_[0]).all()

        residuals_ = fitting_util.residual_map_from_data_mask_and_model_data(data=[si_blur],
                                                                             model_data=[model_datas_])
        assert (fit.fit_normal.residuals_[0] == residuals_[0]).all()

        chi_squareds_normal_ = fitting_util.chi_squared_map_from_residual_map_mask_and_noise_map(residual_map=residuals_,
                                                                                                 noise_map=[si_blur.noise_map_])
        assert (fit.fit_normal.chi_squareds_[0] == chi_squareds_normal_).all()



        assert (fit.fit_sensitive.datas_[0] == si_blur).all()
        assert (fit.fit_sensitive.noise_maps_[0] == si_blur.noise_map_).all()

        model_datas_ = fitting_util.blur_image_including_blurring_region(
            image_=[tracer_sensitive.image_plane_images_1d[0]],
            blurring_image_=[tracer_sensitive.image_plane_blurring_images_1d[0]],
            convolver=[si_blur.convolver_image])

        assert (fit.fit_sensitive.model_datas_[0] == model_datas_[0]).all()

        residuals_ = fitting_util.residual_map_from_data_mask_and_model_data(data=[si_blur], model_data=[model_datas_])
        assert (fit.fit_sensitive.residuals_[0] == residuals_[0]).all()

        chi_squareds_sensitive = fitting_util.chi_squared_map_from_residual_map_mask_and_noise_map(residual_map=residuals_,
                                                                                                   noise_map=[si_blur.noise_map_])
        assert (fit.fit_sensitive.chi_squareds_[0] == chi_squareds_sensitive).all()

        chi_squared_term_normal = \
            sum(fitting_util.chi_squared_from_chi_squared_map(chi_squared_map=chi_squareds_normal_))
        chi_squared_term_sensitive = \
            sum(fitting_util.chi_squared_from_chi_squared_map(chi_squared_map=chi_squareds_sensitive))
        noise_term = sum(fitting_util.noise_normalization_from_mask_and_noise_map(noise_map=[si_blur.noise_map_]))
        assert fit.fit_normal.figure_of_merit == -0.5 * (chi_squared_term_normal + noise_term)
        assert fit.fit_sensitive.figure_of_merit == -0.5 * (chi_squared_term_sensitive + noise_term)

        assert fit.figure_of_merit == fit.fit_sensitive.figure_of_merit - fit.fit_normal.figure_of_merit

        fast_likelihood = sensitivity_fit.SensitivityProfileFit.fast_fit(
            sensitivity_images=[si_blur], tracer_normal=tracer_normal, tracer_sensitive=tracer_sensitive)

        assert fit.figure_of_merit == fast_likelihood