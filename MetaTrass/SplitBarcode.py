
import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

SplitBarcode_usage = '''
====================================== filter_HGT example commands ======================================
# get HGTs detected at at least TWO levels
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 2
# get HGTs detected at at least THREE levels and copy their flanking region plots into a new folder
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 3 -plot NorthSea_pcofg_Flanking_region_plots
=========================================================================================================
'''


def SplitBarcode(rawfq1, rawfq2, outdir, isrun):
	rawfq1 = args['rawfq1']
	rawfq2 = args['rawfq2']
	outdir = args['outdir']
	isrun = args['isrun']	

	all_command_shell = outdir + '/all_command_shell'
	create_folder(all_command_shell)
	shellfile = all_command_shell + '/step1.splitbarcode.sh'

	with open(shellfile, 'a') as CMDFILE:
		barcode_list = config_dict['MetaTrass'] + '/config/barcode_list.txt'

		CMDFILE.write('cd %s \n' % ( outdir ) )
		CMDFILE.write('perl %s %s %s %s split_reads' % ( config_dict['split_barcode'], rawfq1, rawfq2 ))

	if RUNOW is True:
		report_logger('step1 split_barcode starting', all_command_shell+'/run.log', False)
		os.system('sh %s\n' % shellfile)
		report_logger('step1 split_barcode starting', all_command_shell+'/run.log', False)


if __name__ == '__main__':

	# arguments for SplitBarcode
	parser = argparse.ArgumentParser()

	parser.add_argument('-rawfq1',			required=True, type=str,            help='Paired-end data: raw 1 fastq.gz')
	parser.add_argument('-rawfq2',			required=True, type=str,            help='Paired-end data: raw 2 fastq.gz')
	parser.add_argument('-outdir',			required=True, type=str,            help='Output folder')
	parser.add_argument('-runnow',			required=False, type=str,           help='Run this script immediately') 

	args = vars(parser.parse_args())
	SplitBarcode(args)