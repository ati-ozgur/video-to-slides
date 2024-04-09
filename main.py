import argparse


from helper import * 


if __name__ == "__main__":


	parser = argparse.ArgumentParser()
	parser.add_argument('url',help='youtube url to download')   # positional argument
	parser.add_argument('-odv', '--output_directory_video',default='videos',help='output directory to save downloaded video')
	parser.add_argument('-ode', '--output_directory_extracted',default='extracted_frames',help='output directory to save png images files extracted from video')
	parser.add_argument('-st', '--similarity_threshold',type=float,default='0.8',help='similarity value to check, default 0.8')



	args = parser.parse_args()

	downloaded_video_path = download_youtube_video(args.url,
			args.output_directory_video)
	print(f"Video downloaded to: {downloaded_video_path}")

	video_to_images(downloaded_video_path
		,args.output_directory_extracted
		,args.similarity_threshold)
