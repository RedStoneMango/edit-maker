import magic
from moviepy import VideoFileClip, ImageClip
import random
import math

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
            duration=duration or 5 # Fallback for intro or outro w/o specified length
        )

    return clip

def shuffle_for_length(clips:list, length):
    """
    This method alerts the `clips` parameter. References a caller
    might hold might be changed
    """
    res = []
    clip_len = len(clips)
    iters = math.ceil(length / clip_len)
    last_clip = None

    for _ in range(0, iters):
        random.shuffle(clips)

        if last_clip and clips[0] == last_clip and clip_len != 1:
            clips.append(clips.pop(0)) # Move to last so we don't have the same entry 2 times in a row
        
        last_clip = clips[-1]
        res.extend(clips)
    
    return res
