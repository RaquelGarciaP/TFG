import os

directory = 'params'  # name of the directory
parent_dir = './CombinedSpectra/'  # parent directory path
path = os.path.join(parent_dir, directory)  # path

for i in range(10):
    file_name = 'time_' + str(i)
    print(file_name)




