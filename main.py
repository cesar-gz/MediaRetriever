import os
from dotenv import load_dotenv

load_dotenv()

"""
TODO

1) create CLI for steps

2) create a call for audioDownloader.py

3) edit audioDownloader to take in a argument as the URL for youtube download

4) create a script that moves the downloaded file to a different location

"""

while True:
    userInput = input("Enter a Youtube video URL (or type 'exit' to quit): ")

    if userInput.lower() == 'exit':
        print("Exiting the program.")
        break

    print(f"You entered: {userInput}")
    # function call here


filePath = os.getenv("FILE_PATH")
print(filePath)
