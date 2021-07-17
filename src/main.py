# coding = utf-8
# Dragon's Python3.8 code
# Created at 2021/07/01 10:23:56
# Edit with VS Code

from utils import *
import time
from colorama import init
import prettytable as prt


def main():
    init(autoreset=True)
    data = load_timeline()
    gender = data["gender"]
    timeline = styles_assign(data["timeline"])

    life = timeline.get("Life")
    if life:
        birthday = life["start"]
    life["days"], life["month"] = life_span(birthday, gender)

    timeline, intervals = get_each_interval(timeline)

    pt = prt.PrettyTable(hrules=prt.ALL, vrules=prt.NONE)
    pt.field_names = ["Event", "Span Days", "Percentage", "Style"]
    for event, detail in timeline.items():
        days = detail['days']
        style = detail["style"] + SYMBOL + Fore.RESET
        percent = f"{percentage(detail['days'], life['days']):.2f}%"
        if event == 'Life':
            percent = f"{percentage(detail['days'], life['days'])}%"
        pt.add_row([event, days, percent, style])
    print(pt)

    draw_blocks(intervals, life["month"])
    while True:
        left_time = 100 - life_percentage(birthday, life['days'])
        print(f"\rYour life has left {left_time:.10f}%", end="")
        time.sleep(0.5)


if __name__ == "__main__":
    os.system("cls")
    main()
