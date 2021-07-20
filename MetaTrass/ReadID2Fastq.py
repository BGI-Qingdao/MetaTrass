import os
import argparse

from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

ReadID2Fastq_usage = '''
====================================== filter_HGT example commands ======================================
# get HGTs detected at at least TWO levels
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 2
# get HGTs detected at at least THREE levels and copy their flanking region plots into a new folder
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 3 -plot NorthSea_pcofg_Flanking_region_plots
=========================================================================================================
'''

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

def create_batch_fq_convert_sh(X10, X300, seqtk, indir, outdir, cleanfq1, cleanfq2):
	batchsh_dir = commandsh_dir + '/step2.3.convert_single_species_fq_sh/'
	mkdirIfNotExists(batchsh_dir)

	if len(X10) > 0:
		for i in X10:
			if args.strategy == 'both':
				allreadlist = '10X.id_' + i + '.allread.txt'
				shFileAR = batchsh_dir + 'step2.3_X10_TID' + i + '_AR.sh'
				allbarcodelist = '10X.id_' + i + '.allbarcode.txt'
				shFileAB = batchsh_dir + 'step2.3_X10_TID' + i + '_AB.sh'
				convert_single_species_fq_gz(shFileAR, seqtk, indir, outdir, allreadlist, cleanfq1, cleanfq2)
				convert_single_species_fq_gz(shFileAB, seqtk, indir, outdir, allbarcodelist, cleanfq1, cleanfq2)
			elif args.strategy == 'allread':
				allreadlist = '10X.id_' + i + '.allread.txt'
				shFileAR = batchsh_dir + 'step2.3_X10_TID' + i + '_AR.sh'
				convert_single_species_fq_gz(shFileAR, seqtk, indir, outdir, allreadlist, cleanfq1, cleanfq2)
			elif args.strategy == 'allbarcode':
				allbarcodelist = '10X.id_' + i + '.allbarcode.txt'
				shFileAB = batchsh_dir + 'step2.3_X10_TID' + i + '_AB.sh'
				convert_single_species_fq_gz(shFileAB, seqtk, indir, outdir, allbarcodelist, cleanfq1, cleanfq2)
			else:
				print('Please select valid reads strategy')
	else:
		print('No species depth reach the 10X condition!!!')

def ReadID2Fastq(args):
	

if __name__ == '__main__':

	# arguments for ReadID2Fastq
	parser = argparse.ArgumentParser()

	parser.add_argument('-cleanfq1',				required=True, type=str,            help='Paired-end data: cleanfq1 fastq.gz')
	parser.add_argument('-cleanfq2',				required=True, type=str,            help='Paired-end data: cleanfq2 fastq.gz')
	parser.add_argument('-thread',					required=True, type=str, default = '20',           	help='Kraken parameter')
	parser.add_argument('-sample',					required=True, type=str,            help='Output FileName Prefix')
	parser.add_argument('-ref_db',					required=True, type=str,			help='Taxonomy references database' )
	parser.add_argument('-outdir',					required=True, type=str,            help='Output folder')
	parser.add_argument('-runnow',					required=True, type=str, default = 'False',         help='Run this script immediately')
	
	args = vars(parser.parse_args())
	ReadID2Fastq(args)
