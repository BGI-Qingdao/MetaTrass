import os
import argparse

from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

GC_usage = '''
====================================== Get_CleanData example commands ======================================
# 


=========================================================================================================
'''

def GC(args):
	rawfq1 = args['rawfq1']
	rawfq2 = args['rawfq2']
	thread = args['thread']
	outdir = args['outdir']
	runnow = args['runnow']
	# Splitting Barcode 
	os.system('%s %s -rawfq1 %s -rawfq2 %s -outdir %s -runnow %s' %(config_dict['python'],  config_dict['SplitBarcode'], rawfq1, rawfq2, outdir, runnow ))
	# Getting Cleandata
	os.system('%s %s -thread %s -outdir %s -runnow' %(config_dict['python'], config_dict['GetCleandata'], thread, outdir, runnow))

if __name__ == '__main__':

	# arguments for SplitBarcode
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-rawfq1',                       required=True,  type=str,                               help='Paired-end data: raw 1 fastq.gz')
	parser.add_argument('-rawfq2',                       required=True,  type=str,                               help='Paired-end data: raw 2 fastq.gz')
	parser.add_argument('-thread',                       required=False, type=str,  defulat='10',                help='the number of threads')
	parser.add_argument('-outdir',                       required=True,  type=str,                               help='Output folder')
	parser.add_argument('-runnow',                       required=False, type=str,                               help='Run this script immediately') 

	args = vars(parser.parse_args())
	GC(args)