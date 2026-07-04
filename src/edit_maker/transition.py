from proglog import default_bar_logger
from moviepy import VideoClip

current_effect = None
idx = 0

def apply_transitions(clips:list[VideoClip]):
    logger = default_bar_logger("bar")
    logger(message="[3/5]  Applying clip transitions")
    
    for clip in logger.iter_bar(clip=clips):
        pass
    
    return clips
