import subprocess
import re
import os

import cv2

from skimage.metrics import structural_similarity as ssim

def video_to_images(video_path,
			output_dir,
			similarity_threshold=0.9,
			image_per_second=1.0
			):


	cap = cv2.VideoCapture(video_path)

	if not cap.isOpened():
		print("Error opening video file!")
		exit()

	fps = cap.get(cv2.CAP_PROP_FPS)
	fps = int(fps)
	image_fps = int(fps * image_per_second)
	print("fps",fps)
	print(f"every {image_fps} frames one image will be used")
	print(f"every {image_per_second} seconds,  one image will be used")

	previously_saved_image = None
	saved_image_number = 0
	while True:
		ret, frame = cap.read()

		if not ret:
			break  # Reached the end of the video

		frame_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Time in seconds (optional)
		frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1  # Adjust for 0-based indexing
		frame_number = int(frame_number)
		if frame_number % image_fps > 0:
			continue
		seconds = frame_number // fps
		minutes = seconds // 60			
		similarity = image_compare_structural_similarity(previously_saved_image,frame)
		if similarity > similarity_threshold:
			print("skipping saving image,similarity is high, frame_number:",frame_number,", seconds:",seconds,",minutes:",minutes," saved"," similarity",similarity)
			continue



		filename = f"{output_dir}/{saved_image_number:05d}.png"  # Pad with zeros
		cv2.imwrite(filename, frame)
		previously_saved_image = frame
		saved_image_number = saved_image_number +1
		print("frame_number:",frame_number,", seconds:",seconds,",minutes:",minutes," saved"," similarity",similarity)

	cap.release()
	cv2.destroyAllWindows()





def compare_histograms(image1, image2):
	"""Compares histograms of two images and returns a similarity score."""
	if image1 is None or image2 is None:
		return -1
	hist1 = cv2.calcHist([image1], [0], None, [256], [0, 256])
	hist2 = cv2.calcHist([image2], [0], None, [256], [0, 256])
	return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)  # Chi-squared metric

def image_compare_structural_similarity(image1,image2):
	if image1 is None or image2 is None:
		return -1
	image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
	image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

	# Calculate and print SSIM score
	ssim_value = ssim(image1_gray, image2_gray)
	return ssim_value



def get_video_id(url):
	video_id_match = re.search(r"v=([^&]+)", url)
	if not video_id_match:
		raise ValueError("Failed to extract video ID from URL")
	video_id = video_id_match.group(1)
	return video_id


def download_youtube_subtitle(youtube_url,
		language = "en",
		 output_dir="videos"):
	video_id = get_video_id(youtube_url)

	# Construct a unique filename with video ID and extension
	output_filename = f"{output_dir}/{video_id}"

	youtube_dl_cmd = ["yt-dlp",
						"--skip-download",
						"--write-auto-sub",
						"--sub-format", "srt",
						"--sub-langs", language,
						"-o", output_filename,
				 youtube_url]
	try:
		process = subprocess.run(youtube_dl_cmd, check=True)

	except subprocess.CalledProcessError as e:
		raise RuntimeError(f"youtube-dl download failed: {e.output}") from e
	return output_filename + f".{language}.vtt"

from os.path import exists

def filename_from_youtube_url(youtube_url,output_dir="videos"):
	video_id = get_video_id(youtube_url)

	# Construct a unique filename with video ID and extension
	output_filename = f"{output_dir}/{video_id}.mp4"
	return output_filename

def video_already_downloaded(youtube_url,output_dir="videos"):
	output_filename = filename_from_youtube_url(youtube_url,output_dir)
	file_exists = exists(output_filename)
	return file_exists


def download_youtube_video(youtube_url,
		 output_dir="videos"):
	"""Downloads a YouTube video using yt-dlp (youtube-dl fork) and saves it with a unique filename.

	Args:
			url (str): The URL of the YouTube video to download.
			output_dir (str, optional): The directory to save the downloaded video.
					Defaults to "." (current directory).

	Returns:
			str: The path to the downloaded video file.

	Raises:
			RuntimeError: If the download process fails.
	"""

	output_filename = filename_from_youtube_url(youtube_url,output_dir)


	# Build the youtube-dl command with options for format selection and output filename
	youtube_dl_cmd = ["yt-dlp",
					 "--format", "bv",  # best video
					 "-o", output_filename,  # Specify output filename template
					 youtube_url]

	try:
		process = subprocess.run(youtube_dl_cmd, check=True)
	except subprocess.CalledProcessError as e:
		raise RuntimeError("youtube-dl download failed")

	return output_filename
