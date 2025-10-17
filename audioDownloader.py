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



# video_url = "https://www.youtube.com/watch?v=dZDa2u4Hor8"

try:
    video_url = sys.argv[1]
except IndexError:
    print("Error: Please provide a YouTube URL as a command-line argument.")
    sys.exit(1)

output_directory = '.'

temp_filename_pattern = os.path.join(output_directory, '%(title)s_temp.%(ext)s')

temp_output_extension = 'mp3' # Define the output extension for clarity

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': temp_filename_pattern,
    'writethumbnail': True,  # 1. Tell yt-dlp to download the thumbnail

    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
        {
            'key': 'EmbedThumbnail',  # 2. Embed the downloaded thumbnail into the MP3
            'already_have_thumbnail': False
        },
    ],
    'quiet': True,
    'no_warnings': True,
}



try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 1. Download and Process the file (including thumbnail embedding)
        info = ydl.extract_info(video_url, download=True)

        # 2. Get the file's current path and the video's original title
        original_title = info.get('title', 'unknown')

        # Robustly get the final file path after all post-processing
        current_filepath = None
        if info.get('requested_downloads'):
            # This is the path after MP3 conversion is complete
            current_filepath = info['requested_downloads'][0]['filepath']

        if not current_filepath:
            raise Exception("yt-dlp failed to return a valid file path for renaming.")

        # 3. Apply your custom cleaning function
        cleaned_title = clean_title(original_title)

        # 4. Construct the new file path
        base_dir = os.path.dirname(current_filepath)
        new_filepath = os.path.join(base_dir, f"{cleaned_title}.{temp_output_extension}")

        # 5. Rename the file and clean up temporary thumbnail files
        if os.path.exists(current_filepath):
             os.rename(current_filepath, new_filepath)

             # 6. Clean up the temporary thumbnail file (e.g., 'VideoTitle_temp.webp')
             temp_thumb_path = os.path.splitext(current_filepath)[0] + '.webp'
             if os.path.exists(temp_thumb_path):
                 os.remove(temp_thumb_path)

             print(f"Download complete, renamed, and album art embedded: {cleaned_title}.{temp_output_extension}")
        else:
            print(f"Error: Final file not found at {current_filepath}")

except Exception as e:
    print(f"An error occurred: {e}")
