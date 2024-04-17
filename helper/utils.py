import time 
from config import Config, Txt


def humanbytes(size):
    if not size: return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'ᴋ', 2: 'ᴍ', 3: 'ɢ', 4: 'ᴛ'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'


def get_time(seconds):
    periods = [('ᴍᴏ', 86400), ('ʜ', 3600), ('ᴍ', 60), ('ꜱ', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)}{period_name}'
    return result
   
 
