from func import *
from raw_graphs import *
from idc import *
import os
import argparse

RDEBUG_HOST = 'localhost'
RDEBUG_PORT = 12321


def debug():
	import sys
	import pydevd
	print('++ debug()')
	RDEBUG_EGG="/Applications/PyCharm.app/Contents/debug-eggs/pycharm-debug.egg"
	sys.path.append(RDEBUG_EGG)
	pydevd.settrace(RDEBUG_HOST, port=RDEBUG_PORT, stdoutToServer=True, stderrToServer=True)

def parse_command():
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument("--path", type=str, help="The directory where to store the generated .ida file")
	args = parser.parse_args()
	return args

def extract():
	args = parse_command()
	path = args.path
	path = '/Users/Max/Documents/capstone/FeatureEngineering/FeatureResource/rawFeatures/'
	analysis_flags = idc.GetShortPrm(idc.INF_AF)  # idc.INF_START_AF
	analysis_flags &= ~idc.AF_IMMOFF
	# turn off "automatically make offset" heuristic
	idc.SetShortPrm(idc.INF_START_AF, analysis_flags)
	idaapi.autoWait()
	cfgs = get_func_cfgs_c(FirstSeg())
	binary_name = idc.GetInputFile() + '.ida'
	fullpath = os.path.join(path, binary_name)
	pickle.dump(cfgs, open(fullpath, 'w'))
	print binary_name

if __name__ == '__main__':
	idc.Wait()
	# debug()
	extract()
	idc.Exit(0)