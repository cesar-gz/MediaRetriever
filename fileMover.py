import os
import shutil
import sharedVariables
from dotenv import load_dotenv
from difflib import get_close_matches

load_dotenv()
current_dir = os.getcwd()
target_dir = os.getenv("TARGET_DIRECTORY")
file_name = sharedVariables.get_video_title()

"""
if not file_name:
    print("Error: videoTitle.txt is empty. Make sure you've run the download script first.")
    exit(1)
"""

# Function to find the closest matching file
def find_closest_file(directory, target_name):
    files = os.listdir(directory)
    audio_files = [f for f in files if f.endswith(('.mp3', '.m4a', '.wav'))]
    matches = get_close_matches(target_name, audio_files, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Add file extension if it's not already there
if not file_name.lower().endswith(('.mp3', '.m4a', '.wav')):
    file_name += '.mp3'

# Find the closest matching file
closest_file = find_closest_file(current_dir, file_name)

if closest_file:
    source_file = os.path.join(current_dir, closest_file)
    destination_file = os.path.join(target_dir, file_name)

    # Check if destination directory exists, create if it doesn't
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Move the file
    try:
        shutil.move(source_file, destination_file)
        # successfully moved file
        print(f"Moved {closest_file} to {destination_file}")
    except PermissionError:
        print(f"Permission error: Unable to move {closest_file}. Make sure the file is not open in another program.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
#else:
#    print(f"Error: No matching audio file found for '{file_name}'.")

# Clear the video title after attempted move
sharedVariables.set_video_title("")
