#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a single header from multiple C/C++ files.
"""

import os
import importlib
import argparse
import sys
sys.dont_write_bytecode = True

use_config = os.path.isfile("config.py")
if use_config:
	config_file = importlib.import_module("config")

includes = []
header_files = []
source_files = []

def configure():
	config = {
		'lib': 'lib',
		'output_file': 'lib.h',
		'namespace': None,
		'tag_begin': "/* BEGIN */",
		'tag_end': "/* END */",
	}
	if use_config:
		if hasattr(config_file, "lib"):
			config['lib'] =  getattr(config_file, "lib")
		if hasattr(config_file, "tag_begin") is True:
			tag_begin = getattr(config_file, "tag_begin")
		if hasattr(config_file, "tag_end"):
			tag_end = getattr(config_file, "tag_end")
	return config

def process_file(path):
    lines = []
    with open(path, "r") as infile:
        found_marker = False
        for line in infile:
            if line.strip() == tag_begin:
                found_marker = True
            elif line.strip() == tag_end:
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
	
def newline(out):
	out.write("\n")
	
def begin_headerguard(out, headerguard):
	out.write("#ifndef " + headerguard)
	newline(out)
	
def end_headerguard(out, headerguard):
	out.write("#endif // " + headerguard)
	newline(out)
	
def begin_extern_c(out):
	out.write("#ifdef __cplusplus")
	newline(out)
	out.write("extern \"C\" {")
	newline(out)
	out.write("#endif")
	newline(out)

def end_extern_c(out):
	out.write("#ifdef __cplusplus")
	newline(out)
	out.write("}")
	newline(out)
	out.write("#endif")
	newline(out)
	
def begin_namespace(out, namespace):
	out.write("namespace " + namespace)
	newline(out)
	
def end_namespace(out, namespace):
	out.write("} // namespace " + namespace)
	newline(out)
	
def begin_implementation(out, define):
	out.write("#ifdef " + define)
	newline(out)
	
def end_implementation(out, define):
	out.write("#endif // " + define)
	newline(out)

def make_header_only_library(config):
	with open(config['output_file'], "w") as out:
		begin_headerguard(out, config['lib'].upper() + "_HEADER"), newline(out)
		begin_extern_c(out), newline(out)
		if config['namespace'] is not None:
			begin_namespace(out, config['lib'].lower()), newline(out)
		# TODO: insert interface
		begin_implementation(out, config['lib'].upper() + "_IMPLEMENTATION"), newline(out)
		# TODO: insert implementation
		end_implementation(out, config['lib'].upper() + "_IMPLEMENTATION"), newline(out)
		if config['namespace'] is not None:
			end_namespace(out, config['lib'].lower()), newline(out)
		end_extern_c(out), newline(out)
		end_headerguard(out, config['lib'].upper() + "_HEADER")
	
if __name__ == '__main__':
	config = configure()
	make_header_only_library(config)
	#parser = argparse.ArgumentParser()
	