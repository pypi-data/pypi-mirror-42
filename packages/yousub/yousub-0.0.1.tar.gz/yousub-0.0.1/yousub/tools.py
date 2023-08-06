import time
def seconds_to_srt_time(seconds):
    time_str = time.strftime("%H:%M:%S,", time.gmtime(int(float(seconds))))
    seconds_split = seconds.split(".")
    if len(seconds_split) == 2:
        time_str += seconds_split[-1].ljust(3, '0')
    else:
        time_str += "000"
    return time_str


def unescape(s):
    """
    unescape html
    """
    html_codes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in html_codes:
        s = s.replace(code[1], code[0])
    return s

