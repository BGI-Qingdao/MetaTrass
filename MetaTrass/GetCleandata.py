import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder


GetCleandata_usage = '''
====================================== GetCleandata example commands ======================================
# get HGTs detected at at least TWO levels
MetaCHIP GetCleandata -i NorthSea_pcofg_detected_HGTs.txt -n 2
# get HGTs detected at at least THREE levels and copy their flanking region plots into a new folder
MetaCHIP GetCleandata -i NorthSea_pcofg_detected_HGTs.txt -n 3 -plot NorthSea_pcofg_Flanking_region_plots
=========================================================================================================
'''

def GetCleandata(args):
	outdir = args['outdir']
	argument = args['soap_filter_parameter']

	lane_lst = open(outdir+'lane.lst', 'w')
	lane_lst.write('split_reads.1.fq.gz 0 0 10\nsplit_reads.2.fq.gz 0 0 10\n')
	lane_lst.close()

	cmddir = args['cmddir']   

	shellfile = all_command_shell + '/step2.getcleandata.sh'

	with open(shellfile, 'a') as CMDFILE:
		barcode_list = config_dict['MetaTrass'] + '/config/barcode_list.txt'

		CMDFILE.write('cp %s/lane.lst %s/lane.lst' %())
		CMDFILE.write('cd %s \n' % ( outdir ) )
		CMDFILE.write('perl %s %s %s %s split_reads' % ( config_dict['split_barcode'], rawfq1, rawfq2 ))

	if RUNOW is True:
		report_logger('step1 split_barcode starting', all_command_shell+'/run.log', False)
		os.system('sh %s\n' % shellfile)
		report_logger('step1 split_barcode starting', all_command_shell+'/run.log', False)

	command1 = ' '.join(['cd', outdir])
	command2 = ' '.join([ soap_filter, soap_parameter, 'lane.lst', 'stat.txt'  ])
	command = '\n'.join([command1, command2])
	create_shell_script( 'step1.2 stlfr_data_clean', shfile, command)

if __name__ == '__main__':

	# arguments for GetCleandata
	parser = argparse.ArgumentParser()

	parser.add_argument('-rawfq1',			required=True, type=str,            help='Paired-end data: raw 1 fastq.gz')
	parser.add_argument('-rawfq2',			required=True, type=str,            help='Paired-end data: raw 2 fastq.gz')
	parser.add_argument('-outdir',			required=True, type=str,            help='Output folder')
	parser.add_argument('-runnow',			required=False, type=str,           help='Run this script immediately') 

	args = vars(parser.parse_args())
	GetCleandata(args)



