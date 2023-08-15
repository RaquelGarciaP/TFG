import numpy as np


class KeplerianOrbit:
    """
    Description:
    Computation of the keplerian radial velocity

    Input parameters:
        t: array of time
        period: orbital period
        K: radial velocity semi-amplitude
        ecc: eccentricity of the orbit
        omega: angle of periastron
        t_peri: time of periastron_passage

    Output parameters:
        rv: radial velocity array
    """

    def __init__(self, t, period, ecc, t_peri):
        self.__t = t
        self.__period = period
        self.__ecc = ecc
        self.__t_peri = t_peri

        # sin and cos of the true anomaly
        self.__sinf, self.__cosf = self.__true_anomaly(self.__t, self.__period, self.__ecc, self.__t_peri)

    def keplerian_orbit(self, K, omega):
        #   Description:
        #      Computation of the keplerian radial velocity
        #   Input parameters:
        #      t: array of time
        #      period: orbital period
        #      K: radial velocity semi-amplitude
        #      ecc: eccentricity of the orbit
        #      omega: angle of periastron
        #      t_peri: time of periastron_passage
        #   Output parameters:
        #      rv: radial velocity array

        # period, rv, ecc, omega, t_peri = params
        omega = omega * np.pi / 180.0  # converting omega from degrees to radians
        # sinf, cosf = self.__true_anomaly(t, period, ecc, t_peri)
        cosftrueomega = self.__cosf * np.cos(omega) - self.__sinf * np.sin(omega)  # cos(f+omega) = cosf*cos(omega) - sinf*sin(omega)
        rv = K * (self.__ecc * np.cos(omega) + cosftrueomega)
        return rv

    def __true_anomaly(self, t, period, ecc, t_peri):
        #   Description:
        #      Computation of the true anomaly solving the Kepler
        #      equations numerically. A precision of 1.EE-06 is
        #      hard coded.
        #   Input parameters:
        #      t: array of time
        #      period: orbital period
        #      ecc: eccentricity of the orbit
        #      t_peri: time of periastron_passage
        #   Output parameters:
        #      sinf: sin of the true anomaly
        #      cosf: cos of the true anomaly
        sinf = []
        cosf = []
        for i in range(len(t)):
            fmean = 2.0 * np.pi * (t[i] - t_peri) / period  # mean anomaly

            # Solve Kepler eq by Newton's method x(n+1)=x(n)-f(x(n))/f'(x(n))
            fecc = fmean
            diff = 1.0
            while diff > 1.0E-6:
                fecc_0 = fecc
                fecc = fecc_0 - (fecc_0 - ecc * np.sin(fecc_0) - fmean) / (
                            1.0 - ecc * np.cos(fecc_0))  # eccentric anomaly
                diff = np.abs(fecc - fecc_0)

            # calculation of the sin and cos of the true anomaly
            sinf.append(np.sqrt(1.0 - ecc * ecc) * np.sin(fecc) / (1.0 - ecc * np.cos(fecc)))  # sin true anomaly
            cosf.append((np.cos(fecc) - ecc) / (1.0 - ecc * np.cos(fecc)))  # cos true anomaly

        return np.array(sinf), np.array(cosf)
