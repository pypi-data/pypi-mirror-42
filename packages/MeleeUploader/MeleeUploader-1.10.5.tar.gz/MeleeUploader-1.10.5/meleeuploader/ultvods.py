#!/usr/bin/env python3

from consts import *
import pickle

queue = None
with open(queue_values, "rb") as f:
    queue = pickle.load(f)

for options in queue:
    options.file = "/Users/Nikki/Videos/" + options.file.split("/")[-1]
    options.ename = "Cary Fight Night"
    options.ename_min = "CFN"
    options.pID = "PLHnxLvipJ418B-1sII32d7isi765-axC5"
    options.bracket = ""
    options.mprefix = ""
    options.tags = 'PurdueSmash, Purdue Smash'

with open(queue_values, "wb") as f:
    f.write(pickle.dumps(queue))
