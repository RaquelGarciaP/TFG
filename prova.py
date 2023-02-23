import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(1.0,20.0, num=100)
print(x)
min = x[0]
max = x[-1]
mu = min + (max - min) / float(2)

sigma = 0.85

gaussian = [0.0 for i in x]
gauss_norm = [0.0 for i in x]

for i in range(len(x)):
    gaussian[i] = np.exp(-((float(x[i]) - mu) / float(sigma)) ** 2 / float(2))
    gauss_norm[i] = (1.0 / (math.sqrt(2.0 * math.pi) * sigma)) * np.exp(-((float(x[i]) - mu) / float(sigma)) ** 2 / float(2))

area1 = 0.0
for i in range(len(x)):
    area1 += 0.19191919 * gaussian[i]

area2 = 0.0
for i in range(len(x)):
    area2 += 0.19191919 * gauss_norm[i]

print(area1, area2)

plt.plot(x, gaussian)
plt.plot(x, gauss_norm)
plt.show()





