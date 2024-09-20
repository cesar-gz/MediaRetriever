def get_video_title():
    try:
        with open('videoTitle.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def set_video_title(title):
    with open('videoTitle.txt', 'w') as f:
        f.write(title)
