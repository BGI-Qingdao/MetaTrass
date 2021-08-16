import os
import argparse

from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder
#from MetaTrass.SplitBarcode import SplitBarcode
#from MetaTrass.GetCleandata import GetCleandata

GC_usage = '''
====================================== Get_CleanData example commands ======================================
# 
optional arguments:
  -h, --help      show this help message and exit
  -rawfq1 RAWFQ1  Paired-end data: raw 1 fastq.gz
  -rawfq2 RAWFQ2  Paired-end data: raw 2 fastq.gz
  -thread THREAD  the number of threads
  -outdir OUTDIR  Output folder
  -runnow RUNNOW  Run this script immediately


=========================================================================================================
'''

def GC(args, SplitBarcode, GetCleandata):
	SplitBarcode(args)
	GetCleandata(args)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	
	parser.add_argument('-rawfq1',                       required=True,  type=str,                               help='Paired-end data: raw 1 fastq.gz')
	parser.add_argument('-rawfq2',                       required=True,  type=str,                               help='Paired-end data: raw 2 fastq.gz')
	parser.add_argument('-thread',                       required=False, type=str,  default='10',                help='the number of threads')
	parser.add_argument('-outdir',                       required=True,  type=str,                               help='Output folder')
	parser.add_argument('-runnow',                       required=False, type=str,                               help='Run this script immediately') 

	args = vars(parser.parse_args())
	GC(args, SplitBarcode, GetCleandata)
