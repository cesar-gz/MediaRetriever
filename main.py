import subprocess

while True:
    userInput = input("\nEnter a Youtube video URL (or type 'exit' to quit): ")

    if userInput.lower() == 'exit':
        print("\nExiting the program.\n")
        break

    print("\nstarting download...\n")
    initiateDownload = subprocess.run(["python", "audioDownloader.py", userInput])

    getAlbumArt = subprocess.run(["python", "generateAlbumArt.py"])

    glueArt = subprocess.run(["python", "attachArt.py"])

    moveFile = subprocess.run(
        ["python", "fileMover.py"]
    )
