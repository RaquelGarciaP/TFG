import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio
from astropy.io import fits


CARMENES_info = pd.read_csv('./CARMENES_data/info_observations.csv')
CARMENES_filenames = CARMENES_info['FILENAME']

order = 35  # we do the plot for a concrete order

images = []
for i in range(len(CARMENES_filenames)):

    # read the CARMENES file corresponding to the time_i
    file_path = './CombinedSpectra/binary_v1/' + CARMENES_filenames.iloc[i]
    CARMENES_file = fits.open(file_path)

    # crete a data frame whose columns contain the flux and wavelength of the CARMENES file
    file_i = pd.DataFrame()
    file_i['wl'] = CARMENES_file['WAVE'].data[order]
    file_i['flux'] = CARMENES_file['SPEC'].data[order]

    # close the file
    CARMENES_file.close()

    # choose the rows with the mask
    #mask = (file_i['wl'] >= 8040) & (file_i['wl'] <= 8060)
    #file_i = file_i[mask]

    # GIF:
    # Crear lista de imágenes a partir de los datos
    fig, ax = plt.subplots(figsize=(14, 8))
    file_i.plot(x='wl', y='flux', ax=ax)
    ax.set_title(f'Frame {i}')
    fig.canvas.draw()
    image = np.array(fig.canvas.renderer.buffer_rgba())
    images.append(image)
    plt.close()

# Guardar lista de imágenes en un archivo .gif
imageio.mimsave('./CombinedSpectra/time_evolution_synthetic_35.gif', images, fps=2)
