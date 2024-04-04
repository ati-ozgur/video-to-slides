import os
import argparse

from helper import video_to_images

parser = argparse.ArgumentParser()
parser.add_argument('video_filename')   # positional argument
parser.add_argument('-o', '--output_directory',default='extracted_frames')



args = parser.parse_args()
video_to_images(args.video_filename,args.output_directory)
