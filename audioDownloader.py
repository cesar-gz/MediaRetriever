from pytubefix import YouTube
from pytubefix.cli import on_progress
import sys
import sharedVariables

url = sys.argv[1]

yt = YouTube(url, on_progress_callback = on_progress)

print(yt.title)
title = str(yt.title)
sharedVariables.set_video_title(title)

ys = yt.streams.get_audio_only()
ys.download(mp3=True)
