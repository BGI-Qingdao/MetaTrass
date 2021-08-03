import os
import argparse

from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

AP_usage = '''
======================================  example commands ======================================

# 


=========================================================================================================
'''

def AP(args, MetaAssembly, ContigPurify):
	MetaAssembly(args)
	ContigPurify(args)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	# add argument for TB
	parser.add_argument('-maprate',                      required=False, type=str,   default='8',                help='mapping ratio (default=8)')
	parser.add_argument('-thread',                       required=False, type=str,   default='6',                help='number of threads use(default = 6)')
	parser.add_argument('-memory',                       required=False, type=str,   default='150',              help='number of memory use(GB,default = 150)',)
	parser.add_argument('-maxreads',                     required=False, type=str,   default='2140000000',       help='maximumreads for supernova(default = 2140000000)')
	parser.add_argument('-pairdepth',                    required=False, type=str,   default='2',                help='filter less X pair barcode reads(default = 2)')
	parser.add_argument('-outdir',                       required=True,  type=str,                               help='output folder') 
	parser.add_argument('-runnow',                       required=False, type=str,                               help='Run this script immediately') 
	parser.add_argument('-PCT',                          required=False, type=str,   default = '50',             help='Threshold of contig lnegth(0-1)')
	parser.add_argument('-IDY',                          required=False, type=str,   default = '90',             help='Threshold of IDY (80 - 100)')
	parser.add_argument('-ref_fa',                       required=True,  type=str,                               help='Taxonomic reference genome fasta folder')
	parser.add_argument('-max_depth',                    required=False, type=str,  default = '300',             help='Species Maximum-Depth Required Assembly')
	parser.add_argument('-min_depth',                    required=False, type=str,  default = '10',              help='Species Minimum-Depth Required Assembly')
	parser.add_argument('-thread',                       required=False, type=str,   default = '10',             help='Number of Threads')
	parser.add_argument('-outdir',                       required=True,  type=str,                               help='Output folder')
	parser.add_argument('-runnow',                       required=False, type=str,                               help='Run this script immediately')

	args = vars(parser.parse_args())
	AP(args, MetaAssembly, ContigPurify)
