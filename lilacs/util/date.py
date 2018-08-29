from __future__ import division
from builtins import str
from builtins import object
from datetime import datetime, timedelta
from lilacs.util import pronounce_number
from lilacs.util.time import now_local, get_timedelta, to_local

from collections import namedtuple
import json
import os
import re

NUMBER_TUPLE = namedtuple(
    'number',
    ('x, xx, x0, x_in_x0, xxx, x00, x_in_x00, xx00, xx_in_xx00, x000, ' +
     'x_in_x000, x0_in_x000'))


class DateTimeFormat(object):
    def __init__(self, config_path):
        self.lang_config = {}
        self.config_path = config_path

    def cache(self, lang):
        if lang not in self.lang_config:
            try:
                with open(self.config_path + '/' + lang + '/date_time.json',
                          'r') as lang_config_file:
                    self.lang_config[lang] = json.loads(
                        lang_config_file.read())
            except FileNotFoundError:
                with open(self.config_path + '/en-us/date_time.json',
                          'r') as lang_config_file:
                    self.lang_config[lang] = json.loads(
                        lang_config_file.read())

            for x in ['decade_format', 'hundreds_format', 'thousand_format',
                      'year_format']:
                i = 1
                while self.lang_config[lang][x].get(str(i)):
                    self.lang_config[lang][x][str(i)]['re'] = (
                        re.compile(self.lang_config[lang][x][str(i)]['match']
                                   ))
                    i = i + 1

    def _number_strings(self, number, lang):
        x = (self.lang_config[lang]['number'].get(str(number % 10)) or
             str(number % 10))
        xx = (self.lang_config[lang]['number'].get(str(number % 100)) or
              str(number % 100))
        x_in_x0 = self.lang_config[lang]['number'].get(
            str(int(number % 100 / 10))) or str(int(number % 100 / 10))
        x0 = (self.lang_config[lang]['number'].get(
            str(int(number % 100 / 10) * 10)) or
              str(int(number % 100 / 10) * 10))
        xxx = (self.lang_config[lang]['number'].get(str(number % 1000)) or
               str(number % 1000))
        x00 = (self.lang_config[lang]['number'].get(str(int(
            number % 1000 / 100) * 100)) or
               str(int(number % 1000 / 100) * 100))
        x_in_x00 = self.lang_config[lang]['number'].get(str(int(
            number % 1000 / 100))) or str(int(number % 1000 / 100))
        xx00 = self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 100) * 100)) or str(int(number % 10000 / 100) *
                                                 100)
        xx_in_xx00 = self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 100))) or str(int(number % 10000 / 100))
        x000 = (self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 1000) * 1000)) or
                str(int(number % 10000 / 1000) * 1000))
        x_in_x000 = self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 1000))) or str(int(number % 10000 / 1000))
        x0_in_x000 = self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 1000) * 10)) or str(
            int(number % 10000 / 1000) * 10)

        return NUMBER_TUPLE(
            x, xx, x0, x_in_x0, xxx, x00, x_in_x00, xx00, xx_in_xx00, x000,
            x_in_x000, x0_in_x000)

    def _format_string(self, number, format_section, lang):
        s = self.lang_config[lang][format_section]['default']
        i = 1
        while self.lang_config[lang][format_section].get(str(i)):
            e = self.lang_config[lang][format_section][str(i)]
            if e['re'].match(str(number)):
                return e['format']
            i = i + 1
        return s

    def _decade_format(self, number, number_tuple, lang):
        s = self._format_string(number % 100, 'decade_format', lang)
        return s.format(x=number_tuple.x, xx=number_tuple.xx,
                        x0=number_tuple.x0, x_in_x0=number_tuple.x_in_x0,
                        number=str(number % 100))

    def _number_format_hundreds(self, number, number_tuple, lang,
                                formatted_decade):
        s = self._format_string(number % 1000, 'hundreds_format', lang)
        return s.format(xxx=number_tuple.xxx, x00=number_tuple.x00,
                        x_in_x00=number_tuple.x_in_x00,
                        formatted_decade=formatted_decade,
                        number=str(number % 1000))

    def _number_format_thousand(self, number, number_tuple, lang,
                                formatted_decade, formatted_hundreds):
        s = self._format_string(number % 10000, 'thousand_format', lang)
        return s.format(x_in_x00=number_tuple.x_in_x00,
                        xx00=number_tuple.xx00,
                        xx_in_xx00=number_tuple.xx_in_xx00,
                        x000=number_tuple.x000,
                        x_in_x000=number_tuple.x_in_x000,
                        x0_in_x000=number_tuple.x0_in_x000,
                        formatted_decade=formatted_decade,
                        formatted_hundreds=formatted_hundreds,
                        number=str(number % 10000))

    def date_format(self, dt, lang, now):
        format_str = 'date_full'
        if now:
            if dt.year == now.year:
                format_str = 'date_full_no_year'
                if dt.month == now.month and dt.day > now.day:
                    format_str = 'date_full_no_year_month'

            if (now + timedelta(1)).day == dt.day:
                format_str = 'tomorrow'
            if now.day == dt.day:
                format_str = 'today'
            if (now - timedelta(1)).day == dt.day:
                format_str = 'yesterday'

        return self.lang_config[lang]['date_format'][format_str].format(
            weekday=self.lang_config[lang]['weekday'][str(dt.weekday())],
            month=self.lang_config[lang]['month'][str(dt.month)],
            day=self.lang_config[lang]['date'][str(dt.day)],
            formatted_year=self.year_format(dt, lang, False))

    def date_time_format(self, dt, lang, now, use_24hour, use_ampm):
        date_str = self.date_format(dt, lang, now)
        time_str = nice_time(dt, lang, use_24hour=use_24hour,
                             use_ampm=use_ampm)
        return self.lang_config[lang]['date_time_format']['date_time'].format(
            formatted_date=date_str, formatted_time=time_str)

    def year_format(self, dt, lang, bc):
        number_tuple = self._number_strings(dt.year, lang)
        formatted_bc = (
            self.lang_config[lang]['year_format']['bc'] if bc else '')
        formatted_decade = self._decade_format(
            dt.year, number_tuple, lang)
        formatted_hundreds = self._number_format_hundreds(
            dt.year, number_tuple, lang, formatted_decade)
        formatted_thousand = self._number_format_thousand(
            dt.year, number_tuple, lang, formatted_decade, formatted_hundreds)

        s = self._format_string(dt.year, 'year_format', lang)

        return re.sub(' +', ' ',
                      s.format(
                          year=str(dt.year),
                          century=str(int(old_div(dt.year, 100))),
                          decade=str(dt.year % 100),
                          formatted_hundreds=formatted_hundreds,
                          formatted_decade=formatted_decade,
                          formatted_thousand=formatted_thousand,
                          bc=formatted_bc)).strip()


date_time_format = DateTimeFormat(os.path.dirname(os.path.abspath(__file__)))


def nice_date(dt, lang='en-us', now=None):
    """
    Format a datetime to a pronounceable date

    For example, generates 'tuesday, june the fifth, 2018'
    Args:
        dt (datetime): date to format (assumes already in local timezone)
        lang (string): the language to use, use Mycroft default language if not
            provided
        now (datetime): Current date. If provided, the returned date for speech
            will be shortened accordingly: No year is returned if now is in the
            same year as td, no month is returned if now is in the same month
            as td. If now and td is the same day, 'today' is returned.
    Returns:
        (str): The formatted date string
    """

    date_time_format.cache(lang)

    return date_time_format.date_format(dt, lang, now)


def nice_time(dt, speech=True, use_24hour=False, use_ampm=False):
    """
    Format a time to a comfortable human format

    For example, generate 'five thirty' for speech or '5:30' for
    text display.

    Args:
        dt (datetime): date to format (assumes already in local timezone)
        speech (bool): format for speech (default/True) or display (False)=Fal
        use_24hour (bool): output in 24-hour/military or 12-hour format
        use_ampm (bool): include the am/pm for 12-hour format
    Returns:
        (str): The formatted time string
    """
    if use_24hour:
        # e.g. "03:01" or "14:22"
        string = dt.strftime("%H:%M")
    else:
        if use_ampm:
            # e.g. "3:01 AM" or "2:22 PM"
            string = dt.strftime("%I:%M %p")
        else:
            # e.g. "3:01" or "2:22"
            string = dt.strftime("%I:%M")
        if string[0] == '0':
            string = string[1:]  # strip leading zeros

    if not speech:
        return string

    # Generate a speakable version of the time
    if use_24hour:
        speak = ""

        # Either "0 8 hundred" or "13 hundred"
        if string[0] == '0':
            speak += pronounce_number(int(string[0])) + " "
            speak += pronounce_number(int(string[1]))
        else:
            speak = pronounce_number(int(string[0:2]))

        speak += " "
        if string[3:5] == '00':
            speak += "hundred"
        else:
            if string[3] == '0':
                speak += pronounce_number(0) + " "
                speak += pronounce_number(int(string[4]))
            else:
                speak += pronounce_number(int(string[3:5]))
        return speak
    else:
        if dt.hour == 0 and dt.minute == 0:
            return "midnight"
        if dt.hour == 12 and dt.minute == 0:
            return "noon"
        # TODO: "half past 3", "a quarter of 4" and other idiomatic times

        if dt.hour == 0:
            speak = pronounce_number(12)
        elif dt.hour < 13:
            speak = pronounce_number(dt.hour)
        else:
            speak = pronounce_number(dt.hour - 12)

        if dt.minute == 0:
            if not use_ampm:
                return speak + " o'clock"
        else:
            if dt.minute < 10:
                speak += " oh"
            speak += " " + pronounce_number(dt.minute)

        if use_ampm:
            if dt.hour > 11:
                speak += " p.m."
            else:
                speak += " a.m."

        return speak


def nice_time_delta(time_delta, anchor=None):
    """
        Get a timedelta or datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc
        """
    now = anchor or now_local()
    if isinstance(time_delta, datetime) or isinstance(time_delta, int):
        time_delta = get_timedelta(time_delta, now)

    seconds = time_delta.seconds
    days = time_delta.days

    # handle deltas in the future
    if days < 0:
        future = now - time_delta
        return future_time_delta(future, now)

    # handle deltas in the past
    if days == 0:
        if seconds < 10:
            return "just now"
        if seconds < 60:
            return str(seconds) + " seconds ago"
        if seconds < 120:
            return "a minute ago"
        if seconds < 3600:
            return str(seconds // 60) + " minutes ago"
        if seconds < 7200:
            return "an hour ago"
        if seconds < 86400:
            return str(seconds // 3600) + " hours ago"
    if days == 1:
        return "yesterday"
    if days < 7:
        return str(days) + " days ago"

    if days < 31:
        if days // 7 == 1:
            return "last week"
        return str(days // 7) + " weeks ago"

    if days < 365:
        if days // 30 == 1:
            return "last month"
        return str(days // 30) + " months ago"

    if days // 365 == 1:
        return "last year"
    return str(days // 365) + " years ago"


def future_time_delta(future_date, anchor=None):
    """
        Return a nice string representing a future datetime in english.
        If you need to explicitly set the reference that the future is relative
        to, just pass it in as a second datetime object.
        """

    if not anchor:
        anchor = now_local()

    delta = future_date - anchor
    seconds = delta.seconds
    days = delta.days
    global_seconds = days * 24 * 60 * 60 + seconds
    minutes = int(round(old_div(seconds, 60.)) % 60)
    day_changes = (to_local(future_date) - to_local(datetime(*anchor.timetuple()[:3]))).days

    if days < 0:
        raise AttributeError("Negative timedelta. I can only do futures!")

    if global_seconds <= 45:
        if seconds == 1:
            return "a second"
        if seconds <= 15:
            return 'a moment'
        else:

            return str(seconds) + " seconds"

    elif global_seconds < 60 * 59.5:
        if seconds <= 90:
            return 'about a minute'
        elif seconds <= 60 * 4.5:
            return str(minutes) + " minutes"

    elif anchor.day == future_date.day:
        h = seconds // 3600
        if h == 1:
            hour_string = "1 hour"
        else:
            hour_string = str(h) + " hours"
        if minutes > 4:
            hour_string += " and " + str(minutes) + " minutes"
        return hour_string

    elif global_seconds <= 60 * 60 * 24 * 2 and day_changes == 1:
        if future_date.hour == 0:
            if future_date.minute == 0:
                return 'midnight tonight'
        return 'tomorrow at %s' % nice_time(future_date)

    elif global_seconds <= 60 * 60 * 24 * 8 and day_changes <= 7:
        if day_changes <= 3 or (future_date.weekday() == 6 and anchor.weekday() != 6):
            return '%s at %s' % (future_date.strftime('%A'), nice_time(future_date))
        elif (future_date.weekday() > anchor.weekday() or anchor.weekday() == 6) and day_changes <= 6:
            return 'this %s at %s' % (future_date.strftime('%A'), nice_time(future_date))
        else:
            return 'next %s at %s' % (future_date.strftime('%A'), nice_time(future_date))

    else:
        # needs to be here
        from lilacs.util import nice_date
        return nice_date(future_date)
