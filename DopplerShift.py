

class DopplerShift:

    def __init__(self, data, radial_vel):

        self.__radial_vel = radial_vel
        self.__c = 299792458  # light velocity (m/s)

        # data contains two columns (wl, flux). We select the wl
        self.__wl = data['wl']

    def apply_shift(self):
        print('Applying Doppler Shift')
        # loop to apply the Doppler shift:
        for i in range(len(self.__wl)):
            self.__wl[i] = (1 + float(self.__radial_vel) / float(self.__c)) * self.__wl[i]
