#!/usr/bin/env python3

"""
Run this file when you want to regen all the effects for a new build

NOTE: as you can see, it relies on my pa_tools library to be up one directory and inside pa_tools
You can either download my repo to the parent of this mod's dir, or you can download it somewhere else and just update this path
"""

import sys
sys.path.append("../pa_tools")

import mod_generator

mod_generator.run("pa_fx_gen.json")
