import os
import shutil
import sharedVariables
from dotenv import load_dotenv

load_dotenv()
current_dir = os.getcwd()
target_dir = os.getenv("TARGET_DIRECTORY")
file_name = sharedVariables.get_video_title()


# Ensure file_name is not empty
if not file_name:
    print("Error: videoTitle.txt is empty. Make sure you've run the download script first.")
    exit(1)

# Add .mp3 extension if it's not already there
if not file_name.endswith('.mp3'):
    file_name += '.mp3'

# Create the full path for the source file
source_file = os.path.join(current_dir, file_name)

# Create the full path for the destination file
destination_file = os.path.join(target_dir, file_name)

# Check if source file exists
if not os.path.exists(source_file):
    print(f"Error: Source file '{source_file}' does not exist.")
    exit(1)

# Check if destination directory exists, create if it doesn't
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Move the file
try:
    shutil.move(source_file, destination_file)
    print(f"Moved {file_name} from {current_dir} to {target_dir}")
except PermissionError:
    print(f"Permission error: Unable to move {file_name}. Make sure the file is not open in another program.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Clear the video title after successful move
sharedVariables.set_video_title("")
