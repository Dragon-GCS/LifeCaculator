LIFESPAN = {"average": 76.34, "male": 73.64, "famale": 79.43}
# source:https://data.stats.gov.cn/easyquery.htm?cn=C01&zb=A0304&sj=2019
TIMEFORMAT = "%Y%m%d"
SYMBOL = "■"
birthday = "19951001"  # default

BLOCK_PER_LINE = 48

from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILENAME = ROOT.joinpath("data", "timeline.default.json")