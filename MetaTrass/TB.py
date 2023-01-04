import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

TB_usage = '''
====================================== Taxonomic and barcode Reads example commands ======================================
# 
optional arguments:
  -h, --help            show this help message and exit
  -cleanfq1 CLEANFQ1    Paired-end data: cleanfq1 fastq.gz
  -cleanfq2 CLEANFQ2    Paired-end data: cleanfq2 fastq.gz
  -thread THREAD        Kraken parameter
  -sample SAMPLE        Output FileName Prefix
  -ref_db REF_DB        Taxonomy references database
  -genome_size GENOME_SIZE
                        Paired-end data: raw 2 fastq.gz
  -max_depth MAX_DEPTH  Species Maxima-Depth Required Assembly
  -min_depth MIN_DEPTH  Species Minima-Depth Required Assembly
  -outdir OUTDIR        Output folder
  -runnow RUNNOW        Run this script immediately


==========================================================================================================================
'''

def TB(args, Kraken2Taxon, TXACBrefiner, ReadID2Fastq):
	Kraken2Taxon(args)
	TXACBrefiner(args)
	ReadID2Fastq(args)

if __name__ == '__main__':

	# arguments for TB
	parser = argparse.ArgumentParser()

	parser.add_argument('-cleanfq1',                     required=True,  type=str,                               help='Paired-end data: cleanfq1 fastq.gz')
	parser.add_argument('-cleanfq2',                     required=True,  type=str,                               help='Paired-end data: cleanfq2 fastq.gz')
	parser.add_argument('-thread',                       required=False, type=str,  default = '10',              help='Kraken parameter')
	parser.add_argument('-parallel',                     required=False, type=str,  default = '10',              help='The number of parallel species')
	parser.add_argument('-sample',                       required=True,  type=str,                               help='Output FileName Prefix')
	parser.add_argument('-ref_db',                       required=True,  type=str,                               help='Taxonomy references database' )
	parser.add_argument('-genome_size',                  required=True,  type=str,                               help='Paired-end data: raw 2 fastq.gz')
	parser.add_argument('-max_depth',                    required=False, type=str,  default = '300',             help='Species Maximum-Depth Required Assembly')
	parser.add_argument('-min_depth',                    required=False, type=str,  default = '10',              help='Species Minimum-Depth Required Assembly')
	parser.add_argument('-pe_length',                    required=False, type=str,  default = '100',             help='PE read length of sequencing data')
	parser.add_argument('-tp_density',                   required=False, type=str,  default = '0.1',             help='Ture positive read ratio of each barcode')
	parser.add_argument('-outdir',                       required=True,  type=str,                               help='Output folder')
	parser.add_argument('-runnow',                       required=False, type=str,  default = 'False',           help='Run this script immediately')
	
	args = vars(parser.parse_args())
	TB(args, Kraken2Taxon, TXACBrefiner, ReadID2Fastq)



