
import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

TB_usage = '''
====================================== Taxonomic and barcode Reads example commands ======================================
# 


==========================================================================================================================
'''

def TB(args):
	cleanfq1 = args['cleanfq1']
	cleanfq2 = args['cleanfq2']
	thread = args['thread']
	sample = args['sample']
	ref_db = args['ref_db']
	outdir = args['outdir']
	max_depth = args['max_depth']
	min_depth = args['min_depth']
	runnow = args['runnow']

	os.system(' %s %s -cleanfq1 %s -cleanfq2 %s -thread %s -sample %s -ref_db %s -outdir %s -runnow %s'
		%( config_dict['python'], config_dict['Kraken2Taxon'], cleanfq1, cleanfq2, thread, sample, ref_db, outdir, runnow))

	os.system(' %s %s -sample %s -genome_size %s -max_depth %s -min_depth %s -outdir %s -runnow %s'
		%( config_dict['python'], config_dict['TXACBrefiner'], sample, genome_size, max_depth, min_depth, outdir, runnow))

	os.system(' %s %s -cleanfq1 %s -cleanfq2 %s -max_depth %s -min_depth %s -thread %s -outdir %s -runnow %s'
		%( config_dict['python'], config_dict['ReadID2Fastq'], cleanfq1, cleanfq2, max_depth, min_depth, thread, outdir, runnow))



if __name__ == '__main__':

	# arguments for TB
	parser = argparse.ArgumentParser()

	parser.add_argument('-cleanfq1',                     required=True,  type=str,                               help='Paired-end data: cleanfq1 fastq.gz')
	parser.add_argument('-cleanfq2',                     required=True,  type=str,                               help='Paired-end data: cleanfq2 fastq.gz')
	parser.add_argument('-thread',                       required=False, type=str,  default = '20',              help='Kraken parameter')
	parser.add_argument('-sample',                       required=True,  type=str,                               help='Output FileName Prefix')
	parser.add_argument('-ref_db',                       required=True,  type=str,                               help='Taxonomy references database' )
	parser.add_argument('-genome_size',                  required=True,  type=str,                               help='Paired-end data: raw 2 fastq.gz')
	parser.add_argument('-max_depth',                    required=False, type=str,  default = '300',             help='Species Maxima-Depth Required Assembly')
	parser.add_argument('-min_depth',                    required=False, type=str,  default = '10',              help='Species Minima-Depth Required Assembly')
	parser.add_argument('-outdir',                       required=True,  type=str,                               help='Output folder')
	parser.add_argument('-runnow',                       required=False, type=str,  default = 'False',           help='Run this script immediately')
	
	args = vars(parser.parse_args())
	TB(args)



