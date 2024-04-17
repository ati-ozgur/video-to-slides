import argparse


from helper import * 
from clean_subtitles import write_cleaned_subtitle

if __name__ == "__main__":


	parser = argparse.ArgumentParser()
	parser.add_argument('url',help='youtube url to download')   # positional argument
	parser.add_argument('-odv', '--output_directory_video',default='videos',help='output directory to save downloaded video')
	parser.add_argument('-ode', '--output_directory_extracted',default='extracted_frames',help='output directory to save png images files extracted from video')
	parser.add_argument('-st', '--similarity_threshold',type=float,default='0.8',help='similarity value to check, default 0.8')
	parser.add_argument('-sub', '--subtitle_download',type=bool,default=False,help='Download and clean subtitles')
	parser.add_argument('-lang', '--language',type=str,default="en",help='if download subtitle False, ignored, otherwise language of the subtitle')
	parser.add_argument('-novid', '--no_video_download',type=bool,default=False,help='Do not download video and extract slides')



	args = parser.parse_args()

	if args.subtitle_download:
		subtitle_filename = download_youtube_subtitle(args.url,
					args.language,
					args.output_directory_video)
		write_cleaned_subtitle(subtitle_filename)

	if not args.no_video_download:
		downloaded_video_path = download_youtube_video(args.url,
				args.output_directory_video)
		print(f"Video downloaded to: {downloaded_video_path}")



		video_to_images(downloaded_video_path
			,args.output_directory_extracted
			,args.similarity_threshold)
	else:
		print("skipping downloading video and extracting slides")