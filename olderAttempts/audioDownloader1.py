import re
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress
import sys
import sharedVariables
import time

def clean_title(title):
    # Remove text in parentheses and brackets
    title = re.sub(r'\([^)]*\)', '', title)
    title = re.sub(r'\[[^]]*\]', '', title)

    # Remove common phrases
    phrases_to_remove = [
        "Official Video", "Official Music Video", "Official Audio",
        "Lyric Video", "Lyrics", "Audio", "HD", "HQ", "4K", "Club Mix",
        "Music Video", "Official Lyric Video", "[4K UPGRADE]", "AMV", "(from Kaiju No. 8)",
         "[Official HD Music Video]"
    ]
    for phrase in phrases_to_remove:
        title = title.replace(phrase, "")

    # Remove extra whitespace and trim
    title = re.sub(r'\s+', ' ', title).strip()

    # Capitalize first letter of each word
    title = title.title()

    return title

url = sys.argv[1]

yt = YouTube(url, on_progress_callback = on_progress, use_po_token=True)

original_title = str(yt.title)
cleaned_title = clean_title(original_title)

print(f"{cleaned_title}")

sharedVariables.set_video_title(cleaned_title)

ys = yt.streams.get_audio_only()
download_path = os.getcwd()
downloaded_file = ys.download(output_path=download_path, mp3=True)

# Rename the file
file_extension = os.path.splitext(downloaded_file)[1]
new_filename = f"{cleaned_title}{file_extension}"
new_filepath = os.path.join(download_path, new_filename)

try:
    os.rename(downloaded_file, new_filepath)
    # File was successfully renamed
    time.sleep(0.5)
    print("\nDownload Finished.\n")
except Exception as e:
    print(f"Error renaming file: {e}")
    new_filepath = downloaded_file  # If renaming fails, use the original filename
