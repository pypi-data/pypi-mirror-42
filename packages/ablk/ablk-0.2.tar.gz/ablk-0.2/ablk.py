#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import shutil
import time

import PIL.Image
import PIL.ExifTags


def display(path,showFileName=False):
    dim = shutil.get_terminal_size(fallback=(80,24))

    try:
        img = PIL.Image.open(path)
    except:
        return

    try:
        info = img._getexif()
        for tag,value in info.items():
            decoded = PIL.ExifTags.TAGS.get(tag)
            if decoded != 'Orientation':
                continue
            if value == 8: # counter clockwise
                img = img.rotate(90, expand=1)
            elif value == 6: # clock wise
                img = img.rotate(-90, expand=1)
            elif value == 3: # 180
                img = img.rotate(180)
            break
    except AttributeError as e:
        pass

    iw,ih = img.size
    tw,th = dim.columns,dim.lines
    th -= 1 if not showFileName else 2
    th = th * 2
    ir = iw / ih
    tr = tw / th

    if ir > tr:
        cols = tw
        rows = int(cols * (ih / iw))
    else:
        rows = th
        cols = int(rows * (iw / ih))

    if rows & 1:
        rows += 1

    img = img.resize((cols, rows))
    img = img.convert('RGB')

    if showFileName:
        sys.stdout.write('\033[1;44m'+' ' * cols + '\r')
        sys.stdout.write('\033[1;37m '+path+'\033[0m\n')

    for row in range(0,rows,2):
        for col in range(cols):
            p1 = img.getpixel((col, row + 0))
            p2 = img.getpixel((col, row + 1))
            values = (p1[0],p1[1],p1[2],p2[0],p2[1],p2[1])
            sys.stdout.write('\033[38;2;%d;%d;%dm\033[48;2;%d;%d;%dm▀' % values)

        sys.stdout.write('\033[0m\n')


def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('images',
        nargs='+', default=None,
        help='Image files')

    argparser.add_argument('--delay', '-d',
        type=float, default=1.0,
        help='Delay between each image')

    argparser.add_argument('--no-name', '-n',
        action='store_false',
        help='Show filename of image')

    args = argparser.parse_args()

    try:
        totalLength = len(args.images)
        for index in range(totalLength):
            display(args.images[index], args.no_name)
            if index + 1 < totalLength:
                time.sleep(args.delay)
    except KeyboardInterrupt:
        sys.stdout.write('\033[0m\n')


if '__main__' == __name__:
    main()
