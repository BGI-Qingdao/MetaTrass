
import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

TB_usage = '''
====================================== filter_HGT example commands ======================================
# 


=========================================================================================================
'''


    # add argument for Kraken2Taxon_parser 
    Kraken2Taxon_parser.add_argument('-cleanfq1',           required=True,  type=str,            help='Paired-end data: cleanfq1 fastq.gz')
    Kraken2Taxon_parser.add_argument('-cleanfq2',           required=True,  type=str,            help='Paired-end data: cleanfq2 fastq.gz')
    Kraken2Taxon_parser.add_argument('-thread',             required=True,  type=str,   default = '20',            help='Kraken parameter')
    Kraken2Taxon_parser.add_argument('-sample',             required=True,  type=str,            help='Output FileName Prefix')
    Kraken2Taxon_parser.add_argument('-ref_db',             required=True,  type=str,            help='Taxonomy references database' )
    Kraken2Taxon_parser.add_argument('-outdir',             required=True,  type=str,            help='Output folder')
    Kraken2Taxon_parser.add_argument('-runnow',             required=True,  type=str,   default = 'False',         help='Run this script immediately') 
    
    # add argument for TXACBrefiner_parser
    TXACBrefiner_parser.add_argument('-sample',        		required=False,  type=str,            					help='sample name')
    TXACBrefiner_parser.add_argument('-genome_size',        required=True,  type=str,             					help='reference genome size information')
    TXACBrefiner_parser.add_argument('-max_depth',          required=False, type=str,   default = '300',         	help='Species Maxima-Depth Required Assembly')
    TXACBrefiner_parser.add_argument('-min_depth',          required=False, type=str,   default = '10',          	help='Species Minima-Depth Required Assembly')
    TXACBrefiner_parser.add_argument('-outdir',             required=True,  type=str,            					help='Output folder')
    TXACBrefiner_parser.add_argument('-runnow',             required=False, type=str,           					help='Run this script immediately')


def TB(args):
	cleanfq1 = args['cleanfq1']
	cleanfq2 = args['cleanfq2']
	thread = args['thread']
	sample = args['sample']
	ref_db = args['ref_db']
	outdir = args['outdir']
	runnow = args['runnow']

	os.system(' %s %s -cleanfq1 %s -cleanfq2 %s -thread %s -sample %s -ref_db %s -outdir %s -runnow %s'
		%( cleanfq1, cleanfq2, thread, sample, ref_db, outdir, runnow))
	os.system(' %s %s -sample %s -genome_size %s -max_depth %s -min_depth %s -outdir %s -runnow %s'
		%( sample, genome_size, max_depth, min_depth, outdir, runnow))

if __name__ == '__main__':

	# arguments for AP
	parser = argparse.ArgumentParser()

	parser.add_argument('-cleanfq1',           		required=True,  type=str,            							help='Paired-end data: cleanfq1 fastq.gz')
	parser.add_argument('-cleanfq2',           		required=True,  type=str,            							help='Paired-end data: cleanfq2 fastq.gz')
	parser.add_argument('-thread',					required=False, type=str,  default = '20',           			help='Kraken parameter')
	parser.add_argument('-sample',					required=True,  type=str,           							help='Output FileName Prefix')
	parser.add_argument('-ref_db',					required=True,  type=str,										help='Taxonomy references database' )
	parser.add_argument('-outdir',					required=True,  type=str,            							help='Output folder')
	parser.add_argument('-runnow',					required=False, type=str,  default = 'False',         			help='Run this script immediately') 
	parser.add_argument('-genome_size',				required=True,  type=str,            							help='Paired-end data: raw 2 fastq.gz')
	parser.add_argument('-max_depth',				required=False, type=str,  default = '300',         			help='Species Maxima-Depth Required Assembly')

	args = vars(parser.parse_args())
	AP(args)