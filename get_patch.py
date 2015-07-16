#!/usr/bin/env python3

"""
DON'T RUN THIS FILE
- it's only here for reference sake in terms of how I made the patch file.
RUN ./update.py INSTEAD
"""

import sys
sys.path.append("../pa_tools")


import loader
from collections import OrderedDict
import patcher
import utils
import os

# get base pa directory
base_path = utils.pa_media_dir()
# the directory where the mod files are (right here in this case xD)
mod_path = '.'

# get the unit list file dir
unit_list_path = os.path.join(base_path, "pa/units/unit_list.json")

# unit list files for comparing
unit_list = loader.load(unit_list_path)

patches = []

# iterate over all the units
for unit_file in unit_list['units']:
    # get rid of the extra slash at the start so that path join works
    unit_file = unit_file[1:]
    base_unit_path = os.path.join(base_path, unit_file)

    unit_base = loader.load(base_unit_path)

    # check to see if it's actually a file we've bothered shadowing or not:
    mod_unit_path = os.path.join(mod_path, unit_file)

    # the mod doesn't shadow this file; no need to compare them
    if not os.path.exists(mod_unit_path): continue

    unit_mod = loader.load(mod_unit_path)

    # compute diff in terms of json diff
    diff = patcher.from_diff(unit_base, unit_mod)

    # remove anything that isn't to do with fx_offsets (since those changes represent balance/configuration changes)

    diff = [op for op in diff if op['path'].startswith('/fx_offsets')]

    for op in diff:
        # here just to make things robust, we use the more generic version of 'add' to array
        if op['path'].startswith('/fx_offsets/'):
            # this path just means append to the end of the array
            # which means we are not relying on the number of fx that are already on a unit in PA's base game files
            # this makes the patch itself more robust
            op['path'] = '/fx_offsets/-'

    # store this patch
    loader.dump(OrderedDict([('target', unit_file),('patch', diff )]), 'src/' + unit_file + '.patch', indent=2)
    patches.append({'from_file' : unit_file + '.patch'})

options = loader.loads("""{
            "output_dir" : "..",
            "pretty_print_effects" : true,
            "indent" : 2
        }""")

modinfo = loader.load("modinfo.json")

patcher_mod_file = OrderedDict([
        ('options', options),
        ('modinfo', modinfo),
        ('mod', patches)
    ])

# now store all these patches in a single file
loader.dump(patcher_mod_file, 'src/mod.json', indent=2)









