import yt_dlp
import os
import sys
import re
import sharedVariables
from dotenv import load_dotenv
from yt_dlp.utils import sanitize_filename

def clean_title(title):
    # Remove text in parentheses and brackets
    title = re.sub(r'\([^)]*\)', '', title)
    title = re.sub(r'\[[^]]*\]', '', title)

    # Remove common phrases
    phrases_to_remove = [
        "Official Video", "Official Music Video", "Official Audio",
        "Lyric Video", "Lyrics", "Audio", "HD", "HQ", "4K", "Club Mix",
        "Music Video", "Official Lyric Video", "[4K UPGRADE]", "[Official HD Music Video]"
    ]
    for phrase in phrases_to_remove:
        title = title.replace(phrase, "")

    # Remove extra whitespace and trim
    title = re.sub(r'\s+', ' ', title).strip()

    # Capitalize first letter of each word
    title = title.title()
    sharedVariables.set_video_title(title)

    return title

try:
    video_url = sys.argv[1]
except IndexError:
    print("Error: Please provide a YouTube URL as a command-line argument.")
    sys.exit(1)

load_dotenv()
TARGET_DIRECTORY = os.getenv("TARGET_DIRECTORY")
if TARGET_DIRECTORY is None:
    raise RuntimeError("TARGET_DIRECTORY is not set (check your .env file).")
output_directory = TARGET_DIRECTORY

temp_filename_pattern = os.path.join(output_directory, '%(title)s_temp.%(ext)s')
temp_output_extension = 'mp3'

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': temp_filename_pattern,
    'writethumbnail': True,
    'extractor_args': {
        'youtube': {
            'player_client': ['ios', 'android', 'web'],
            'skip': ['hls', 'dash']
        }
    },
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
        {
            'key': 'EmbedThumbnail',
            'already_have_thumbnail': False
        },
    ],
    #'verbose': True
    'quiet': False,
    'no_warnings': True,
    "progress_with_newline": False,
    "noprogress": False,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Download, Process the file and thumbnail
        info = ydl.extract_info(video_url, download=True)

        # Get the file's current path and the video's original title
        original_title = info.get('title', 'unknown')

        # Get the final file path after all post-processing
        current_filepath = None
        if info.get('requested_downloads'):
            current_filepath = info['requested_downloads'][0]['filepath']

        if not current_filepath:
            raise Exception("yt-dlp failed to return a valid file path for renaming.")

        # Apply custom cleaning function
        cleaned_title = clean_title(original_title)
        safe_title = sanitize_filename(cleaned_title, restricted=False)

        # Construct the new file path
        base_dir = os.path.dirname(current_filepath)
        new_filepath = os.path.join(base_dir, f"{safe_title}.{temp_output_extension}")
        os.replace(current_filepath, new_filepath)


        # Rename the file and clean up temporary thumbnail files
        if os.path.exists(current_filepath):
             os.rename(current_filepath, new_filepath)

            # Clean up the temporary thumbnail file (e.g., 'VideoTitle_temp.webp')
             temp_thumb_path = os.path.splitext(current_filepath)[0] + '.webp'
             if os.path.exists(temp_thumb_path):
                 os.remove(temp_thumb_path)

             print(f"Download complete, renamed, and album art embedded: {cleaned_title}.{temp_output_extension}")
        #else:
        #    print(f"Error: Final file not found at {current_filepath}")

except Exception as e:
    print(f"An error occurred: {e}")
