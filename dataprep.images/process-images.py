import PIL
from PIL import Image
from PIL import ImageFilter

import argparse
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument("--blur", help="apply blur filter", action="store_true")
parser.add_argument("--box-blur", help="apply box blur filter with given size", type=int)
parser.add_argument("--gaussian-blur", help="apply gaussian blur filter with given size", type=int)
parser.add_argument("--smooth", help="apply smoothing filter", action="store_true")
parser.add_argument("--smooth-more", help="apply extra smoothing filter", action="store_true")
parser.add_argument("--downsize", help="downsize the image with the given scale, eg. 1.5, 2.0, etc.", type=float)
parser.add_argument("--include", help="include only files with a given string in the filename")
parser.add_argument("--exclude", help="exclude files with a given string in the filename")
parser.add_argument("--dir", help="directory to process, defaults to current directory")
parser.add_argument("--dst", help="destination directory, if not specified: files are overwritten")
parser.add_argument("--verbose", help="print filenames as they are processed",action='store_true')
parser.add_argument("--no",help="number of images to process. useful for debugging",type=int)
parser.add_argument("--renumber", help="name output image files in numerical fashion (1,2,etc)",action='store_true')

args = parser.parse_args()

dir = args.dir if args.dir else os.getcwd()
dst = args.dst if args.dst else dir

i=0
for fn in os.listdir(dir):
    if args.no and i>args.no-1:
        break
    if args.include and not args.include in fn:
        continue
    if args.exclude and args.exclude in fn:
        continue
    i+=1
    img = Image.open(os.path.join(dir,fn))
    if args.verbose:
        print(" - Processing {}, size ({}x{})".format(fn,img.width,img.height))

    if args.blur:
        img = img.filter(ImageFilter.BLUR)
    if args.smooth:
        img = img.filter(ImageFilter.SMOOTH)
    if args.smooth:
        img = img.filter(ImageFilter.SMOOTH_MORE)
    if args.box_blur:
        img = img.filter(ImageFilter.BoxBlur(args.box_blur))
    if args.gaussian_blur:
        img = img.filter(ImageFilter.GaussianBlur(args.gaussian_blur))

    if args.downsize:
        w = int(img.width/args.downsize)
        h = int(img.height/args.downsize)
        img = img.resize((w,h),PIL.Image.LANCZOS)

    fnx = os.path.splitext(fn)
    ofn = str(i)+fnx[1] if args.renumber else fn
    img.save(os.path.join(dst,ofn))
