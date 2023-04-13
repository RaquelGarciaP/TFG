from astropy.io import fits
# from importlib.metadata import packages_distributions
# import importlib.metadata


hdul = fits.open('car-20160520T03h10m13s-sci-gtoc-vis_A.fits')
hdul.info()
print('\n')
print(hdul['WAVE'].header)
print(hdul['WAVE'].data[60])
print(len(hdul['WAVE'].data[60]))
