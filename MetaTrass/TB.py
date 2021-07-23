
import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

TB_usage = '''
====================================== filter_HGT example commands ======================================
# get HGTs detected at at least TWO levels
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 2
# get HGTs detected at at least THREE levels and copy their flanking region plots into a new folder
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 3 -plot NorthSea_pcofg_Flanking_region_plots
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
    TXACBrefiner_parser.add_argument('-kraken_file',        required=True,  type=str,            help='Paired-end data: raw 1 fastq.gz')
    TXACBrefiner_parser.add_argument('-genome_size',        required=True,  type=str,            help='Paired-end data: raw 2 fastq.gz')
    TXACBrefiner_parser.add_argument('-max_depth',          required=False, type=str,   default = '300',         help='Species Maxima-Depth Required Assembly')
    TXACBrefiner_parser.add_argument('-min_depth',          required=False, type=str,   default = '10',          help='Species Minima-Depth Required Assembly')
    TXACBrefiner_parser.add_argument('-outdir',             required=True,  type=str,            help='Output folder')
    TXACBrefiner_parser.add_argument('-runnow',             required=False, type=str,           help='Run this script immediately') 





def TB(args):
	cleanfq1 = args['cleanfq1']
	cleanfq2 = args['cleanfq2']
	thread = args['thread']
	sample = args['sample']
	ref_db = args['ref_db']
	outdir = args['outdir']
	runnow = args['runnow']

if __name__ == '__main__':

	# arguments for AP
	parser = argparse.ArgumentParser()

	parser.add_argument('-cleanfq1',           		required=True,  type=str,            							help='Paired-end data: cleanfq1 fastq.gz')
	parser.add_argument('-cleanfq2',           		required=True,  type=str,            							help='Paired-end data: cleanfq2 fastq.gz')
	parser.add_argument('-thread',					required=False, type=str, default = '20',           			help='Kraken parameter')
	parser.add_argument('-sample',					required=True,  type=str,           							help='Output FileName Prefix')
	parser.add_argument('-ref_db',					required=True,  type=str,										help='Taxonomy references database' )
	parser.add_argument('-outdir',					required=True,  type=str,            							help='Output folder')
	parser.add_argument('-runnow',					required=False, type=str, default = 'False',         			help='Run this script immediately') 

	args = vars(parser.parse_args())
	AP(args)