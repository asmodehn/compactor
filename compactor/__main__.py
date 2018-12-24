#!/usr/bin/env python3.7

import sys
import argparse
import os

import compactor


def version():
    print(f"{sys.argv[0]} v{compactor.__version__} from {__file__}")


def usage():
    version()
    print(f"""
Usage : {sys.argv[0]} [input_file]
The compacted file will be send to stdout.
if input_file is not passed, {sys.argv[0]} attempts to read from stdin.
""")


parser = argparse.ArgumentParser(description='Compact a file or standard input')
parser.add_argument('-f', '--file', default=None, type=str, help='file to compress')
parser.add_argument('--version', action='store_true', help='displays the version')

args = parser.parse_args()

if args.version:
    version()
elif hasattr(args, "help") and args.help:
    usage()
else:
    if args.file:
        try:
            # TODO : use streams to read file to allow compressing large files that may not fit in available memory
            with open(args.file, mode='rb') as instr:
                # will work while we can read whole file into memory.
                compressed = compactor.alzw_compress(instr.read())
            sys.stdout.buffer.write(compressed)
        except FileNotFoundError:
            sys.stderr.write(f"file {args.file} NOT FOUND!")
    else:  # we assume reading on stdin
        # TODO : use streams and allow more complex input data than one string line
        compressed = compactor.alzw_compress(input().encode())
        # decoding in dumb ascii to make sure we see something on each and every terminal
        # not the right thing to do for process interface...
        sys.stdout.write(compressed.decode('ascii', errors='replace'))
        sys.stdout.write(os.linesep)
