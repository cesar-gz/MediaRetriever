import yt_dlp
import os
import sys
import re
import sharedVariables

def clean_title(title):
    # Remove text in parentheses and brackets
    title = re.sub(r'\([^)]*\)', '', title)
    title = re.sub(r'\[[^]]*\]', '', title)

    # Remove common phrases
    phrases_to_remove = [
        "Official Video", "Official Music Video", "Official Audio", "AMV", "Amv",
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



# video_url = "https://www.youtube.com/watch?v=dZDa2u4Hor8"

video_url = sys.argv[1]

output_directory = '.'

temp_filename_pattern = os.path.join(output_directory, '%(title)s_temp.%(ext)s')

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': temp_filename_pattern,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
    'no_warnings': True,
}



try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 1. Download the file with a temporary name (e.g., 'VideoTitle_temp.mp3')
        info = ydl.extract_info(video_url, download=True)

        # 2. Get the file's current path and the video's original title
        original_title = info.get('title', 'unknown')

        # After post-processing, the file path is usually stored in the
        # 'requested_downloads' list. We take the path from the first item.
        current_filepath = None
        if info.get('requested_downloads'):
            # This is the path after MP3 conversion is complete
            current_filepath = info['requested_downloads'][0]['filepath']

        if not current_filepath:
            raise Exception("yt-dlp failed to return a valid file path.")

        # 3. Apply your custom cleaning function
        cleaned_title = clean_title(original_title)

        # 4. Construct the new file path
        base_dir = os.path.dirname(current_filepath)
        new_filepath = os.path.join(base_dir, f"{cleaned_title}.mp3")

        # 5. Rename the file
        # We need to ensure the final file is actually the .mp3 file before renaming
        # The 'current_filepath' should already be the .mp3 due to the postprocessor,
        # but we add an extra check just in case.
        if os.path.exists(current_filepath):
             os.rename(current_filepath, new_filepath)
             print(f"Download complete and renamed to: {cleaned_title}.mp3")
        else:
            print(f"Error: Temporary file not found at {current_filepath}")


except Exception as e:
    print(f"An error occurred: {e}")
