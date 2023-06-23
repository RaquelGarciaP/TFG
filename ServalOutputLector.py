import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


'''dic = {'columna1': [2,4,5], 'columna2': [3,6,7]}
df = pd.DataFrame(dic)

print(df)

llista = [[2,4,5], [3,6,7]]
df2 = pd.DataFrame(llista)

print(df2[0])'''

# ************************* 12 files *************************
head = ['BJD', 'RVC', 'E_RVC', 'DRIFT', 'E_DRIFT', 'RV', 'E_RV', 'BERV', 'SADRIFT']

# read files
rv1 = np.load('./CombinedSpectra/rv1_binary_v1.npy')
rv2 = np.load('./CombinedSpectra/rv2_binary_v1.npy')

serval_output = pd.read_csv('./SERVAL/J18356+329_binary_v1/J18356+329_binary_v1.rvc.dat', names=head, delimiter=' ')

CARMENES_info = pd.read_csv('./CARMENES_data/info_observations.csv')
t = CARMENES_info['BJD'].to_numpy()

# final_rv = rv1 #- (rv1[0] - serval_output['RV'][0])
total_rv = (rv1 + 0.796068465 * rv2) / (1 + 0.796068465)  # mean_rv = (k1 - L2/L1 * k2)/(1+ L2/L1)
new_rv = total_rv - (total_rv[0] - serval_output['RV'][0])


# calculate the difference between original RVs and SERVAL RV output
difference_rv = total_rv - serval_output['RV']

difference_rv2 = []

for i in range(len(t)):
    difference_rv2.append(new_rv[i] - serval_output['RV'][i])

print('max difference: ', np.max(np.absolute(difference_rv2)))
print('max radial velocity value: ', np.max(np.absolute(new_rv)))

plt.plot(t, difference_rv2)  # serval_output['BJD'], difference_rv)
plt.show()

'''new_rv = - rv1 - (-rv1[0] - serval_output['RV'][0])
print(rv1)
print(new_rv)'''

fig, ax = plt.subplots()

l1, = ax.plot(t, new_rv)  # serval_output['BJD'], rv1)
l2, = ax.plot(t, serval_output['RV'])  # serval_output['BJD'], serval_output['RV'])

ax.legend((l1, l2), ('original rv', 'serval'), loc='upper right', shadow=False)
ax.set_xlabel('Time (BJD)')
ax.set_ylabel('RV')
ax.set_title('original RV vs serval RV')
plt.show()


# ************************* all files *************************
'''head = ['BJD', 'RVC', 'E_RVC', 'DRIFT', 'E_DRIFT', 'RV', 'E_RV', 'BERV', 'SADRIFT']

# read files
rv1 = np.load('./CombinedSpectra/rv1_noDoppler.npy')
serval_output = pd.read_csv('./SERVAL/J18356+329_no_R2_SNR_with_BarCor_broadening/J18356+329_no_R2_SNR_with_BarCor_broadening.rvc.dat', names=head, delimiter=' ')

# mask = np.ones(len(rv1), dtype=bool)
# mask[8] = False
# rv1 = rv1[mask, ...]

# calculate the difference between original RVs and SERVAL RV output
difference_rv = abs(abs(rv1)-abs(serval_output['RVC']))
plt.plot(serval_output['BJD'], difference_rv, 'o')
plt.show()


fig, ax = plt.subplots()

l1, = ax.plot(serval_output['BJD'], rv1, 'o')
l2, = ax.plot(serval_output['BJD'], serval_output['RVC'], 'o')

ax.legend((l1, l2), ('original', 'serval'), loc='upper right', shadow=False)
ax.set_xlabel('Time (BJD)')
ax.set_ylabel('RV')
ax.set_title('original RV vs serval RV')
plt.show()
'''

# ************************* rvo *************************
'''head2 = ['BJD', 'RV', 'E_RV', 'RVMED', 'E_RVMED', 'RVO_00', 'RVO_01', 'RVO_02']

# read files
rv1 = np.load('./CombinedSpectra/rv1_noDoppler.npy')
serval_output = pd.read_csv('./SERVAL/J18356+329_Riszero_SNRzero/J18356+329_Riszero_SNRzero.rvo.dat', delimiter=' ')

print(serval_output)

# calculate the difference between original RVs and SERVAL RV output
difference_rv = abs(abs(rv1)-abs(serval_output[1]))
plt.plot(serval_output[0], difference_rv, 'o')
plt.show()


fig, ax = plt.subplots()

l1, = ax.plot(serval_output[0], rv1, 'o')
l2, = ax.plot(serval_output[0], serval_output[1], 'o')

ax.legend((l1, l2), ('original', 'serval'), loc='upper right', shadow=False)
ax.set_xlabel('Time (BJD)')
ax.set_ylabel('RV')
ax.set_title('original RV vs serval RV')
plt.show()'''

# ************************* antic *************************
'''head = ['BJD', 'RVC', 'E_RVC', 'DRIFT', 'E_DRIFT', 'RV', 'E_RV', 'BERV', 'SADRIFT']
df = pd.read_csv('D:/raquel/Desktop/UNI/5e/TFG/observacions CARMENES/dates de mesura de CARMENES/J18356+329.rvc.csv', names=head)

# print(df['RVC'].mean())
# print(df['RV'].mean())

df2 = pd.read_csv('D:/raquel/Desktop/UNI/5e/TFG/GitHub/SERVAL/fet igual que el mathias/J18356+329.rvc.csv', names=head)


print(len(df), len(df2))
# plt.plot(df['BJD'], df['RVC'], 'o')
# plt.show()

fig, ax = plt.subplots()

l1, = ax.plot(df['BJD'], df['RVC'], 'o')
l2, = ax.plot(df2['BJD'], df2['RVC'], 'o')

ax.legend((l1, l2), ('Mathias', 'Jo'), loc='upper right', shadow=False)
ax.set_xlabel('Time')
ax.set_ylabel('RV')
ax.set_title('serval')
plt.show()'''

