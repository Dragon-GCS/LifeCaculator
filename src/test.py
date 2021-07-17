from json import load
from utils import load_timeline, time_span

data = load_timeline()
timeline = data["timeline"]
dic = {key: value for (key, value) in sorted(timeline.items(), key=lambda kv: kv[1]["start"])}

spans = []
for idx, (key, value) in enumerate(dic.items()):
    if idx == 0:
        temp = value['start']
        continue
    month = time_span(value['start'], temp)
    spans.append((month, dic["Life"]["style"]))
    spans.append((value['month'], value['style']))
    temp = value['end']
