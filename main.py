import os
import subprocess

while True:
    userInput = input("Enter a Youtube video URL (or type 'exit' to quit): ")

    if userInput.lower() == 'exit':
        print("\nExiting the program.\n")
        break

    print("\nstarting download...\n")
    initiateDownload = subprocess.run(["python", "audioDownloader.py", userInput])
    print("\n")

    print("moving file...\n")
    moveFile = subprocess.run(
        ["python", "fileMover.py"]
    )
    print("...file have been moved!\n")
