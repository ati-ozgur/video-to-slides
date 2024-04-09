import subprocess
import re

import argparse

from helper import download_youtube_video



# Example usage
if __name__ == "__main__":


	parser = argparse.ArgumentParser()
	parser.add_argument('url',help='youtube url to download')   # positional argument
	parser.add_argument('-o', '--output_directory',default='videos',help='output directory to save downloaded video')



	args = parser.parse_args()

	downloaded_video_path = download_youtube_video(args.url,args.output_directory)
	print(f"Video downloaded to: {downloaded_video_path}")


