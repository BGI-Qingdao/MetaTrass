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
	pass

if __name__ == '__main__':

	# arguments for ReadID2Fastq
	parser = argparse.ArgumentParser()

	parser.add_argument('-rawfq1',			required=True, type=str,            help='Paired-end data: raw 1 fastq.gz')
	parser.add_argument('-rawfq2',			required=True, type=str,            help='Paired-end data: raw 2 fastq.gz')
	parser.add_argument('-outdir',			required=True, type=str,            help='Output folder')
	parser.add_argument('-runnow',			required=False, type=str,           help='Run this script immediately') 

	args = vars(parser.parse_args())
	ReadID2Fastq(args)