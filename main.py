import sys
from src import dumpcs

path = sys.argv[1]
path = "../../bpsr/dump.cs"  # for dev
out = "dump"

dcs = dumpcs(path)
dcs.split(out)
