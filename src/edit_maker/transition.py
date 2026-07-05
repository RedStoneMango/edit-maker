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

def apply_transitions(clips:list):
    logger = default_bar_logger("bar")
    logger(message="[3/5]  Applying clip transitions")

    result = []

    prev_outro = None
    idx = 0
    clips_len = len(clips)

    for clip in logger.iter_bar(clip=clips):
        idx += 1
        trans_duration = get_transition_duration(clip.duration)

        if clip.duration <= 2 * trans_duration:
            result.append(clip)
            continue
        
        intro = clip.subclipped(0, trans_duration)
        midtro = clip.subclipped(trans_duration, -trans_duration)
        outro = clip.subclipped(-trans_duration)

        # Generate and append transition if applicable
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
