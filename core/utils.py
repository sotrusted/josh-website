import re
from urllib.parse import urlparse, parse_qs


def extract_youtube_id(url: str) -> str:
    """
    Accept any YouTube URL form or a bare 11-char ID and return the video ID.
    Returns empty string if nothing recognizable is found.
    """
    if not url:
        return ''
    url = url.strip()
    # youtu.be/ID
    m = re.match(r'(?:https?://)?youtu\.be/([A-Za-z0-9_-]{11})', url)
    if m:
        return m.group(1)
    # youtube.com/watch?v=ID or /embed/ID or /shorts/ID
    m = re.match(r'(?:https?://)?(?:www\.)?youtube\.com/(?:watch\?.*v=|embed/|shorts/)([A-Za-z0-9_-]{11})', url)
    if m:
        return m.group(1)
    # bare ID — exactly 11 alphanumeric/dash/underscore chars
    if re.match(r'^[A-Za-z0-9_-]{11}$', url):
        return url
    return ''
