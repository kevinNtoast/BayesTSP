import os
import glob
import pandas as pd
os.chdir("C:/Users/Toast/Dropbox/PhD/psych234/optimal/solution")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{} '.format(extension))]

for i in range(9):
    for j in range(30):
        all_filenames = [k for k in glob.glob('*prob{prob}*.{ext}'.format(prob = i, ext = extension))]
    print(all_filenames)
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], axis = 1)
    combined_csv.to_csv( "solution{num}.csv".format(num=i), index=False, encoding='utf-8-sig')
    print(i)
# print(all_filenames)
all_filenames2 = [k for k in glob.glob('*solution*.{ext}'.format(ext = extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames2], axis = 0)
combined_csv.to_csv("solutioncomplete.csv".format(num=i), index=False, encoding='utf-8-sig')
#combine all files in the list
# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# #export to csv
