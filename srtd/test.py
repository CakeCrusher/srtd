#!/usr/bin/env python3

import core
import filter

# print(core.buildDestinationList(["/home/paul/Pictures"]))
# print(core.buildDestinationList(["/home/paul/School"]))

for file in filter.getMatches("scree", core.buildFileList("/home/paul/Pictures")):
    print(file['name'])
