import cv2
from skimage.metrics import structural_similarity as ssim

def video_to_images(video_path,output_dir):


	cap = cv2.VideoCapture(video_path)

	if not cap.isOpened():
		print("Error opening video file!")
		exit()

	previously_saved_image = None
	while True:
		ret, frame = cap.read()

		if not ret:
			break  # Reached the end of the video

		frame_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Time in seconds (optional)
		frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1  # Adjust for 0-based indexing
		frame_number = int(frame_number)
		if frame_number % 1000 > 0:
			continue
		filename = f"{output_dir}/frame_{frame_number:05d}.png"  # Pad with zeros

		similarity = image_compare_structural_similarity(previously_saved_image,frame)
		if similarity > 0.9:
			print("skipping saving image,similarity is high",similarity,"frame_number",frame_number)
			continue

		cv2.imwrite(filename, frame)
		previously_saved_image = frame
		seconds = frame_number // 1000
		minutes = seconds // 60
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