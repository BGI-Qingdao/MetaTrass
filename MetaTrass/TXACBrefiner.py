import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder




TXACBrefiner_usage = '''
====================================== filter_HGT example commands ======================================
# get HGTs detected at at least TWO levels
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 2
# get HGTs detected at at least THREE levels and copy their flanking region plots into a new folder
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 3 -plot NorthSea_pcofg_Flanking_region_plots
=========================================================================================================
'''


def get_all_single_species_reads_list(shfile, splitterCC, species_genome_size, min_depth, limited_depth, kraken_C, outdir):
	command1 = ' '.join(['mkdir -p ' + outdir + ' && cd ' + outdir + ' && '])
	command2 = ' '.join([ splitterCC, species_genome_size, kraken_C ])
	create_shell_script( 'get_all_single_species_reads_list', shfile, command1 + command2)

def convert_single_species_fq_gz(shfile, seqtk, indir, outdir, readlist, cleanfq1, cleanfq2):
	fq1list	= outdir + readlist + '_list_1'
	fq2list = outdir + readlist + '_list_2'
	command1 = ' '.join([ 'awk', '\'{print $1"/1"}\'',  indir + readlist, '>', fq1list ])
	command2 = ' '.join([ 'awk', '\'{print $1"/2"}\'',  indir + readlist, '>', fq2list ])
	command3 = ' '.join([seqtk, 'subseq', cleanfq1, fq1list, '|gzip >', fq1list + '.fq.gz' ])
	command4 = ' '.join([seqtk, 'subseq', cleanfq2, fq2list, '|gzip >', fq2list + '.fq.gz' ])
	command5 = ' '.join([ 'rm', fq1list])
	command6 = ' '.join([ 'rm', fq2list])
	command = '\n'.join([ command1, command2, command3, command4, command5, command6 ])
	create_shell_script('convert_single_species_fq_gz', shfile, command)

def TXACBrefiner(args):
	pass

if __name__ == '__main__':

	# arguments for TXACBrefiner
	parser = argparse.ArgumentParser()

	parser.add_argument('-rawfq1',			required=True, type=str,            help='Paired-end data: raw 1 fastq.gz')
	parser.add_argument('-rawfq2',			required=True, type=str,            help='Paired-end data: raw 2 fastq.gz')
	parser.add_argument('-outdir',			required=True, type=str,            help='Output folder')
	parser.add_argument('-runnow',			required=False, type=str,           help='Run this script immediately') 

	args = vars(parser.parse_args())
	TXACBrefiner(args)