from .transition import apply_transitions
from .graphics import shuffle_for_length
from .renderer import render
from .audio import analyze_audio, pad_audio_beginning
from .composition import build_clips, prepare_clip
from .dataholders import *

def generate(general:GeneralData, base_edit:BaseEditData, intro: IntroData | None):
    res = []
    base_clips_start_offset = 0

    if intro:
        intro_clip = prepare_clip(intro.graphic, intro.audio_duration, general.size,
                                  base_edit.render_options, True)
        base_clips_start_offset = intro_clip.duration
        res.append(intro_clip)

    # If we want audio to play, delay base edit clips by that time
    #  (keeping audio playback for later concat), otherwise don't trim anything
    base_edit_res:BaseEditResult = generate_base_edit(base_edit, general.audio,
                                                      base_clips_start_offset if intro.audio_duration else 0,
                                                      general.size)
    res.extend(base_edit_res.clips)

    # If we have an intro without audio overlap, the video audio should be silent for that time
    padded_audio = pad_audio_beginning(base_edit_res.audio.clip,
                                       base_clips_start_offset if not intro.audio_duration else 0)
    render(res, padded_audio, general.out)
    

def generate_base_edit(data:BaseEditData, audio_path:str, clip_start_offset:float,
                       size:tuple[int, int]) -> BaseEditResult:
    audio = analyze_audio(audio_path, data.beat_tightness, data.clips_per_beat, clip_start_offset)

    shuffled_clips = shuffle_for_length(data.graphics, len(audio.clip_durations))

    clips = build_clips(
        audio,
        shuffled_clips,
        size,
        data.render_options
    )

    clips = apply_transitions(
        clips,
        data.transitions
    )

    return BaseEditResult(clips=clips, audio=audio)
