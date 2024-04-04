import os


from helper import video_to_images

video_path = "videos/a.mp4"  # Replace with your actual video path
output_dir = "extracted_frames"
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

video_to_images(video_path,output_dir)
