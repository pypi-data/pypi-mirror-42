import numpy as np

def map_arrays_to_scaled_arrays(arrays_, map_to_scaled_arrays):
    """Map a list of masked 1D arrays (followed by an underscore _) to their masked 2D regular, using their
    *map_to_scaled_array* functions.

    Parameters
    -----------
    arrays_ : [ndarray]
        List of the arrays (e.g. datas_, model_images_, residual_map) which are mapped to 2D.
    map_to_scaled_arrays : [func]
        A list of functions which map each regular from 1D to 2D, using their masks.
    """
    return list(map(lambda _array, map_to_scaled_array, : map_to_scaled_array(_array), arrays_, map_to_scaled_arrays))

def map_contributions_to_scaled_arrays(contributions_, map_to_scaled_array):
    """Map a list of masked 1D contribution maps to their masked 2D unblurred_image_1d, using each unblurred_image_1d *map_to_scaled_array*
    function.

    The reason this is separate from the *map_arrays_to_scaled_arrays* function is that each regular has a list of
    contribution maps (one for each galaxy). Thus, this function breaks down the mapping of each map and returns the
    2D unblurred_image_1d in the same datas structure (2 lists with indexes [image_index][contribution_map_index].

    Parameters
    -----------
    contributions_ : [[ndarray]]
        Lists of the contribution maps which are mapped to 2D.
    map_to_scaled_arrays : [func]
        A list of functions which map each regular from 1D to 2D, using their masks.
    """
    return list(map(lambda _contribution : map_to_scaled_array(_contribution), contributions_))

def blur_images_including_blurring_regions(images_, blurring_images_, convolvers):
    """For a list of 1D masked unblurred_image_1d and 1D blurrings unblurred_image_1d (the regular regions outside the masks whose light blurs
    into the masks after PSF convolution), use both to computed the blurred regular within the masks via PSF convolution.

     The convolution uses each regular's convolver (*See ccd.convolution*).

    Parameters
    ----------
    image_ : [ndarray]
        List of the 1D masked unblurred_image_1d which are blurred.
    blurring_image : [ndarray]
        List of the 1D masked blurring unblurred_image_1d which are blurred.
    convolver : [ccd.convolution.Convolver]
        List of the convolvers which perform the convolution and have built into the the PSF kernel.
    """
    return list(map(lambda image_, blurring_image_, convolver :
                    convolver.convolve_image(image_array=image_, blurring_array=blurring_image_),
                    images_, blurring_images_, convolvers))

def residuals_from_datas_and_model_datas(datas_, model_datas_):
    """Compute the residual_map between a list of 1D masked observed datas and model datas, where:

    Residuals = (Data - Model_Data).

    For strong lens ccd, this subtracts the model lens regular from the observed regular within the masks.

    Parameters
    -----------
    datas_ : [np.ndarray]
        List of the 1D masked observed datas-sets.
    model_datas_ : [np.ndarray]
        List of the 1D masked model datas-sets.
    """
    return list(map(lambda data_, model_data_ : np.subtract(data_, model_data_), datas_, model_datas_))

def chi_squareds_from_residuals_and_noise_maps(residuals_, noise_maps_):
    """Computes the chi-squared unblurred_image_1d between a list of 1D masked residual_map and noise_map-maps, where:

    Chi_Squared = ((Residuals) / (Noise)) ** 2.0 = ((Data - Model)**2.0)/(Variances)

    Parameters
    -----------
    residuals_ : [np.ndarray]
        List of the 1D masked residual_map of the model-datas fit to the observed datas.
    noise_maps_ : [np.ndarray]
        List of the 1D masked noise_map-maps of the observed datas.
    """
    return list(map(lambda residual_, noise_map_ : np.square((np.divide(residual_, noise_map_))),
                    residuals_, noise_maps_))

def chi_squared_terms_from_chi_squareds(chi_squareds_):
    """Compute the chi-squared terms of each model's datas-set's fit to an observed datas-set, by summing the 1D masked
    chi-squared values of the fit.

    Parameters
    ----------
    chi_squareds_ : [np.ndarray]
        List of the 1D masked chi-squareds values of the model-datas fit to the observed datas.
    """
    return list(map(lambda chi_squared_ : np.sum(chi_squared_), chi_squareds_))

def noise_terms_from_noise_maps(noise_maps_):
    """Compute the noise_map-map normalization terms of a list of masked 1D noise_map-maps, summing the noise_map vale in every
    pixel as:

    [Noise_Term] = sum(log(2*pi*[Noise]**2.0))

    Parameters
    ----------
    noise_maps_ : [np.ndarray]
        List of masked 1D noise_map-maps.
    """
    return list(map(lambda noise_map_ : np.sum(np.log(2 * np.pi * noise_map_ ** 2.0)), noise_maps_))

def likelihoods_from_chi_squareds_and_noise_terms(chi_squared_terms, noise_terms):
    """Compute the likelihood of each masked 1D model-datas fit to the datas, where:

    Likelihood = -0.5*[Chi_Squared_Term + Noise_Term] (see functions above for these definitions)

    Parameters
    ----------
    chi_squared_terms : [float]
        List of the chi-squared terms for each model-datas fit to the observed datas.
    noise_terms : [float]
        List of the normalization noise_map-terms for each observed datas's noise_map-map.
    """
    return list(map(lambda chi_squared_term, noise_term : -0.5 * (chi_squared_term + noise_term),
                    chi_squared_terms, noise_terms))

def likelihoods_with_regularization_from_chi_squared_regularization_and_noise_terms(chi_squared_terms,
                                                                                    regularization_terms, noise_terms):
    """Compute the likelihood of each masked 1D model-datas fit to the datas, including the regularization term which
    comes from an inversion:

    Likelihood = -0.5*[Chi_Squared_Term + Regularization_Term + Noise_Term] (see functions above for these definitions)

    Parameters
    ----------
    chi_squared_terms : [float]
        List of the chi-squared terms for each model-datas fit to the observed datas.
    regularization_terms : [float]
        List of the regularization terms of the inversion, which is the sum of the difference between reconstructed \
        flux of every pixel multiplied by the regularization coefficient.
    noise_terms : [float]
        List of the normalization noise_map-terms for each observed datas's noise_map-map.
    """
    return list(map(lambda chi_squared_term, regularization_term, noise_term :
                    -0.5 * (chi_squared_term + regularization_term + noise_term),
                    chi_squared_terms, regularization_terms, noise_terms))

def evidences_from_reconstruction_terms(chi_squared_terms, regularization_terms, log_covariance_regularization_terms,
                                        log_regularization_terms, noise_terms):
    """Compute the evidence of each masked 1D model-datas fit to the datas, where an evidence includes a number of
    terms which quantify the complexity of an inversion's reconstruction (see the *inversion* module):

    Likelihood = -0.5*[Chi_Squared_Term + Regularization_Term + Log(Covariance_Regularization_Term) -
                       Log(Regularization_Matrix_Term) + Noise_Term]

    Parameters
    ----------
    chi_squared_terms : [float]
        List of the chi-squared terms for each model-datas fit to the observed datas.
    regularization_terms : [float]
        List of the regularization terms of the inversion, which is the sum of the difference between reconstructed \
        flux of every pixel multiplied by the regularization coefficient.
    noise_terms : [float]
        List of the normalization noise_map-terms for each observed datas's noise_map-map.
    """
    return list(map(lambda chi_squared_term, regularization_term, log_covariance_regularization_term,
                           log_regularization_term, noise_term :
                    -0.5 * (chi_squared_term + regularization_term + log_covariance_regularization_term -
                            log_regularization_term + noise_term),
                    chi_squared_terms, regularization_terms, log_covariance_regularization_terms,
                    log_regularization_terms, noise_terms))

def unmasked_blurred_images_from_fitting_images(fitting_images, unmasked_images_):
    """For a list of fitting unblurred_image_1d, compute an unmasked blurred unblurred_image_1d from a list of unmasked unblurred unblurred_image_1d.
    Unmasked unblurred_image_1d are used for plotting the results of a model outside a masked region.

    This relies on using a fitting regular's padded_grid, which is grid of coordinates which extends over the entire
    regular as opposed to just the masked region.

    Parameters
    ----------
    fitting_images_ : [fitting.fit_data.FitData]
        List of the fitting unblurred_image_1d.
    unmasked_images_ : [ndarray]
        List of the 1D unmasked unblurred_image_1d which are blurred.
    """
    return list(map(lambda fitting_image, _unmasked_image :
                    unmasked_model_image_from_fitting_image(fitting_image, _unmasked_image),
                    fitting_images, unmasked_images_))

def unmasked_model_image_from_fitting_image(fitting_image, unmasked_image_):
    """For a fitting regular, compute an unmasked blurred regular from an unmasked unblurred regular. Unmasked
    unblurred_image_1d are used for plotting the results of a model outside a masked region.

    This relies on using a fitting regular's padded_grid, which is grid of coordinates which extends over the entire
    regular as opposed to just the masked region.

    Parameters
    ----------
    fitting_image_ : fitting.fit_data.FitData
        A fitting_image, whose padded grid is used for PSF convolution.
    unmasked_images_ : [ndarray]
        The 1D unmasked unblurred_image_1d which are blurred.
    """
    _model_image = fitting_image.padded_grids.regular.convolve_array_1d_with_psf(unmasked_image_,
                                                                               fitting_image.psf)

    return fitting_image.padded_grids.regular.scaled_array_from_array_1d(_model_image)

def contributions_from_fitting_hyper_images_and_hyper_galaxies(fitting_hyper_images, hyper_galaxies):
    """For a list of fitting hyper-unblurred_image_1d (which includes the hyper model regular and hyper galaxy unblurred_image_1d) and model
    hyper-galaxies, compute their contribution maps, which are used to compute a scaled-noise_map map.

    Parameters
    ----------
    fitting_hyper_images : [fitting.fit_data.FitDataHyper]
        List of the fitting hyper-unblurred_image_1d.
    hyper_galaxies : [galaxy.Galaxy]
        The hyper-galaxies which represent the model components used to scale the noise_map, which correspond to
        individual galaxies in the regular.
    """
    return list(map(lambda hyp :
                    contributions_from_hyper_images_and_galaxies(hyper_model_image=hyp.hyper_model_image,
                                                                 hyper_galaxy_images=hyp.hyper_galaxy_images,
                                                                 hyper_galaxies=hyper_galaxies,
                                                                 minimum_values=hyp.hyper_minimum_values),
                fitting_hyper_images))

def contributions_from_hyper_images_and_galaxies(hyper_model_image, hyper_galaxy_images, hyper_galaxies, minimum_values):
    """For a fitting hyper-regular, hyper model regular, list of hyper galaxy unblurred_image_1d and model hyper-galaxies, compute
    their contribution maps, which are used to compute a scaled-noise_map map. All quantities are masked 1D arrays.

    The reason this is separate from the *contributions_from_fitting_hyper_images_and_hyper_galaxies* function is that
    each hyper regular has a list of hyper galaxy unblurred_image_1d and associated hyper galaxies (one for each galaxy). Thus,
    this function breaks down the calculation of each 1D masked contribution map and returns them in the same datas
    structure (2 lists with indexes [image_index][contribution_map_index].

    Parameters
    ----------
    hyper_model_image : ndarray
        The best-fit model regular to the datas (e.g. from a previous analysis phase).
    hyper_galaxy_images : [ndarray]
        The best-fit model regular of each hyper-galaxy to the datas (e.g. from a previous analysis phase).
    hyper_galaxies : [galaxy.Galaxy]
        The hyper-galaxies which represent the model components used to scale the noise_map, which correspond to
        individual galaxies in the regular.
    minimum_values : [float]
        The minimum value of each hyper-unblurred_image_1d contribution map, which ensure zero's don't impact the scaled noise_map-map.
    """
    # noinspection PyArgumentList
    return list(map(lambda hyper, galaxy_image, minimum_value:
                    hyper.contributions_from_hyper_images(hyper_model_image, galaxy_image, minimum_value),
                    hyper_galaxies, hyper_galaxy_images, minimum_values))

def scaled_noise_maps_from_fitting_hyper_images_contributions_and_hyper_galaxies(fitting_hyper_images, contributions_,
                                                                                 hyper_galaxies):
    """For a list of fitting hyper-unblurred_image_1d (which includes the hyper model regular and hyper galaxy unblurred_image_1d),
     contribution maps and model hyper-galaxies, compute their scaled noise_map-maps.

     This is performed by using each hyper-galaxy's *noise_factor* and *noise_power* parameter in conjunction with the
     unscaled noise_map-map and contribution map.

    Parameters
    ----------
    fitting_hyper_images : [fitting.fit_data.FitDataHyper]
        List of the fitting hyper-unblurred_image_1d.
    contributions_ : [[ndarray]]
        List of each regular's list of 1D masked contribution maps (e.g. one for each hyper-galaxy)
    hyper_galaxies : [galaxy.Galaxy]
        The hyper-galaxies which represent the model components used to scale the noise_map, which correspond to
        individual galaxies in the regular.
    """
    return list(map(lambda hyp, contribution_ :
                    scaled_noise_map_from_hyper_galaxies_and_contributions(contributions_=contribution_,
                                                                           hyper_galaxies=hyper_galaxies,
                                                                           noise_map_=hyp.noise_map_),
                    fitting_hyper_images, contributions_))

def scaled_noise_map_from_hyper_galaxies_and_contributions(contributions_, hyper_galaxies, noise_map_):
    """For a contribution map and noise_map-map, use the model hyper galaxies to computed a scaled noise_map-map.

    Parameters
    -----------
    contributions_ : ndarray
        The regular's list of 1D masked contribution maps (e.g. one for each hyper-galaxy)
    hyper_galaxies : [galaxy.Galaxy]
        The hyper-galaxies which represent the model components used to scale the noise_map, which correspond to
        individual galaxies in the regular.
    noise_maps : ccd.NoiseMap or ndarray
        An array describing the RMS standard deviation error in each pixel, preferably in units of electrons per
        second.
    """
    scaled_noises_ = list(map(lambda hyper, contribution_:
                              hyper.hyper_noise_from_contributions(noise_map_, contribution_),
                              hyper_galaxies, contributions_))
    return noise_map_ + sum(scaled_noises_)