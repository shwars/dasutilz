# This utility assumes the following data structure: ./category/file.ext with several categories
# It will split files intro train and test set and create the bat file to copy all files into target directory
# under train and val subfolders.

dest_dir = 'data'
src_dir = '.'
split = 0.2

from os import listdir
from os.path import join,isdir,isfile
from glob import glob
import random

result = []
mk = []

for cat in listdir(src_dir):
    if isdir(join(src_dir,cat)):
        print("Processing category {}".format(cat))
        mk.append(cat)
        for f in listdir(join(src_dir,cat)):
            if isfile(join(src_dir,cat,f)):
                result.append((join(cat,f),"val" if random.random()<split else "train"))

print("Writing copy.bat...")
with open('copy.bat','w') as f:
    f.write("set DRV=D:\n")
    for fn in mk:
        for cat in ["train","val"]:
            f.write("MKDIR %DRV%\\{0}\\{1}\\{2}\n".format(dest_dir,cat,fn))
    for fn,c in result:
        f.write("COPY {0} %DRV%\\{1}\\{2}\\{0}\n".format(fn,dest_dir,c))