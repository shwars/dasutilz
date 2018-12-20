
# This file will convert PASCAL VOC representation into CSV file with bounding boxes

import mPyPl as mp
import argparse
import os
from pipe import *

parser = argparse.ArgumentParser()

parser.add_argument("--source", help="source directory with PASCAL VOC tree")
parser.add_argument("--dest", help="target CSV file name")

args = parser.parse_args()

base_dir = args.source or os.getcwd()
dest = args.dest or "images.csv"

@Pipe
def apply_many(l,field_name,func):
    for x in l:
        res = mp.core.__fnapply(x,field_name,func)
        for z in res:
            yield z

def processor(args):
    fn,obj = args
    for x in obj:
        yield [fn,x.as_int('bndbox_xmin'),x.as_int('bndbox_ymin'),x.as_int('bndbox_xmax'),x.as_int('bndbox_ymax'),x['name']]

data = (mp.get_pascal_annotations(os.path.join(base_dir,'Annotations'))
       |apply_many(['filename','object'],processor)
       |mp.write_csv(dest))
