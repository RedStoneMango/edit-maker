import magic
from moviepy import VideoFileClip, ImageClip, vfx
import random
import math

is_video_cache = {}

def is_video(file):
    # Just to be sure, verify element presence in cache
    if not file in is_video_cache:
        try:
            mime_type = magic.from_file(file, mime=True)
            is_video_cache[file] = \
                mime_type.startswith("video/") or mime_type == "image/gif"
        except:
            is_video_cache[file] = False
    
    return is_video_cache[file]

def is_valid_graphic(file):
    try:
        mime = magic.from_file(file, mime=True)
        # Cache for #is_video
        is_video_cache[file] = \
                mime.startswith("video/") or mime == "image/gif"
        
        return mime.startswith("video/") or mime.startswith("image/")
    except:
        return False

# When needed, directly provide the duration value to improve performance
#  with ImageClip creation
def instantiate_clip(graphic, duration=None, ensure_fully_playing:bool = False):
    if is_video(graphic):
        clip = VideoFileClip(
            graphic
        )
        if duration:
            clip = video_clip_to_duration(clip, duration, ensure_fully_playing)
    else:
        clip = ImageClip(
            graphic,
            duration=duration or 5 # Fallback for intro or outro w/o specified length
        )

    return clip

def video_clip_to_duration(clip:VideoFileClip, duration, ensure_fully_playing):
    if ensure_fully_playing:
        if clip.duration == duration:
            return clip
        return clip.with_speed_scaled(final_duration=duration)

    if clip.duration > duration:
        return clip.subclipped(0, duration)
    
    if clip.duration < duration:
        return clip.with_effects([vfx.Loop(duration=duration)])
    
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
