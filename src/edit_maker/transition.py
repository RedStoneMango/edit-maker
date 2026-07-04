from .transition_registry import transitions

import random
from proglog import default_bar_logger
from moviepy import VideoClip

current_effect = None
idx = 0

def get_transition_duration(clip_duration):
    return max(0.1, min(1, clip_duration * 0.3))

def create_transitioned(prev_outro:VideoClip, this_intro:VideoClip) -> list[VideoClip]:
    transition = random.choice(transitions)
    return transition.get("factory")(prev_outro, this_intro)

def apply_transitions(clips:list[VideoClip]):
    logger = default_bar_logger("bar")
    logger(message="[3/5]  Applying clip transitions")

    result = []
    clips[0].subclipped

    prev_outro = None
    idx = 0
    clips_len = len(clips)

    for clip in logger.iter_bar(clip=clips):
        idx += 1
        duration = get_transition_duration(clip.duration)

        if clip.duration <= 2 * duration:
            result.append(clip)
            continue
        
        intro = clip.subclipped(0, duration)
        midtro = clip.subclipped(duration, -duration)
        outro = clip.subclipped(-duration)

        # Generate and append trnasition if applicable
        if prev_outro == None:
            result.append(intro)
        else:
            result.extend(create_transitioned(prev_outro, intro))

        # Always use body
        result.append(midtro)

        # Store outro to be combined with next intro or keep if last clip
        if idx == clips_len:
            result.append(outro)
        else:
            prev_outro = outro

    return result
