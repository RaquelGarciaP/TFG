import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio


file = pd.read_csv('./CombinedSpectra/test_file.csv')

'''column_name_wl = 'wl_time_2'
column_name_flux = 'flux_time_2'
file_i = pd.DataFrame()
file_i['wl'] = file[column_name_wl].copy()
file_i['flux'] = file[column_name_flux].copy()

plt.plot(file_i['wl'], file_i['flux'])
plt.show()'''

images = []
for i in range(100):
    # choose the columns of the file
    column_name_wl = 'wl_time_' + str(i)
    column_name_flux = 'flux_time_' + str(i)
    file_i = pd.DataFrame()
    file_i['wl'] = file[column_name_wl].copy()
    file_i['flux'] = file[column_name_flux].copy()

    # choose the rows with the mask
    mask = (file_i['wl'] >= 6140) & (file_i['wl'] <= 6180)
    file_i = file_i[mask]

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
imageio.mimsave('time_evolution.gif', images, fps=2)
