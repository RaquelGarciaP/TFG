import pandas as pd

col1 = [1,2,3,4,5,6,7,8,9,10,11,12]
col2 = [6,8,10,12,13,14,15,19,20,22,23,25]
dic = {'col1': col1, 'col2': col2}
df = pd.DataFrame(dic)

mask = (df['col1'] >= 6) & (df['col1'] <= 9)
copi = df[mask]

print(df)
print(copi)





