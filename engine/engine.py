#!/usr/bin/python

"""
the templateSetEngine: a wrapper script for make
"""
import warnings
import argparse
import subprocess
import sys
import os

VERSION = 0.1

thisScriptsPath = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(
        description='templateSetEngine -- apply database to templateSet',
        epilog='additional arguments are passed to make'
        )
parser.add_argument(
        '-v', '--version',
        action='version',
        version='the \'%(prog)s\' version is '+str(VERSION)
        )
parser.add_argument(
        "target",
        choices=['info', 'sysdeps', 'verify', 'generate', 'clean_state', 'clean'],
        default='generate',
        nargs="*",
        help='perform this list of targets of the Makefile. default target: \'%(default)s\''
        )
parser.add_argument(
        '-DB', '--database',
        required=True,
        help='which yaml database to use on the templateSet'
        )
parser.add_argument(
        '-O', '--outdir',
        default=".",
        help='output directory for the generated templateSet, default: \'%(default)s\''
        )
parser.add_argument(
        '-T', '--templateSet',
        required=True,
        help='templateSet to use'
        )
# parse it. parse our options as good as it can and puts all the rest
# into the "remainder", to be passed to make
(args, remainder) = parser.parse_known_args()

# this looks like a bug in "argparse" -- even if only one "target" is
# supplied via comandline "args.target" is a list. but when using the
# default-value the result is just a string.
if type(args.target)==str:
    args.target = [args.target]

mainMakefile = thisScriptsPath+"/Makefile"

# prepare some more
# pass the $(T) variable:
templateSet = \
    "T="+os.path.realpath(args.templateSet)
if not templateSet.endswith("/"):
    templateSet += "/"
# pass the $(O) variable:
outdir = "O=" + args.outdir
if not outdir.endswith("/"):
    outdir += "/"
# and precious: the database
database="DB="+args.database

# and finally calling make! could add more code for error recovery, deleting a wrong $(O)Makefile.inc for example
retval = subprocess.call(["make", "-f", mainMakefile, outdir, templateSet, database]+args.target+remainder)

if retval == 2:
    print "\n'make' encountered an error; consider deleting outdir '%s'" % (os.path.realpath(args.outdir))

sys.exit(retval)
