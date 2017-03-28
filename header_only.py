#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a single header from multiple C/C++ files.
"""

from importlib import import_module
import argparse

use_config = True
try:
    import config
except ImportError:
    use_config = False

template_file = ''
output_file = ''
tags = {
    'insert_headers': '/* INTERFACE */',
    'insert_source': '/* IMPLEMENTATION */',
    'begin': '/* BEGIN */',
    'end': '/* END */'
}
header_files = []
source_files = []

def set_defaults():
    template_file = 'template.h'
    output_file = 'single_header.h'

def configure():
    if use_config is False:
        return

def process_file(path):
    lines = []
    with open(path, "r") as infile:
        found_marker = False
        for line in infile:
            if line.strip() == tags['begin']:
                found_marker = True
            elif line.strip() == tags['end']:
                break
            elif found_marker is True:
                lines += line
    lines = lines[1:-2]
    lines += "\n"
    lines += "\n"
    return lines

def process_files(files):
    data = []
    for file in files:
        data.extend(process_file("src/" + file))
    data = data[:-1]
    return "".join(data)

def make_header_only_library(interface_source, implementation_source):
    with open("tools/template.h", "r") as infile, open("io.h", "w") as outfile:
        data = infile.read().replace("/*INTERFACE*/\n", interface_source)
        data = data.replace("/*IMPLEMENTATION*/\n", implementation_source)
        outfile.write(data)
    
if __name__ == '__main__':
    configure()
    parser = argparse.ArgumentParser()
    
