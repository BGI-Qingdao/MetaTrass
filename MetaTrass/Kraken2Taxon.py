import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder




Kraken2Taxon_usage = '''
====================================== filter_HGT example commands ======================================
# get HGTs detected at at least TWO levels
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 2
# get HGTs detected at at least THREE levels and copy their flanking region plots into a new folder
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 3 -plot NorthSea_pcofg_Flanking_region_plots
=========================================================================================================
'''

def run_kraken_shell(shfile, cleanfq1, cleanfq2, kraken, kraken_parameter, sample, outdir):
	command = ' '.join([ kraken,  kraken_parameter,  '--report', outdir+sample+'.R', '--output', outdir+sample+'.C', cleanfq1, cleanfq2 ])
	create_shell_script('step2.1 run_kraken', shfile, command)




def Kraken2Taxon(args):
	pass

if __name__ == '__main__':

	# arguments for SplitBarcode
	parser = argparse.ArgumentParser()

	parser.add_argument('-rawfq1',			required=True, type=str,            help='Paired-end data: raw 1 fastq.gz')
	parser.add_argument('-rawfq2',			required=True, type=str,            help='Paired-end data: raw 2 fastq.gz')
	parser.add_argument('-outdir',			required=True, type=str,            help='Output folder')
	parser.add_argument('-runnow',			required=False, type=str,           help='Run this script immediately') 

	args = vars(parser.parse_args())
	Kraken2Taxon(args)