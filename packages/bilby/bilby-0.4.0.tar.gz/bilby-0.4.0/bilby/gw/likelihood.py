from __future__ import division
import numpy as np
from scipy.interpolate import interp1d

try:
    from scipy.special import logsumexp
except ImportError:
    from scipy.misc import logsumexp
from scipy.special import i0e

from ..core import likelihood
from ..core.utils import logger, UnsortedInterp2d
from ..core.prior import Prior, Uniform
from .detector import InterferometerList
from .prior import BBHPriorDict
from .source import lal_binary_black_hole
from .utils import noise_weighted_inner_product, build_roq_weights, blockwise_dot_product
from .waveform_generator import WaveformGenerator
from math import ceil


class GravitationalWaveTransient(likelihood.Likelihood):
    """ A gravitational-wave transient likelihood object

    This is the usual likelihood object to use for transient gravitational
    wave parameter estimation. It computes the log-likelihood in the frequency
    domain assuming a colored Gaussian noise model described by a power
    spectral density


    Parameters
    ----------
    interferometers: list, bilby.gw.detector.InterferometerList
        A list of `bilby.detector.Interferometer` instances - contains the
        detector data and power spectral densities
    waveform_generator: `bilby.waveform_generator.WaveformGenerator`
        An object which computes the frequency-domain strain of the signal,
        given some set of parameters
    distance_marginalization: bool, optional
        If true, marginalize over distance in the likelihood.
        This uses a look up table calculated at run time.
    time_marginalization: bool, optional
        If true, marginalize over time in the likelihood.
        This uses a FFT.
    phase_marginalization: bool, optional
        If true, marginalize over phase in the likelihood.
        This is done analytically using a Bessel function.
    priors: dict, optional
        If given, used in the distance and phase marginalization.

    Returns
    -------
    Likelihood: `bilby.core.likelihood.Likelihood`
        A likelihood object, able to compute the likelihood of the data given
        some model parameters

    """

    def __init__(self, interferometers, waveform_generator, time_marginalization=False, distance_marginalization=False,
                 phase_marginalization=False, priors=None):

        self.waveform_generator = waveform_generator
        likelihood.Likelihood.__init__(self, dict())
        self.interferometers = InterferometerList(interferometers)
        self.time_marginalization = time_marginalization
        self.distance_marginalization = distance_marginalization
        self.phase_marginalization = phase_marginalization
        self.priors = priors
        self._check_set_duration_and_sampling_frequency_of_waveform_generator()
        self.meta_data = dict(
            interferometers=self.interferometers.meta_data,
            time_marginalization=self.time_marginalization,
            phase_marginalization=self.phase_marginalization,
            distance_marginalization=self.distance_marginalization,
            waveform_arguments=waveform_generator.waveform_arguments,
            frequency_domain_source_model=waveform_generator.frequency_domain_source_model)

        if self.time_marginalization:
            self._check_prior_is_set(key='geocent_time')
            self._setup_time_marginalization()
            priors['geocent_time'] = float(self.interferometers.start_time)

        if self.phase_marginalization:
            self._check_prior_is_set(key='phase')
            self._bessel_function_interped = None
            self._setup_phase_marginalization()
            priors['phase'] = float(0)

        if self.distance_marginalization:
            self._check_prior_is_set(key='luminosity_distance')
            self._distance_array = np.linspace(self.priors['luminosity_distance'].minimum,
                                               self.priors['luminosity_distance'].maximum, int(1e4))
            self._setup_distance_marginalization()
            priors['luminosity_distance'] = float(self._ref_dist)

    def __repr__(self):
        return self.__class__.__name__ + '(interferometers={},\n\twaveform_generator={},\n\ttime_marginalization={}, ' \
                                         'distance_marginalization={}, phase_marginalization={}, priors={})'\
            .format(self.interferometers, self.waveform_generator, self.time_marginalization,
                    self.distance_marginalization, self.phase_marginalization, self.priors)

    def _check_set_duration_and_sampling_frequency_of_waveform_generator(self):
        """ Check the waveform_generator has the same duration and
        sampling_frequency as the interferometers. If they are unset, then
        set them, if they differ, raise an error
        """

        attributes = ['duration', 'sampling_frequency', 'start_time']
        for attr in attributes:
            wfg_attr = getattr(self.waveform_generator, attr)
            ifo_attr = getattr(self.interferometers, attr)
            if wfg_attr is None:
                logger.debug(
                    "The waveform_generator {} is None. Setting from the "
                    "provided interferometers.".format(attr))
            elif wfg_attr != ifo_attr:
                logger.warning(
                    "The waveform_generator {} is not equal to that of the "
                    "provided interferometers. Overwriting the "
                    "waveform_generator.".format(attr))
            setattr(self.waveform_generator, attr, ifo_attr)

    def _check_prior_is_set(self, key):
        if key not in self.priors or not isinstance(
                self.priors[key], Prior):
            logger.warning(
                'Prior not provided for {}, using the BBH default.'.format(key))
            if key == 'geocent_time':
                self.priors[key] = Uniform(
                    self.interferometers.start_time,
                    self.interferometers.start_time + self.interferometers.duration)
            else:
                self.priors[key] = BBHPriorDict()[key]

    @property
    def priors(self):
        return self.__prior

    @priors.setter
    def priors(self, priors):
        if priors is not None:
            self.__prior = priors.copy()
        elif any([self.time_marginalization, self.phase_marginalization,
                  self.distance_marginalization]):
            raise ValueError("You can't use a marginalized likelihood without specifying a priors")
        else:
            self.__prior = None

    def noise_log_likelihood(self):
        log_l = 0
        for interferometer in self.interferometers:
            log_l -= noise_weighted_inner_product(
                interferometer.frequency_domain_strain,
                interferometer.frequency_domain_strain,
                interferometer.power_spectral_density_array,
                self.waveform_generator.duration) / 2
        return log_l.real

    def log_likelihood_ratio(self):
        waveform_polarizations =\
            self.waveform_generator.frequency_domain_strain(self.parameters)

        if waveform_polarizations is None:
            return np.nan_to_num(-np.inf)

        d_inner_h = 0
        optimal_snr_squared = 0
        d_inner_h_squared_tc_array = np.zeros(
            self.interferometers.frequency_array[0:-1].shape,
            dtype=np.complex128)
        for interferometer in self.interferometers:
            signal_ifo = interferometer.get_detector_response(
                waveform_polarizations, self.parameters)

            d_inner_h += interferometer.inner_product(signal=signal_ifo)
            optimal_snr_squared += interferometer.optimal_snr_squared(signal=signal_ifo)
            if self.time_marginalization:
                d_inner_h_squared_tc_array +=\
                    4 / self.waveform_generator.duration * np.fft.fft(
                        signal_ifo[0:-1] *
                        interferometer.frequency_domain_strain.conjugate()[0:-1] /
                        interferometer.power_spectral_density_array[0:-1])

        if self.time_marginalization:

            if self.distance_marginalization:
                rho_mf_ref_tc_array, rho_opt_ref = self._setup_rho(
                    d_inner_h_squared_tc_array, optimal_snr_squared)
                if self.phase_marginalization:
                    dist_marged_log_l_tc_array = self._interp_dist_margd_loglikelihood(
                        abs(rho_mf_ref_tc_array), rho_opt_ref)
                else:
                    dist_marged_log_l_tc_array = self._interp_dist_margd_loglikelihood(
                        rho_mf_ref_tc_array.real, rho_opt_ref)
                log_l = logsumexp(dist_marged_log_l_tc_array,
                                  b=self.time_prior_array)
            elif self.phase_marginalization:
                log_l = logsumexp(self._bessel_function_interped(abs(
                    d_inner_h_squared_tc_array)),
                    b=self.time_prior_array) - optimal_snr_squared / 2
            else:
                log_l = logsumexp(
                    d_inner_h_squared_tc_array.real,
                    b=self.time_prior_array) - optimal_snr_squared / 2

        elif self.distance_marginalization:
            rho_mf_ref, rho_opt_ref = self._setup_rho(d_inner_h, optimal_snr_squared)
            if self.phase_marginalization:
                rho_mf_ref = abs(rho_mf_ref)
            log_l = self._interp_dist_margd_loglikelihood(rho_mf_ref.real, rho_opt_ref)[0]

        elif self.phase_marginalization:
            d_inner_h = self._bessel_function_interped(abs(d_inner_h))
            log_l = d_inner_h - optimal_snr_squared / 2

        else:
            log_l = d_inner_h.real - optimal_snr_squared / 2

        return log_l.real

    def _setup_rho(self, d_inner_h, optimal_snr_squared):
        rho_opt_ref = (optimal_snr_squared.real *
                       self.parameters['luminosity_distance'] ** 2 /
                       self._ref_dist ** 2.)
        rho_mf_ref = (d_inner_h * self.parameters['luminosity_distance'] /
                      self._ref_dist)
        return rho_mf_ref, rho_opt_ref

    def log_likelihood(self):
        return self.log_likelihood_ratio() + self.noise_log_likelihood()

    @property
    def _delta_distance(self):
        return self._distance_array[1] - self._distance_array[0]

    @property
    def _ref_dist(self):
        """ Smallest distance contained in priors """
        return self._distance_array[0]

    @property
    def _rho_opt_ref_array(self):
        """ Optimal filter snr at fiducial distance of ref_dist Mpc """
        return np.logspace(-5, 10, self._dist_margd_loglikelihood_array.shape[0])

    @property
    def _rho_mf_ref_array(self):
        """ Matched filter snr at fiducial distance of ref_dist Mpc """
        if self.phase_marginalization:
            return np.logspace(-5, 10, self._dist_margd_loglikelihood_array.shape[1])
        else:
            return np.hstack((-np.logspace(3, -3, self._dist_margd_loglikelihood_array.shape[1] / 2),
                              np.logspace(-3, 10, self._dist_margd_loglikelihood_array.shape[1] / 2)))

    def _setup_distance_marginalization(self):
        self._create_lookup_table()
        self._interp_dist_margd_loglikelihood = UnsortedInterp2d(
            self._rho_mf_ref_array, self._rho_opt_ref_array,
            self._dist_margd_loglikelihood_array)

    def _create_lookup_table(self):
        """ Make the lookup table """
        self.distance_prior_array = np.array([self.priors['luminosity_distance'].prob(distance)
                                              for distance in self._distance_array])
        logger.info('Building lookup table for distance marginalisation.')

        self._dist_margd_loglikelihood_array = np.zeros((400, 800))
        for ii, rho_opt_ref in enumerate(self._rho_opt_ref_array):
            for jj, rho_mf_ref in enumerate(self._rho_mf_ref_array):
                optimal_snr_squared_array = rho_opt_ref * self._ref_dist ** 2. / self._distance_array ** 2
                d_inner_h_array = rho_mf_ref * self._ref_dist / self._distance_array
                if self.phase_marginalization:
                    d_inner_h_array =\
                        self._bessel_function_interped(abs(d_inner_h_array))
                self._dist_margd_loglikelihood_array[ii][jj] = \
                    logsumexp(d_inner_h_array - optimal_snr_squared_array / 2,
                              b=self.distance_prior_array * self._delta_distance)
        log_norm = logsumexp(0. / self._distance_array - 0. / self._distance_array ** 2.,
                             b=self.distance_prior_array * self._delta_distance)
        self._dist_margd_loglikelihood_array -= log_norm

    def _setup_phase_marginalization(self):
        self._bessel_function_interped = interp1d(
            np.logspace(-5, 10, int(1e6)), np.logspace(-5, 10, int(1e6)) +
            np.log([i0e(snr) for snr in np.logspace(-5, 10, int(1e6))]),
            bounds_error=False, fill_value=(0, np.nan))

    def _setup_time_marginalization(self):
        delta_tc = 2 / self.waveform_generator.sampling_frequency
        times =\
            self.interferometers.start_time + np.linspace(
                0, self.interferometers.duration,
                int(self.interferometers.duration / 2 *
                    self.waveform_generator.sampling_frequency + 1))[1:]
        self.time_prior_array =\
            self.priors['geocent_time'].prob(times) * delta_tc


class BasicGravitationalWaveTransient(likelihood.Likelihood):

    def __init__(self, interferometers, waveform_generator):
        """

        A likelihood object, able to compute the likelihood of the data given
        some model parameters

        The simplest frequency-domain gravitational wave transient likelihood. Does
        not include distance/phase marginalization.


        Parameters
        ----------
        interferometers: list
            A list of `bilby.gw.detector.Interferometer` instances - contains the
            detector data and power spectral densities
        waveform_generator: bilby.gw.waveform_generator.WaveformGenerator
            An object which computes the frequency-domain strain of the signal,
            given some set of parameters

        """
        likelihood.Likelihood.__init__(self, dict())
        self.interferometers = interferometers
        self.waveform_generator = waveform_generator

    def __repr__(self):
        return self.__class__.__name__ + '(interferometers={},\n\twaveform_generator={})'\
            .format(self.interferometers, self.waveform_generator)

    def noise_log_likelihood(self):
        """ Calculates the real part of noise log-likelihood

        Returns
        -------
        float: The real part of the noise log likelihood

        """
        log_l = 0
        for interferometer in self.interferometers:
            log_l -= 2. / self.waveform_generator.duration * np.sum(
                abs(interferometer.frequency_domain_strain) ** 2 /
                interferometer.power_spectral_density_array)
        return log_l.real

    def log_likelihood(self):
        """ Calculates the real part of log-likelihood value

        Returns
        -------
        float: The real part of the log likelihood

        """
        log_l = 0
        waveform_polarizations =\
            self.waveform_generator.frequency_domain_strain(
                self.parameters.copy())
        if waveform_polarizations is None:
            return np.nan_to_num(-np.inf)
        for interferometer in self.interferometers:
            log_l += self.log_likelihood_interferometer(
                waveform_polarizations, interferometer)
        return log_l.real

    def log_likelihood_interferometer(self, waveform_polarizations,
                                      interferometer):
        """

        Parameters
        ----------
        waveform_polarizations: dict
            Dictionary containing the desired waveform polarization modes and the related strain
        interferometer: bilby.gw.detector.Interferometer
            The Interferometer object we want to have the log-likelihood for

        Returns
        -------
        float: The real part of the log-likelihood for this interferometer

        """
        signal_ifo = interferometer.get_detector_response(
            waveform_polarizations, self.parameters)

        log_l = - 2. / self.waveform_generator.duration * np.vdot(
            interferometer.frequency_domain_strain - signal_ifo,
            (interferometer.frequency_domain_strain - signal_ifo) /
            interferometer.power_spectral_density_array)
        return log_l.real


class ROQGravitationalWaveTransient(GravitationalWaveTransient):
    """A reduced order quadrature likelihood object

    This uses the method described in Smith et al., (2016) Phys. Rev. D 94,
    044031. A public repository of the ROQ data is available from
    https://git.ligo.org/lscsoft/ROQ_data.

    Parameters
    ----------
    interferometers: list, bilby.gw.detector.InterferometerList
        A list of `bilby.detector.Interferometer` instances - contains the
        detector data and power spectral densities
    waveform_generator: `bilby.waveform_generator.WaveformGenerator`
        An object which computes the frequency-domain strain of the signal,
        given some set of parameters
    linear_matrix: str, array
        Either a string point to the file from which to load the linear_matrix
        array, or the array itself.
    quadratic_matrix: str, array
        Either a string point to the file from which to load the quadratic_matrix
        array, or the array itself.
    priors: dict, bilby.prior.PriorDict
        A dictionary of priors containing at least the geocent_time prior

    """
    def __init__(self, interferometers, waveform_generator,
                 linear_matrix, quadratic_matrix, priors):
        GravitationalWaveTransient.__init__(
            self, interferometers=interferometers,
            waveform_generator=waveform_generator, priors=priors)

        if isinstance(linear_matrix, str):
            logger.info("Loading linear matrix from {}".format(linear_matrix))
            linear_matrix = np.load(linear_matrix).T
        if isinstance(quadratic_matrix, str):
            logger.info("Loading quadratic_matrix from {}".format(quadratic_matrix))
            quadratic_matrix = np.load(quadratic_matrix).T

        self.linear_matrix = linear_matrix
        self.quadratic_matrix = quadratic_matrix
        self.time_samples = None
        self.weights = dict()
        self._set_weights()
        self.frequency_nodes_linear =\
            waveform_generator.waveform_arguments['frequency_nodes_linear']

    def log_likelihood_ratio(self):
        optimal_snr_squared = 0.
        matched_filter_snr_squared = 0.

        indices, in_bounds = self._closest_time_indices(
            self.parameters['geocent_time'] - self.interferometers.start_time)
        if not in_bounds:
            return np.nan_to_num(-np.inf)

        waveform = self.waveform_generator.frequency_domain_strain(
            self.parameters)
        if waveform is None:
            return np.nan_to_num(-np.inf)

        for ifo in self.interferometers:

            f_plus = ifo.antenna_response(
                self.parameters['ra'], self.parameters['dec'],
                self.parameters['geocent_time'], self.parameters['psi'], 'plus')
            f_cross = ifo.antenna_response(
                self.parameters['ra'], self.parameters['dec'],
                self.parameters['geocent_time'], self.parameters['psi'], 'cross')

            dt = ifo.time_delay_from_geocenter(
                self.parameters['ra'], self.parameters['dec'],
                ifo.strain_data.start_time)
            ifo_time = self.parameters['geocent_time'] + dt - \
                ifo.strain_data.start_time

            h_plus_linear = f_plus * waveform['linear']['plus']
            h_cross_linear = f_cross * waveform['linear']['cross']
            h_plus_quadratic = f_plus * waveform['quadratic']['plus']
            h_cross_quadratic = f_cross * waveform['quadratic']['cross']

            indices, in_bounds = self._closest_time_indices(ifo_time)
            if not in_bounds:
                return np.nan_to_num(-np.inf)

            matched_filter_snr_squared_array = np.einsum(
                'i,ji->j', np.conjugate(h_plus_linear + h_cross_linear),
                self.weights[ifo.name + '_linear'][indices])

            matched_filter_snr_squared += interp1d(
                self.time_samples[indices],
                matched_filter_snr_squared_array, kind='quadratic')(ifo_time)

            optimal_snr_squared += \
                np.vdot(np.abs(h_plus_quadratic + h_cross_quadratic)**2,
                        self.weights[ifo.name + '_quadratic'])

        log_l = matched_filter_snr_squared - optimal_snr_squared / 2

        return log_l.real

    def _closest_time_indices(self, time):
        """
        Get the closest an two neighbouring times

        Parameters
        ----------
        time: float
            Time to check

        Returns
        -------
        indices: list
            Indices nearest to time.
        in_bounds: bool
            Whether the indices are for valid times.
        """
        closest = np.argmin(np.absolute(self.time_samples - time))
        indices = [closest + ii for ii in [-1, 0, 1]]
        in_bounds = (indices[0] >= 0) & (indices[2] < self.time_samples.size)
        return indices, in_bounds

    def _set_weights(self):
        """
        Setup the time-dependent ROQ weights.
        This follows FIXME: Smith et al.

        The times are chosen to allow all the merger times allows in the time
        prior.
        """
        for ifo in self.interferometers:
            # only get frequency components up to maximum_frequency
            self.linear_matrix = \
                self.linear_matrix[:, :sum(ifo.frequency_mask)]
            self.quadratic_matrix = \
                self.quadratic_matrix[:, :sum(ifo.frequency_mask)]

            # array of relative time shifts to be applied to the data
            # 0.045s comes from time for GW to traverse the Earth
            self.time_samples = np.linspace(
                self.priors['geocent_time'].minimum - 0.045,
                self.priors['geocent_time'].maximum + 0.045,
                int(ceil((self.priors['geocent_time'].maximum -
                          self.priors['geocent_time'].minimum + 0.09) *
                         ifo.strain_data.sampling_frequency)))
            self.time_samples -= ifo.strain_data.start_time
            time_space = self.time_samples[1] - self.time_samples[0]

            # array to be filled with data, shifted by discrete time_samples
            tc_shifted_data = np.zeros([
                len(self.time_samples),
                len(ifo.frequency_array[ifo.frequency_mask])], dtype=complex)

            # shift data to beginning of the prior
            # increment by the time step
            shifted_data =\
                ifo.frequency_domain_strain[ifo.frequency_mask] * \
                np.exp(2j * np.pi * ifo.frequency_array[ifo.frequency_mask] *
                       self.time_samples[0])
            single_time_shift = np.exp(
                2j * np.pi * ifo.frequency_array[ifo.frequency_mask] *
                time_space)
            for j in range(len(self.time_samples)):
                tc_shifted_data[j] = shifted_data
                shifted_data *= single_time_shift

            # to not kill all computers this minimises the memory usage of the
            # required inner products
            max_block_gigabytes = 4
            max_elements = int((max_block_gigabytes * 2 ** 30) / 8)

            self.weights[ifo.name + '_linear'] = blockwise_dot_product(
                tc_shifted_data /
                ifo.power_spectral_density_array[ifo.frequency_mask],
                self.linear_matrix, max_elements) * 4 / ifo.strain_data.duration

            del tc_shifted_data

            self.weights[ifo.name + '_quadratic'] = build_roq_weights(
                1 / ifo.power_spectral_density_array[ifo.frequency_mask],
                self.quadratic_matrix.real, 1 / ifo.strain_data.duration)


def get_binary_black_hole_likelihood(interferometers):
    """ A rapper to quickly set up a likelihood for BBH parameter estimation

    Parameters
    ----------
    interferometers: {bilby.gw.detector.InterferometerList, list}
        A list of `bilby.detector.Interferometer` instances, typically the
        output of either `bilby.detector.get_interferometer_with_open_data`
        or `bilby.detector.get_interferometer_with_fake_noise_and_injection`

    Returns
    -------
    bilby.GravitationalWaveTransient: The likelihood to pass to `run_sampler`

    """
    waveform_generator = WaveformGenerator(
        duration=interferometers.duration,
        sampling_frequency=interferometers.sampling_frequency,
        frequency_domain_source_model=lal_binary_black_hole,
        waveform_arguments={'waveform_approximant': 'IMRPhenomPv2',
                            'reference_frequency': 50})
    return GravitationalWaveTransient(interferometers, waveform_generator)
