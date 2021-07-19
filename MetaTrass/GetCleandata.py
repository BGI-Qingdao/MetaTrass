import os
import argparse

from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

GetCleandata_usage = '''
====================================== GetCleandata example commands ======================================
# Get Cleandata from the splitted fastq.gz file.
python GetCleandata.py -thread 20 -outdir ./TMP_DIR -runnow True -parameter -y -F CTGTCTCTTATACACATCTTAGGAAGACAAGCACTGACGACATGA -R TCTGCTGAGTCGAGAACGTCTCTGTGAGCCAAGGAGTTGCTCTGG -p -M 2 -f -1 -Q 10
# Running with main function.
python Trass.py GetCleandata  -thread 20 -outdir ./TMP_DIR -runnow True -parameter -y -F CTGTCTCTTATACACATCTTAGGAAGACAAGCACTGACGACATGA -R TCTGCTGAGTCGAGAACGTCTCTGTGAGCCAAGGAGTTGCTCTGG -p -M 2 -f -1 -Q 10
=========================================================================================================
'''

def GetCleandata(args):
	outdir = args['outdir']
	thread = args['thread']
	runnow = args['runnow']
	parameter = args['parameter']

	lane_lst = open(outdir+'lane.lst', 'w')
	lane_lst.write('split_reads.1.fq.gz 0 0 10\nsplit_reads.2.fq.gz 0 0 10\n')
	lane_lst.close()

	cmddir = outdir + '/all_command_shell/'
	create_folder(cmddir)
	output = outdir + '/dir1_cleandata/'
	create_folder(output)
	shellfile = cmddir + '/stp1.getcleandata.sh'

	with open(shellfile, 'a') as CMDFILE:
		barcode_list = config_dict['MetaTrass'] + '/config/barcode_list.txt'

		CMDFILE.write('cp %s/lane.lst %s/lane.lst \n' %(config_dict['MetaTrass'] + '/config/', output ))
		CMDFILE.write('cd %s \n' % ( output ) )
		CMDFILE.write('%s -t %s %s lane.lst stat.txt\n' % (config_dict['SOAPfilter'], thread, parameter))


	if args['runnow'] is True:
		report_logger('step1 split_barcode starting', all_command_shell+'/run.log', True)
		os.system('sh %s\n' % shellfile)
		report_logger('step1 split_barcode starting', all_command_shell+'/run.log', True)

if __name__ == '__main__':

	# arguments for GetCleandata
	parser = argparse.ArgumentParser()
	parser.add_argument('-outdir',			required=True, type=str,  help='Output folder')
	parser.add_argument('-thread',			required=True, type=str,  default = '10',          help='Running Thread Number')
	parser.add_argument('-runnow',          required=True, type=str,  default = 'False',          help='Runing immediately')
	parser.add_argument('-parameter',		required=False, type=str, default = '-y -F CTGTCTCTTATACACATCTTAGGAAGACAAGCACTGACGACATGA -R TCTGCTGAGTCGAGAACGTCTCTGTGAGCCAAGGAGTTGCTCTGG -p -M 2 -f -1 -Q 10',          help='Run this script immediately') 

	args = vars(parser.parse_args())
	GetCleandata(args)



