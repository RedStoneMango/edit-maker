from .transition import apply_transitions
from .graphics import shuffle_for_length
from .renderer import render
from .audio import analyze_audio, align_audio_for_intro
from .composition import build_clips, prepare_clip
from .dataholders import *

def generate(general:GeneralData, base_edit:BaseEditData, intro: IntroData | None):
    res = []
    effective_intro_duration = 0
    missing_audio_due_to_intro = 0

    if intro:
        intro_render_options = (
            base_edit.render_options
            if intro.apply_effects
            else RenderOptions(base_edit.render_options.blur, None, None)
        )
        intro_clip = prepare_clip(intro.graphic, intro.duration, general.size,
                                  intro_render_options, True)
        effective_intro_duration = intro_clip.duration
        missing_audio_due_to_intro = intro.audio_time_of_end or effective_intro_duration
        res.append(intro_clip)

    base_edit_res:BaseEditResult = generate_base_edit(base_edit, general.audio, missing_audio_due_to_intro, general.size)
    res.extend(base_edit_res.clips)

    padded_audio = align_audio_for_intro(base_edit_res.audio.clip, intro.audio_time_of_end if intro else None, effective_intro_duration)
    render(res, padded_audio, general.out)
    

def generate_base_edit(data:BaseEditData, audio_path:str, clip_start_offset:float,
                       size:tuple[int, int]) -> BaseEditResult:
    audio = analyze_audio(audio_path, data.beat_tightness, data.beat_deviation, data.clips_per_beat, clip_start_offset)

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
