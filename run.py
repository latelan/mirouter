import os
import math
import json
import mirouter.mirouter

def get_online_dev():
    devlist = mirouter.get_device_list()
    for dev in devlist:
        time = second_to_date(dev['ip'][0]['online'])
        print '* %s %s %s' % (dev['name'], dev['ip'][0]['ip'], time)

def second_to_hour(time):
    hour = time / 3600
    minute = time % 3600 / 60
    second = time - hour * 3600 - minute * 60
    format =  str(hour) + 'h' + str(minute) + 'm' + str(second) + 's'

    return format

def second_to_date(seconds=None):
    sec = int(seconds)
    if 60 < sec < 60 * 60:
        time = str(sec / 60) + 'm' + str(sec / 60 - (sec / 60) * 60) + 's'
    elif 60 * 60 <= sec < 60 * 60 * 24:
        time = second_to_hour(sec)
    elif sec >= 24 * 60 * 60:
        day = sec / (3600 * 24)
        sec = sec - (day * 3600 * 24)
        time = str(day) + 'd' + second_to_hour(sec)
    else:
        time = str(sec) + 's'

    return time

def second_to_date2(seconds=None):
    time = int(seconds)
    num = 0
    unit = 'd'
    if time:
        if 60 < time < 60 * 60:
            num = math.floor(time / 60)
            unit = 'm'
        elif 60 * 60 <= time < 60 * 60 * 24:
            num = math.floor(time / 3600)
            unit = 'h'
        elif time >= 24 * 60 *60:
            num = math.floor(time / (3600 * 24))
            unit = 'd'
        else:
            num = time
            unit = 's'

    return str(int(num)) + unit

if __name__ == '__main__':
    get_online_dev()
