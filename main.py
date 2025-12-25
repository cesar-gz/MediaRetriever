import subprocess

while True:
    userInput = input("\nEnter a Youtube video URL. Remember to enter the URL with only the first URL query parameter in the link (type 'q' to quit): ")

    if userInput.lower() in ['exit', 'quit', 'q', 'stop', 'bye', 'esc', 'escape', 'end']:
        print("\nExiting the program.\n")
        break

    print("\n")
    initiateDownload = subprocess.run(["python", "audioDownloader.py", userInput])
    print("\nStarting file moving process...")
    moveFile = subprocess.run(["python", "fileMover.py"])
    print("Finished.")
