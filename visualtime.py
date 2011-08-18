# This Python file uses the following encoding: utf-8
import time, sys
from datetime import date
# see time.struct_time in docs

marker = "<fc=#009900>.</fc>"
marker_active = "<fc=#009900>¤</fc>"
fill_char = "¤"
empty_char = " "
containers = ["[", "]"]
title_suffix = ": "
sep = " "

def load_calendar(start, end):
    # working on day of year ints
    # should probably load this from an external calendar somewhere
    calendar = [date(2011,8,7), date(2011,8,20), ]
    calendar = [d.timetuple()[7] for d in calendar]
    # checks if calendar dates are in scope and remaps to offsets from startdate
    return map(lambda t:t-start, filter(lambda t: t>=start and t<= end, calendar))

def progressbar(title, cur_val, min_val, max_val, num_elements, markers = []):
    # make a nice ascii progressbar, might still be some floor/ceil messing about to fix
    cur_val = min(max_val, max(cur_val, min_val))
    markers = map(lambda m: int(num_elements * (float(m)-min_val)/(max_val - min_val)), markers)
    pos = num_elements * float(cur_val-min_val)/(max_val-min_val)
    buf = "%s%s%s" % (title, title_suffix, containers[0])
    for x in xrange(num_elements):
        if x > pos:
            if x not in markers:
                buf += empty_char
            else:
                buf += marker
        else:
            if x not in markers:
                buf += fill_char
            else:
                buf += marker_active
    return buf + containers[1] + sep


buf = ""

# rolling 60 day window of events ("do i need to remember something this day?")
buf += progressbar(title = "+60d",
                   cur_val = 0,
                   min_val = 0,
                   max_val = 60,
                   num_elements = 60,
                   # todo: fix year wrap
                   markers = load_calendar(start = time.localtime()[7], end = time.localtime()[7]+60))
                   
buf += progressbar(title = "day",
                   cur_val = time.localtime()[3],
                   min_val = 0,
                   max_val = 24,
                   num_elements = 24,
                   markers = [6,12,18])
# workday
buf += progressbar(title = "wd",
                   cur_val = time.localtime()[3],
                   min_val = 8,
                   max_val = 16,
                   num_elements = 8,
                   markers = [11,])
                   
# workweek
buf += progressbar(title = "ww",
                   cur_val = time.localtime()[6],
                   min_val = 0,
                   max_val = 4,
                   num_elements = 5)

print buf.strip()
sys.exit(0)
