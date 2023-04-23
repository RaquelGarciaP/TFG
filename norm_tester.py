import pandas as pd
import numpy as np

# Crea un DataFrame de ejemplo
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})

print(df)

# Crea un vector de ejemplo
arr = np.array([2, 3, 4])

# Divide la columna 'A' de df por el vector arr
df['A'] = df['A'].div(arr)

print(df)
