import subprocess
import re

def get_video_id(url):
	video_id_match = re.search(r"v=([^&]+)", url)
	if not video_id_match:
		raise ValueError("Failed to extract video ID from URL")
	video_id = video_id_match.group(1)
	return video_id



def download_youtube_video(url, output_dir="videos"):
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

  # Extract the unique YouTube video ID from the URL
  video_id = get_video_id(youtube_url)

  # Construct a unique filename with video ID and extension
  output_filename = f"{output_dir}/{video_id}.%(ext)s"

  # Build the youtube-dl command with options for format selection and output filename
  youtube_dl_cmd = ["yt-dlp",
                     "-f", "best",  # Download the best available format
                     "-o", output_filename,  # Specify output filename template
                     url]

  # Execute the youtube-dl command
  try:
    process = subprocess.run(youtube_dl_cmd, check=True, capture_output=True)
  except subprocess.CalledProcessError as e:
    raise RuntimeError(f"youtube-dl download failed: {e.output}") from e

  # Return the path to the downloaded video
  return output_filename




# Example usage
if __name__ == "__main__":
	youtube_url = "https://www.youtube.com/watch?v=DG1ujHRWafM"
	video_id = get_video_id(youtube_url)
	print("video_id",video_id)

	downloaded_video_path = download_youtube_video(youtube_url)
	print(f"Video downloaded to: {downloaded_video_path}")
