import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder




Kraken2Taxon_usage = '''
====================================== Kraken2Taxon example commands ======================================
# Using taxonomic references database to classify the sequencing data
python Kraken2Taxon.py -cleanfq1 fq1 -cleanfq2 fq2 -thread 10 -sample SMAPLE -ref_db ref-db \\
-outdir ~/GitHub/MetaTrass/Test/ -runnow False
# Using taxonomic references database to classify the sequencing data with main function
python Trass.py Kraken2Taxon -cleanfq1 fq1 -cleanfq2 fq2 -thread 10 -sample SMAPLE -ref_db ref-db \\
-outdir ~/GitHub/MetaTrass/Test/ -runnow False
=========================================================================================================
'''

def Kraken2Taxon(args):
	cleanfq1 = args['cleanfq1']
	cleanfq2 = args['cleanfq2']
	thread = args['thread']
	sample = args['sample']
	ref_db = args['ref_db']
	outdir = args['outdir']
	runnow = args['runnow']

	cmddir = outdir + '/all_command_shell/'
	create_folder(cmddir)

	shellfile = cmddir + '/stp2.1.kraken2taxon.sh'
	taxdir = outdir + '/dir2_taxonomy/'

	create_folder(taxdir)
	output = outdir + '/dir2_taxonomy/kraken/'
	create_folder(output)

	taxresult = output + sample + '.C'
	taxreport = output + sample + '.R'

	with open(shellfile, 'w') as CMDFILE:
		kraken = config_dict['kraken']
		CMDFILE.write('cd %s \n' % ( output ) )
		CMDFILE.write('%s --threads %s --gzip-compressed --paired --db %s --output %s --report %s %s %s\n' % ( kraken, thread, ref_db, taxresult, taxreport, cleanfq1, cleanfq2))

	if runnow:
		report_logger('###step2.1 kraken classfying starting', cmddir+'/run.log', runnow)
		os.system( 'sh %s\n' % shellfile )
		report_logger('###step2.1 kraken classfying end', cmddir+'/run.log', runnow)

if __name__ == '__main__':

	# arguments for Kraken2Taxon
	parser = argparse.ArgumentParser()

	parser.add_argument('-cleanfq1',				required=True, type=str,            help='Paired-end data: cleanfq1 fastq.gz')
	parser.add_argument('-cleanfq2',				required=True, type=str,            help='Paired-end data: cleanfq2 fastq.gz')
	parser.add_argument('-thread',					required=True, type=str, default = '20',           	help='Kraken parameter')
	parser.add_argument('-sample',					required=True, type=str,            help='Output FileName Prefix')
	parser.add_argument('-ref_db',					required=True, type=str,			help='Taxonomy references database' )
	parser.add_argument('-outdir',					required=True, type=str,            help='Output folder')
	parser.add_argument('-runnow',					required=True, type=str, default = 'False',         help='Run this script immediately') 

	args = vars(parser.parse_args())
	Kraken2Taxon(args)

