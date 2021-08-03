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
	os.system(command)

def ContigPurify(args):
	IDY = args['IDY']
	PCT = args['PCT']
	thread = args['thread']
	refdir = args['ref_fa']
	max_depth = args['max_depth']
	min_depth = args['min_depth']
	outdir = args['outdir']
	runnow = args['runnow']

	taxReadDepth = outdir + '/dir2_taxonomy/SSRlist/' + 'tax_reads_depth.txt'
	TaskCMD = []

	cmddir = outdir + '/all_command_shell/'
	create_folder(cmddir)

	asbdir = outdir + '/dir3_assembly/'
	create_folder(asbdir)

	quast_dir = asbdir + '/quast/'
	create_folder(quast_dir)

	purify_dir = asbdir + '/purify/'
	create_folder(purify_dir)

	shellfile = cmddir + '/stp3.2.ContigPurify.sh'
	with open(shellfile, 'w') as CMDFILE:
		if os.path.exists(taxReadDepth):
			for tax in open(taxReadDepth, 'r').readlines():
				taxid, readnum, bareadnum, depth = tax.split()
				rawContig = outdir + '/dir3_assembly/supernova/' + taxid + '/' + taxid + '_scaffold.fa'
				reference = refdir + '/' + taxid + '_genomic.fa'
				if float(depth) >= float(min_depth):
					if os.path.exists(rawContig):
						taxid_quast_dir = outdir + 'dir3_assembly/quast/' + taxid
						create_folder(taxid_quast_dir)
	
						task1 = quast_bin(rawContig, reference, thread, taxid_quast_dir, IDY)

						purifySeq = purify_dir + taxid + '.fa'
						quastAlnTsv = taxid_quast_dir + '/contigs_reports/all_alignments_' + taxid + '_scaffold.tsv'
						task2 = purify_bin(rawContig, purifySeq, quastAlnTsv, IDY, PCT)
						task = '\n'.join([ task1, task2 ])

						TaskCMD.append(task)
						CMDFILE.write('%s\n' % ( task ) )
					else:
						pass
				else:
					pass
		else:
			print('!!!%s not found! Please run the step2.2 TABrefiner at first!!! ' %( taxReadDepth))
	if runnow == 'yes':
		report_logger('###step3.2 ContigPurify starting', cmddir + '/run.log', runnow)
		with Pool(int(thread)) as p:
			p.map(lunchFunc, TaskCMD)
		report_logger('###step3.2 ContigPurify end', cmddir + '/run.log', runnow)
	elif runnow == 'no':
		print('this step3.2 ContigPurify is skipped!\n')
	else:
		print('the runnow parameter is wrong with %s\n' %(runnow))


if __name__ == '__main__':

	# arguments for ContigPurify
	parser = argparse.ArgumentParser()

	parser.add_argument('-PCT',			required=False, type=str, default = '50',		help='Threshold of contig lnegth(0-1)')
	parser.add_argument('-IDY', 			required=False, type=str, default = '90',		help='Threshold of IDY (80 - 100)')
	parser.add_argument('-thread',			required=False, type=str, default = '10',           	help='Number of Threads')
	parser.add_argument('-ref_fa',			required=True, 	type=str,				help='Taxonomic reference genome fasta folder')
	parser.add_argument('-max_depth',               required=False, type=str,  default = '300',             help='Species Maximum-Depth Required Assembly')
	parser.add_argument('-min_depth',               required=False, type=str,  default = '10',              help='Species Minimum-Depth Required Assembly')
	parser.add_argument('-outdir',			required=True, 	type=str,   				help='Output folder')
	parser.add_argument('-runnow',                  required=True,  type=str,  default='no',                help='Set \'yes\' with launch the step immediately')

	args = vars(parser.parse_args())
	ContigPurify(args)
