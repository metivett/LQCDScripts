#! /usr/bin/python

import argparse
import math
import os
import shutil

parser = argparse.ArgumentParser(description='Split lattices.dat and prepare directories to run dynqcd.')
parser.add_argument('lattices', action='store', default="lattices.dat", type=argparse.FileType('r'), help='the lattices.dat file to split (default: %(default)s)')
parser.add_argument('nconf_per_run', action='store', type=int, help='number of configurations analyzed per run')
parser.add_argument('--paramfile', action='store', nargs='?', const="parameters", help='copy parameter file with given name (default: %(default)s) in each run directory')
parser.add_argument('--jobfile', action='store', nargs='?', const="job", help='copy job file with given name (default: %(default)s) in each run directory')
parser.add_argument('--dirname', action='store', default="run", help='name for the created run directories (default: %(default)s)')

args = parser.parse_args()

# read lattices file
lat = args.lattices.read()

# split into N chunks of nconf_per_run lines across run* directories
lattices = [l for l in lat.split("\n") if l]
Nlat = len(lattices)
N = int(math.ceil(Nlat / float(args.nconf_per_run)))

for i in range(0, N):
	rundir = args.dirname + str(i)
	if not os.path.exists(rundir):
		os.makedirs(rundir)

	with open(rundir + "/lattices.dat", "w") as latfile:
		latfile.write('\n'.join(lattices[args.nconf_per_run*i:min(args.nconf_per_run*(i+1), Nlat)]))

	if args.paramfile:
		shutil.copy(args.paramfile, rundir + "/" + args.paramfile)
	if args.jobfile:
		shutil.copy(args.jobfile, rundir + "/" + args.jobfile)

print("Created %s run directories." % N)