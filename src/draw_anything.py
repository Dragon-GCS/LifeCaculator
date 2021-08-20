# coding = utf-8
# Dragon's Python3.8 code
# Created at 2021/08/20 22:20:36
# Edit with VS Code
# draw other format data by blocks
# data = {"event name":{"value": value}, ...}

from prettytable.prettytable import NONE
from utils import *
from colorama import init
import prettytable as prt
from config import BLOCK_PER_LINE



def main():
    init(autoreset=True)
    # default data, you can read data from json file.
    data = {
        "House":    {"value":4337.0},
        "Payment":  {"value":1601.0},
        "Food":     {"value":588.93},
        "Daily Necessities": {"value":182.7},
        "Healthy":  {"value":70.2},
        "Sport":    {"value":33.0}}

    total_value = sum(value["value"] for value in data.values())
    total_blocks = 12 * BLOCK_PER_LINE    # block numbers to show
    
    data = styles_assign(data)

    pt = prt.PrettyTable(hrules=prt.ALL, vrules=prt.NONE)
    pt.field_names = ["Item", "Value", "Percentage", "Style"]
    intervels = []
    for item, detail in data.items():
        value = detail['value']
        style = detail["style"] + SYMBOL + Fore.RESET
        percent = f"{percentage(value, total_value):.2f}%"
        intervels.append((round(total_blocks * value / total_value),detail["style"]))
        pt.add_row([item, value, percent, style])
    pt.add_row(["Total", total_value, "100.0%", ""])
    print(pt)
    
    draw_blocks(intervels, total_blocks)


if __name__ == '__main__':
    os.system("cls")
    main()
    