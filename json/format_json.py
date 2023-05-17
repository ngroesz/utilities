#!/usr/bin/env python

import json
import sys

with open(sys.argv[1]) as f:
    j = json.load(f)

print(json.dumps(j, sort_keys=True, indent=4))
