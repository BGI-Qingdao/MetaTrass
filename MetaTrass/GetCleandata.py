import os
import argparse

from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

GetCleandata_usage = '''
====================================== GetCleandata example commands ================================================
# Get Cleandata from the splitted fastq.gz file.
python GetCleandata.py -thread 20 -outdir ~/GitHub/MetaTrass/Test/ -runnow False

# Running with main function.
python Trass.py GetCleandata  -thread 20 -outdir ~/GitHub/MetaTrass/Test/ -runnow False 
=====================================================================================================================
'''

def GetCleandata(args):
	outdir = args['outdir']
	thread = args['thread']
	runnow = args['runnow']
	parameter = '-F CTGTCTCTTATACACATCTTAGGAAGACAAGCACTGACGACATGA -R TCTGCTGAGTCGAGAACGTCTCTGTGAGCCAAGGAGTTGCTCTGG -y -p -M 2 -f -1 -Q 10'

	cmddir = outdir + '/all_command_shell/'
	create_folder(cmddir)
	output = outdir + '/dir1_cleandata/'
	create_folder(output)
	shellfile = cmddir + '/stp1.2.getcleandata.sh'

	with open(shellfile, 'w') as CMDFILE:
		barcode_list = config_dict['MetaTrass'] + '/config/barcode_list.txt'

		CMDFILE.write('cp %s/lane.lst %s/lane.lst \n' %(config_dict['MetaTrass'] + '/config/', output ))
		CMDFILE.write('cd %s \n' % ( output ) )
		CMDFILE.write('%s -t %s %s lane.lst stat.txt\n' % (config_dict['SOAPfilter'], thread, parameter))

	if runnow is True:
		report_logger('###step1.2 split_barcode starting', cmddir+'/run.log', runnow)
		os.system('sh %s\n' % shellfile)
		report_logger('###step1.2 split_barcode end', cmddir+'/run.log', runnow)

if __name__ == '__main__':

	# arguments for GetCleandata
	parser = argparse.ArgumentParser()
	parser.add_argument('-outdir',			required=True, 	type=str,  										help='Output folder')
	parser.add_argument('-thread',			required=True, 	type=str,  	default = '10',          			help='Running Thread Number')
	parser.add_argument('-runnow',          required=True, 	type=str,  	default = 'False',          		help='Runing immediately')
	parser.add_argument('-parameter',		required=False, type=str, 	default = '-y -F CTGTCTCTTATACACATCTTAGGAAGACAAGCACTGACGACATGA -R TCTGCTGAGTCGAGAACGTCTCTGTGAGCCAAGGAGTTGCTCTGG -p -M 2 -f -1 -Q 10',          help='Run this script immediately') 

	args = vars(parser.parse_args())
	GetCleandata(args)
