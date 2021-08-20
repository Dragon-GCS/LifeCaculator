# coding = utf-8
# Dragon's Python3.8 code
# Created at 2021/08/20 22:20:36
# Edit with VS Code
# draw other format data by blocks
# data = {"event name":{"value": value}, ...}

import json
from utils import *
from config import *
from colorama import init

import prettytable as prt


def read_data(filename):
    filename = ROOT.joinpath("data", filename)

    if not os.path.isfile(filename):
        print(f"File was not found: '{filename}'")
        exit(0)

    with open(filename) as f:
        return json.load(f)

def main():
    init(autoreset=True)

    filename = "anything.json"
    data = read_data(filename)

    total_value = sum(value["value"] for value in data.values())
    total_blocks = 12 * BLOCK_PER_LINE    # block numbers to show
    
    data = styles_assign(data)

    pt = prt.PrettyTable(hrules=prt.ALL, vrules=prt.NONE)
    pt.field_names = ["Item", "Value", "Percentage", "Style"]

    intervels = []

    for item, detail in data.items():
        value = round(detail['value'], 2)
        style = detail["style"] + SYMBOL + Fore.RESET

        percent = f"{percentage(value, total_value):.2f}%"
        pt.add_row([item, value, percent, style])

        intervels.append((round(total_blocks * value / total_value),detail["style"]))
        
    pt.add_row(["Total", f"{total_value:.1f}", "100.0%", ""])
    print(pt)
    
    draw_blocks(intervels, total_blocks)


if __name__ == '__main__':
    os.system("cls")
    main()
    