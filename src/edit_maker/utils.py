def cover_scale(w, h, tw, th):
    return max(tw / w, th / h)

def contain_scale(w, h, tw, th):
    return min(tw / w, th / h)

def ease_out(x):
    return 1 - (1 - x) ** 3

def zoom_translation(start_scale, end_scale, duration):
    return lambda t: start_scale + (end_scale - start_scale) * ease_out(min(t / max(duration, 0.001), 1.0))
