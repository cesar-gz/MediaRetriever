import subprocess

while True:
    userInput = input("\nEnter a Youtube video URL, remember to enter the URL with only the first URL query parameter in the link (type 'exit' to quit): ")

    if userInput.lower() == 'exit':
        print("\nExiting the program.\n")
        break

    print("\nstarting download...\n")
    print("You entered: " + userInput)
    initiateDownload = subprocess.run(["python", "audioDownloader.py", userInput])

    #getAlbumArt = subprocess.run(["python", "generateAlbumArt.py"])

    #glueArt = subprocess.run(["python", "attachArt.py"])

    print("\nstarting file moving process...\n")
    moveFile = subprocess.run(["python", "fileMover.py"])
