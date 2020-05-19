from django import template

register = template.Library()

@register.filter()
def timefield(timedeltaobj):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    secs = timedeltaobj.total_seconds()
    timetot = ""
    if secs > 60:
        mins = secs // 60
        if mins < 10:
            timetot += "0{}:".format(int(mins))
        else:
            timetot += "{}:".format(int(mins))
        secs = secs - mins*60

    if secs > 0:
        if secs < 10:
            timetot += "0{}".format(int(secs))
        else:
            timetot += "{}".format(int(secs))
    return timetot