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
rv1 = np.load('./CombinedSpectra/rv1_noDoppler.npy')
serval_output = pd.read_csv('./SERVAL/J18356+329_prova1_reduced3/J18356+329_prova1_reduced3.rvc.dat', names=head, delimiter=' ')

mask = np.zeros(len(rv1), dtype=bool)
# print(mask)
mask[[34, 35, 36, 38, 39, 40, 41, 42, 44, 46, 48, 50, 51, 52, 53]] = True
# print(mask)
rv1_masked = rv1[mask, ...]

# calculate the difference between original RVs and SERVAL RV output
difference_rv = abs(abs(rv1_masked)-abs(serval_output['RVC']))
plt.plot(serval_output['BJD'], difference_rv)
plt.show()


fig, ax = plt.subplots()

l1, = ax.plot(serval_output['BJD'], rv1_masked)
l2, = ax.plot(serval_output['BJD'], serval_output['RVC'])

ax.legend((l1, l2), ('original', 'serval'), loc='upper right', shadow=False)
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

