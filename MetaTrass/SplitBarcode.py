import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

SplitBarcode_usage = '''
====================================== SplitBarcode example commands ======================================
# 

# 

=========================================================================================================
'''


def SplitBarcode(args):
	rawfq1 = args['rawfq1']
	rawfq2 = args['rawfq2']
	outdir = args['outdir']
	runnow = args['runnow']	

	cmddir = outdir + '/all_command_shell/'
	create_folder(cmddir)
	shellfile = cmddir + '/stp0.splitbarcode.sh'
	output = outdir + '/dir1_cleandata/'

	with open(shellfile, 'a') as CMDFILE:
		barcode_list = config_dict['MetaTrass'] + '/config/barcode_list.txt'

		CMDFILE.write('cd %s \n' % ( output ) )
		CMDFILE.write('perl %s %s %s %s split_reads\n' % ( config_dict['split_barcode'], barcode_list, rawfq1, rawfq2 ))

	if runnow is True:
		report_logger('step1 split_barcode starting', all_command_shell+'/run.log', False)
		os.system('sh %s\n' % shellfile)
		report_logger('step1 split_barcode starting', all_command_shell+'/run.log', False)

if __name__ == '__main__':

	# arguments for SplitBarcode
	parser = argparse.ArgumentParser()
	parser.add_argument('-rawfq1',         required=True, type=str,            help='Paired-end data: raw 1 fastq.gz ')
	parser.add_argument('-rawfq2',         required=True, type=str,            help='Paired-end data: raw 2 fastq.gz')
	parser.add_argument('-outdir',         required=True, type=str,            help='Output folder')
	parser.add_argument('-runnow',         required=True, type=str,            help='Run this script immediately')

	args = vars(parser.parse_args())
	SplitBarcode(args)