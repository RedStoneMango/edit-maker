from .effects import transitions

current_effect = None
idx = 0

def apply_transitions(clip):
    transition_duration = get_transition_duration(clip.duration)

    global current_effect
    global idx

    if current_effect != None:
        clip = clip.with_effects_on_subclip(
            current_effect[0](transition_duration),
            start_time=max(0, clip.duration - transition_duration)
        )

    current_effect = transitions[idx]
    idx = (idx + 1) % len(transitions)

    clip = clip.with_effects_on_subclip(
        current_effect[1](transition_duration),
        end_time=transition_duration
    )
    
    return clip

def get_transition_duration(clip_duration):
    return max(0.15, min(1.0, clip_duration * 0.3))