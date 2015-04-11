#!/usr/bin/python

__author__ = 'Andy Hawkins'
__version__ = 0

print
"""
    __             __                   __
   |  |--.--------|  |--.-----.-----.--|  |
   |  _  |        |  _  |__ --|  _  |  _  |
   |_____|__|__|__|_____|_____|__   |_____|
   ----------------------------- |__| -----
   ANDY@BMBSQD.COM   -  WWW.BMBSQD.COM

"""

import cv2
import argparse
import PIL.Image
from PIL import ImageFilter

parser = argparse.ArgumentParser(description='Video Frames To Image Converter')
parser.add_argument('video', help='Source Video')
parser.add_argument('-o', '--output', help='Output Image', default='output.png')
parser.add_argument('-f', '--frames', type=int, help='Width Of Each Extracted Frame Size', default=1)
parser.add_argument('-s', '--smooth', help='Smooth Result Image', action="store_true")

args = parser.parse_args()

frameSize = args.frames

video = cv2.VideoCapture(args.video)

frames = []

success = True

n = 0
while success:
    success, image = video.read()
    if success: # and n % 100 == 0
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        frame = PIL.Image.fromarray(image)
        size = frameSize, frame.size[1]
        frame = frame.resize(size, PIL.Image.ANTIALIAS)
        frames.append(frame)
    n += 1
    print 'Frame #', n, "\r",

print "\nCreating Merge Image: ", (len(frames), frame.size[1])
merged = PIL.Image.new('RGBA', (len(frames)*frameSize, frame.size[1]))

n = 0
for frame in frames:
    # print (n, 0), frame
    merged.paste(frame, (n*frameSize, 0))
    n += 1
    print 'Processed Frame #', n, "\r",

print "\nDone"

if args.smooth:
    merged.filter(ImageFilter.SMOOTH_MORE)
merged.save(args.output,quality=100,compress_level=0)