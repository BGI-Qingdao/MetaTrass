import os
import argparse

from multiprocessing import Pool

from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

ReadID2Fastq_usage = '''
====================================== ReadID2Fastq example commands ======================================

# Covert ReadID to the fastq format compile file with SeqTK
python Trass.py ReadID2Fastq -cleanfq1 FQ1 -cleanfq2 FQ2 -thread 4 -outdir ~/GitHub/MetaTrass/Test/ -runnow True

=========================================================================================================
'''

def convertReadName2FQGZ(outdir, readIdFile, cleanfq1, cleanfq2):
	indir = outdir + '/dir2_taxonomy/SSRlist/'
	output = outdir + '/dir2_taxonomy/ID2FQ/'
	create_folder(output)
	fq1list	= output + readIdFile + '_list_1'
	fq2list = output + readIdFile + '_list_2'
	command1 = ' '.join([ 'awk', '\'{print $1"/1"}\'',  indir + readIdFile, '>', fq1list ])
	command2 = ' '.join([ 'awk', '\'{print $1"/2"}\'',  indir + readIdFile, '>', fq2list ])
	command3 = ' '.join([ config_dict['seqtk'], 'subseq', cleanfq1, fq1list, '|gzip >', fq1list + '.fq.gz' ])
	command4 = ' '.join([ config_dict['seqtk'], 'subseq', cleanfq2, fq2list, '|gzip >', fq2list + '.fq.gz' ])
	command5 = ' '.join([ 'rm -f', fq1list, fq2list])
	command = '\n'.join([ command1, command2, command3, command4, command5 ])
	return command

def lunchFunc(command):
	os.system(command)

def ReadID2Fastq(args):
	cleanfq1 = args['cleanfq1']
	cleanfq2 = args['cleanfq2']
	max_depth = int(args['max_depth'])
	min_depth = int(args['min_depth'])
	parallel = int(args['parallel'])
	outdir = args['outdir']
	runnow = args['runnow']

	indir = outdir + '/dir2_taxonomy/SSRlist/'
	taxReadDepth = indir + 'tax_reads_depth.txt'
	TaskCMD = []

	cmddir = outdir + '/all_command_shell/'
	create_folder(cmddir)
	shellfile = cmddir + '/stp2.3.ReadID2Fastq.sh'

	with open(shellfile, 'w') as CMDFILE:
		if os.path.exists(taxReadDepth):
			for tax in open(taxReadDepth, 'r').readlines():
				taxid, readnum, bareadnum, depth = tax.split()
				if float(depth) >= max_depth:
					readIdFile = args['max_depth'] + 'X.id_' + taxid + '.allbarcode.txt'
					if os.path.exists(indir + readIdFile):
						task = convertReadName2FQGZ(outdir, readIdFile, cleanfq1, cleanfq2)
						TaskCMD.append(task)
						CMDFILE.write('%s\n' % ( task ) )
					else:
						pass
				elif float(depth) >= min_depth:
					readIdFile = args['min_depth'] + 'X.id_' + taxid + '.allbarcode.txt'
					if os.path.exists(indir + readIdFile):
						task = convertReadName2FQGZ(outdir, readIdFile, cleanfq1, cleanfq2)
						TaskCMD.append(task)
						CMDFILE.write('%s\n' % ( task ) )
					else:
						pass
				else:
					pass
		else:
			print('!!!%s not found! Please run the step2.2 TABrefiner at first!!! ' %( taxReadDepth))

	if runnow == 'yes':
		report_logger('###step2.3 ReadID2Fastq starting', cmddir + '/run.log', runnow)
		with Pool(int(parallel)) as p:
			p.map(lunchFunc, TaskCMD)
		report_logger('###step2.3 ReadID2Fastq end', cmddir + '/run.log', runnow)
	elif runnow == 'no':
		print('this step2.3 ReadID2Fastq is skipped!\n')
	else:
		print('the runnow parameter is wrong with %s\n' %(runnow))


if __name__ == '__main__':

	# arguments for ReadID2Fastq
	parser = argparse.ArgumentParser()

	parser.add_argument('-cleanfq1',           required=True,  type=str,                               help='Paired-end data: cleanfq1 fastq.gz')
	parser.add_argument('-cleanfq2',           required=True,  type=str,                               help='Paired-end data: cleanfq2 fastq.gz')
	parser.add_argument('-max_depth',          required=False, type=str,  default = '300',             help='Species Maxima-Depth Required Assembly')
	parser.add_argument('-min_depth',          required=False, type=str,  default = '10',              help='Species Minima-Depth Required Assembly')
	parser.add_argument('-parallel',           required=True,  type=str,  default = '10',              help='Number of Threads')
	parser.add_argument('-outdir',             required=True,  type=str,                               help='Output folder')
	parser.add_argument('-runnow',             required=True,  type=str,  default='no',                help='Set \'yes\' with launch the step immediately')

	args = vars(parser.parse_args())
	ReadID2Fastq(args)

