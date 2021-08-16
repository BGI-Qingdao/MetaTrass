import os
import argparse

from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

TXACBrefiner_usage = '''
====================================== TXACB refining example commands =============================================================

# Using Taxonomic and Barcode information to refining each single-species with main function
python Trass.py TXACBrefiner -kraken_file kraken_result -genome_size genome_size.txt  -outdir ~/GitHub/MetaTrass/Test/ -runnow False

====================================================================================================================================
'''

def TXACBrefiner(args):
	genome_size = args['genome_size']
	sample = args['sample']
	max_depth = args['max_depth']
	min_depth = args['min_depth']
	pe_length = args['pe_length']
	outdir = args['outdir']
	runnow = args['runnow']

	cmddir = outdir + '/all_command_shell/'
	create_folder(cmddir)
	kraken_file = outdir + '/dir2_taxonomy/kraken/' + sample + '.C'

	create_folder(outdir + '/dir2_taxonomy')
	output = outdir + '/dir2_taxonomy/SSRlist/'
	create_folder(output)
	shellfile = cmddir + '/stp2.2.TXACBrefiner.sh'

	with open(shellfile, 'w') as CMDFILE:

		CMDFILE.write('cd %s \n' % ( output ) )
		CMDFILE.write('%s -g %s -k %s -m %s -n %s -r %s\n' % ( config_dict['TABrefiner'], genome_size, kraken_file, max_depth, min_depth, pe_length))

	if runnow == 'yes':
		report_logger('###step2.2 TABrefining starting', cmddir+'/run.log', runnow)
		os.system('sh %s\n' % shellfile)
		report_logger('###step2.2 TABrefining end', cmddir+'/run.log', runnow)
	elif runnow == 'no':
		print('this step2.2 TABrefining is skipped!\n')
	else:
		print('the runnow parameter is wrong with %s\n' %(runnow))


if __name__ == '__main__':

	# arguments for TXACBrefiner
	parser = argparse.ArgumentParser()
	parser.add_argument('-kraken_file',        required=False, type=str,                               help='Taxonomic file by Kraken2')
	parser.add_argument('-genome_size',        required=True,  type=str,                               help='Reference genome size table file')
	parser.add_argument('-sample',             required=True,  type=str,                               help='Sample Name')
	parser.add_argument('-max_depth',          required=False, type=str,  default='300',               help='Species Maximum-Depth Required Assembly')
	parser.add_argument('-min_depth',          required=False, type=str,  default='10',                help='Species Minimum-Depth Required Assembly')
	parser.add_argument('-pe_length',          required=False, type=str,  default='100',               help='PE read length of sequencing data')
	parser.add_argument('-outdir',             required=True,  type=str,                               help='Output folder')
	parser.add_argument('-runnow',             required=False, type=str,  default='no',                help='Set \'yes\' with launch the step immediately')

	args = vars(parser.parse_args())
	TXACBrefiner(args)
