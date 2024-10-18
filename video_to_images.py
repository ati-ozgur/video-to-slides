import os
import argparse

from helper import video_to_images


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('video_filename',help='video filename to load')   # positional argument
	parser.add_argument('-o', '--output_directory',default='extracted_frames',help='output directory to save png images files extracted from video')
	parser.add_argument('-st', '--similarity_threshold',type=float,default='0.9',help='similarity value to check, default 0.9')
	parser.add_argument('-ifps', '--image_per_second',type=float,default='1.0',help='0.5 for 2 images per second, 2 for 1 image per 2 second, 0.1, 1 image per second')



	args = parser.parse_args()
	video_to_images(args.video_filename
		,args.output_directory
		,args.similarity_threshold
		,args.image_per_second)
