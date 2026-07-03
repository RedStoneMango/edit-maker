def cover_scale(w, h, tw, th):
    return max(tw / w, th / h)

def contain_scale(w, h, tw, th):
    return min(tw / w, th / h)
