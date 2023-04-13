from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from ContinuumNormalization import ContinuumNormalization

# Create a sample DataFrame
df = pd.DataFrame({
    'A': [10, 20, 30, 40],
    'B': [5, 15, 25, 35],
    'C': [1, 2, 3, 4]
})

# Create a MinMaxScaler object
scaler = MinMaxScaler()

# Normalize the DataFrame
df_normalized = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

# Print the normalized DataFrame
print(df_normalized)


'''df = pd.read_csv('./CombinedSpectra/test_file.csv')
df_time0 = pd.DataFrame()
df_time0['wl'] = df['wl_time_0'].copy()
df_time0['flux'] = df['flux_time_0'].copy()

test = ContinuumNormalization(df_time0)
'''

