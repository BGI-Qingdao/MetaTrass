import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

MetaAssembly_usage = '''
====================================== filter_HGT example commands ======================================
# get HGTs detected at at least TWO levels
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 2
# get HGTs detected at at least THREE levels and copy their flanking region plots into a new folder
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 3 -plot NorthSea_pcofg_Flanking_region_plots
=========================================================================================================
'''


def supernova_assembly_shell(shfile, python2, supernovaPY, supernova_parameter, tssfq1, tssfq2, sample, outdir):
	supernova_dir = outdir + '/supernova/' + sample
	command1 = ' '.join([ 'mkdir -p ', supernova_dir, ' && cd ', supernova_dir ])
	command2 = ' '.join([ python2, supernovaPY, supernova_parameter, '-n', sample, '-r1', tssfq1, '-r2', tssfq2,'-o', supernova_dir ])
	command3 = ' '.join([ 'mv', supernova_dir + '/supernova_out/supernova_out.mri.tgz', supernova_dir ])
	command4 = ' '.join([ 'rm -rf', supernova_dir + '/supernova_out/' ])
	command5 = ' '.join([ 'gunzip -c', supernova_dir+'/'+sample+'_supernova_result.fasta.gz', '>', supernova_dir + '/scaffold.fa'])
	command6 = ' '.join([ 'rm -rf', supernova_dir + '/*.fastq.gz'])
	command = '\n'.join([ command1, command2, command3, command4, command5, command6 ])
	create_shell_script( 'supernova_assembly_shell', shfile, command)

def MetaAssembly(args):
	pass
	
if __name__ == '__main__':

	# arguments for MetaAssembly
	parser = argparse.ArgumentParser()

	parser.add_argument('-rawfq1',			required=True, type=str,            help='Paired-end data: raw 1 fastq.gz')
	parser.add_argument('-rawfq2',			required=True, type=str,            help='Paired-end data: raw 2 fastq.gz')
	parser.add_argument('-outdir',			required=True, type=str,            help='Output folder')
	parser.add_argument('-runnow',			required=False, type=str,           help='Run this script immediately') 

	args = vars(parser.parse_args())
	MetaAssembly(args)