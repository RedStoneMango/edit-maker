import magic
from moviepy import VideoFileClip, ImageClip

is_video_cache = {}

def is_video(file):
    if not file in is_video_cache:
        try:
            mime_type = magic.from_file(file, mime=True)
            is_video_cache[file] = \
                mime_type.startswith('video/') or mime_type == "image/gif"
        except Exception:
            is_video_cache[file] = False
    
    return is_video_cache[file]

# When needed, directly provide the duration value to improve performance
#  with ImageClip creation
def instantiate_clip(graphic, duration=None):
    if is_video(graphic):
        clip = VideoFileClip(
            graphic
        )
        if duration != None:
            clip = clip.subclipped(0, duration)
    else:
        clip = ImageClip(
            graphic,
            duration=duration
        )

    return clip
