STYLES = {
    "classic": {"model": "hayao"},
    "anime": {"model": "hayao"},
    "comic": {"model": "paprika"},
    "watercolor": {"model": "shinkai"},
    "sketch": {"model": "hayao"},
    "oil": {"model": "shinkai"},
    "pixar": {"model": "paprika"},
    "popart": {"model": "paprika"},
    "sticker": {"model": "hayao"},
    "minimal": {"model": "shinkai"},
}

def get_model(style):
    style = style.lower()
    if style in STYLES:
        return STYLES[style]["model"]
    return "hayao"