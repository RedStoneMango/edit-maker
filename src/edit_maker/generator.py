from .transition import apply_transitions
from .graphics import shuffle_for_length, instantiate_clip
from .renderer import render
from .audio import analyze_audio
from .composition import build_clips
from .dataholders import *

def generate(general:GeneralData, base_edit:BaseEditData, intro: IntroData | None):
    res = []
    effective_intro_duration = 0
    if intro:
        intro_clip = instantiate_clip(intro.graphic, intro.duration)
        effective_intro_duration = intro_clip.duration
        res.append(intro_clip)

    base_edit_data = generate_base_edit(base_edit, general.audio, effective_intro_duration)
    res.extend(base_edit_data.clips)

    render(res, base_edit_data.audio, general.out)
    

def generate_base_edit(data:BaseEditData, audio_path:str, clip_start_offset:float) -> BaseEditResult:
    audio = analyze_audio(audio_path, data.beat_tightness, data.clips_per_beat, clip_start_offset)

    shuffled_clips = shuffle_for_length(data.graphics, len(audio.clip_durations))

    clips = build_clips(
        audio,
        shuffled_clips,
        data.size,
        data.render_options
    )

    clips = apply_transitions(
        clips,
        data.transitions
    )

    return BaseEditResult(clips=clips, audio=audio)
