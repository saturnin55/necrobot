import re


def from_str(time_str):
    """Given a time string, returns the time in total milliseconds, or -1 on failure."""
    args = re.findall(r'\d+', time_str)
    if not args or len(args) > 4:
        return -1
    elif len(args) == 4:
        args[1] += args[0] * 60
        args = args[1:]

    result = int(args[0]) * 60000

    try:
        result += int(args[1]) * 1000
    except IndexError:
        pass

    try:
        result += int(args[2])
    except IndexError:
        pass

    return result


def to_str(time_ms):  # time in milliseconds; returns a string in the form [m]:ss.ttt
    minutes = int(int(time_ms) // int(60000))
    seconds = int(int(time_ms) // int(1000) - int(60)*minutes)
    ms = int(int(time_ms) - 1000*seconds - 60000*minutes)
    return str(minutes) + ':' + str(seconds).zfill(2) + '.' + str(ms).zfill(3)
