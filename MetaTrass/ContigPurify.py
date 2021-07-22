import os
import argparse

from multiprocessing import Pool
from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

ContigPurify_usage = '''
====================================== Contig Purify example commands ======================================

# quast assessment assembly sequencing based on reference and purifying the contigs
python Trass.py ContigPurify -outdir ~/GitHub/MetaTrass/Test/ -ref_fa ref_fa_DIR

============================================================================================================
'''

### quast assessment assembly sequencing based on reference
def quast_bin(rawContig, reference, threads, outdir, IDY):
	command = ' '.join([ config_dict['python'], config_dict['quast'], '-r', reference, '-t', threads, '--min-identity', IDY, '-o', outdir, rawContig ])
	return command

### purifying the contigs after quast assessment
def purify_bin(rawContig, purifySeq, quastAlnTsv, IDY, PCT):
	command = ' '.join([ config_dict['python'], config_dict['contig_purify'], '-rawContig', rawContig, '-purifySeq', purifySeq, '-quastAlnTsv', quastAlnTsv, '-IDY', IDY, '-PCT', PCT])
	return command

def lunchFunc(command):
	print(command)

def ContigPurify(args):
	IDY = args['IDY']
	PCT = args['PCT']
	thread = args['thread']
	refdir = args['ref_fa']
	outdir = args['outdir']
	runnow = args['runnow']

	taxReadDepth = outdir + '/dir2_taxonomy/SSRlist/' + 'tax_reads_depth.txt'
	TaskCMD = []

	cmddir = outdir + '/all_command_shell/'
	create_folder(cmddir)

	quast_dir = outdir + 'dir3_assembly/quast/'
	create_folder(quast_dir)

	purify_dir = outdir + 'dir3_assembly/purify/'
	create_folder(purify_dir)

	shellfile = cmddir + '/stp3.2.ContigPurify.sh'
	with open(shellfile, 'w') as CMDFILE:
		for tax in open(taxReadDepth, 'r').readlines():
			taxid, readnum, bareadnum, depth = tax.split()
			rawContig = outdir + '/dir3_assembly/supernova/' + taxid + '/' + taxid + '_scaffold.fa'
			reference = refdir + '/' + taxid + '_genomic.fa'
			if float(depth) >= 10:
				if not os.path.exists(rawContig):
					taxid_quast_dir = outdir + 'dir3_assembly/quast/' + taxid
					create_folder(taxid_quast_dir)

					task1 = quast_bin(rawContig, reference, thread, taxid_quast_dir, IDY)

					purifySeq = purify_dir + taxid + '.fa'
					quastAlnTsv = taxid_quast_dir + '/contigs_reports/all_alignments_scaffold.tsv'

					task2 = purify_bin(rawContig, purifySeq, quastAlnTsv, IDY, PCT)
					task = '\n'.join([ task1, task2 ])

					TaskCMD.append(task)
					CMDFILE.write('%s\n' % ( task ) )
				else:
					pass
			else:
				pass
	if runnow:
		report_logger('###step3.1 MetaAssembly starting', cmddir + '/run.log', runnow)
		with Pool(int(thread)) as p:
			p.map(lunchFunc, TaskCMD)
		report_logger('###step3.1 MetaAssembly end', cmddir + '/run.log', runnow)

if __name__ == '__main__':

	# arguments for ContigPurify
	parser = argparse.ArgumentParser()

	parser.add_argument('-PCT',				required=False, type=str, default = '50',				help='Threshold of contig lnegth(0-1)')
	parser.add_argument('-IDY', 			required=False, type=str, default = '90',				help='Threshold of IDY (80 - 100)')
	parser.add_argument('-thread',			required=False, type=str, default = '10',           	help='Number of Threads')
	parser.add_argument('-outdir',			required=True, 	type=str,   							help='Output folder')
	parser.add_argument('-ref_fa',			required=True, 	type=str,								help='Taxonomic reference genome fasta folder')
	parser.add_argument('-runnow',      	required=False, type=str,           					help='Run this script immediately')

	args = vars(parser.parse_args())
	ContigPurify(args)
