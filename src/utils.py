# coding = utf-8
# Dragon's Python3.8 code
# Created at 2021/07/02 10:56:29
# Edit with VS Code

import os
import json
import calendar
import time
from datetime import datetime
from colorama import Fore, init

LIFESPAN = {"average": 76.34, "male": 73.64, "famale": 79.43}
# source:https://data.stats.gov.cn/easyquery.htm?cn=C01&zb=A0304&sj=2019
TIMEFORMAT = "%Y%m%d"
SYMBOL = "■"
birthday = "19951001"  # default


def draw_blocks(intervals: list, total_blocks: int) -> None:
    intervals.append((total_blocks - sum([interval[0] for interval in intervals]), Fore.WHITE))
    styles = ''.join([(style + SYMBOL) * m for m, style in intervals]).split(SYMBOL)[:-1]
    for idx, style in enumerate(styles):
        print(style + SYMBOL, end="")
        if idx % 48 == 47:
            print()
    print()


def get_each_interval(timeline: dict):
    """
    Get each interval of & between events
    Args:
        timeline: timeline dict
    Returns:
        timeline: timeline dict include event's 'span' and 'pre_interval'
        span: list of intervals of events, [(span_month, style), ...]
    """
    intervals = []
    for idx, (event, detail) in enumerate(timeline.items()):
        if idx == 0:
            assert event == 'Life'
            temp = detail['start']
            continue
        else:
            assert int(detail['start']) > int(temp)
            detail["days"] = time_span(detail["start"], detail["end"], mode="day")
            detail["month"] = time_span(detail["start"], detail["end"], mode="month")
            detail["pre_interval"] = time_span(detail['start'], temp, mode='month')
            intervals.append((detail["pre_interval"], timeline["Life"]["style"]))
            intervals.append((detail['month'], detail['style']))
            temp = detail['end']
    today = datetime.strftime(datetime.now(), TIMEFORMAT)
    intervals.append((time_span(today, temp, mode="month"), timeline["Life"]["style"]))
    return timeline, intervals


def life_span(birthday: str, gender=None):
    """
    Calculate the life days
    Args:
        birthday: the day of birth, by format TIMEFORMAT
        gender: choose in male,famale or None
    Returns:
        days: the days of life
        month: the month of life
    """
    age = LIFESPAN[gender] if gender else LIFESPAN["average"]
    birthday = datetime.strptime(birthday, TIMEFORMAT)
    death_year = int(birthday.year + age) + 1
    leapdays = calendar.leapdays(birthday.year, death_year + 1)
    days = int(age * 365) + 1 + leapdays
    month = round(age * 12)
    return days, month


def time_span(start: str, end: str, mode='day') -> int:
    """
    Calculate the time between start to end.
    Args:
        start: start time, format=YYYYMMDD
        end: end time, format = YYYYMMDD
        mode: include [month, day, second]
    Returns:
        span: the span time corresponding to modes.
    """
    if int(start) > int(end):
        start, end = end, start
    start = datetime.strptime(start, TIMEFORMAT)
    end = datetime.strptime(end, TIMEFORMAT)
    if mode == "month":
        # 整年：（终年-始年-1）*12
        # 始年月份： 12 - 始月
        # 终年月份： 终月
        month = (end.year - start.year) * 12 - start.month + end.month
        if start.day <= 15:
            month += 1
        if end.day <= 16:
            month -= 1
        return month
    elif mode == 'day':
        span = end - start
        return span.days


def percentage(partial: int, total: int) -> float:
    """
    Calculate the days' percentage
    Args:
        partial: partial num
        total: total num
    Returns:
        percentage: the days' percentage
    """
    return 100 * (partial / total)


def life_percentage(birth: str, total_days: int) -> float:
    """
    the second passed from birth to now
    Args:
        birth: birthday, format = YYYYMMDD
        total_day: total life days
    Returns:
        returns: the percentage
    """
    total_sec = total_days * 24 * 3600
    birth_time = time.mktime(time.strptime(birth, TIMEFORMAT))
    return percentage(time.time() - birth_time, total_sec)


def load_timeline() -> dict:
    """
    Get the timeline infomation
    Args:
        None
    Returns:
        returns: timeline dict, {event0:{start,end},...}
    """
    filename = os.path.join(os.path.dirname(__file__), "timeline.json")
    if not os.path.isfile(filename):
        filename = os.path.join(os.path.dirname(__file__),
                                "timeline.default.json")
    with open(filename) as f:
        data = json.load(f)
        timeline = data.get("timeline")
        if timeline:
            data["timeline"] = {key: value for (key, value) in sorted(timeline.items(), key=lambda kv: kv[1].get("start", 0))}
            return data
        else:
            print("Not Found timeline in timeline.json")
            exit()


class CycleList():
    def __init__(self, list):
        self.list = list
        self.max_num = len(list)

    def __getitem__(self, idx):
        idx = idx % self.max_num
        return self.list[idx]


def styles_assign(timeline: dict) -> dict:
    """
    Assign the color to every event
    Args:
        timeline: timeline dict
    Returns:
        timeline: timeline dict include the style
    """
    styles = CycleList([
        Fore.LIGHTBLUE_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTRED_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX
    ])
    for idx, key in enumerate(timeline.keys()):
        if key == "gender":
            continue
        timeline[key]["style"] = styles[idx]
    return timeline


if __name__ == "__main__":
    data = load_timeline()
    gender = data["gender"]
    timeline = styles_assign(data["timeline"])
    for key in timeline.keys():
        print(timeline[key]["style"] + key)
    print("over")
