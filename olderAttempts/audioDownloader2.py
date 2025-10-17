import yt_dlp
import os

# 1. The full URL works fine with yt-dlp!
video_url = "https://www.youtube.com/watch?v=dZDa2u4Hor8"
# You can even use the original complex URL if you want.

# Define the directory where the file will be saved
output_directory = '.'

# Define options to download ONLY the best quality audio and convert it to MP3
ydl_opts = {
    'format': 'bestaudio/best',  # Download the best audio format
    'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'), # Output file path/name
    'postprocessors': [{  # Post-processing settings
        'key': 'FFmpegExtractAudio', # Extract audio using FFmpeg
        'preferredcodec': 'mp3',     # Convert to MP3
        'preferredquality': '192',   # Bitrate (e.g., 192kbps)
    }],
    # Suppress verbose output
    'quiet': True,
    'no_warnings': True,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        # Get the final filename for the success message
        title = info.get('title', 'Unknown')
        print(f"Download complete: {title}.mp3")

except Exception as e:
    print(f"An error occurred: {e}")
