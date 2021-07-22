import os
import argparse
from multiprocessing import Pool
from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

MetaAssembly_usage = '''
====================================== MetaAssembly example commands ======================================

# 

=========================================================================================================
'''

def supernova_assembly(tssfq1, tssfq2, memory, maprate, threads, maxreads, pairdepth, outdir, sample):
	create_folder(outdir + 'dir3_assembly/')
	create_folder(outdir + 'dir3_assembly/supernova/')
	output = outdir + 'dir3_assembly/supernova/' + sample
	create_folder(output)

	command1 = ' '.join([ 'mkdir -p ', output, ' && cd ', output ])
	command2 = ' '.join([ config_dict['python'], config_dict['sflfr2supernova'], '-fastq1', tssfq1, '-fastq2', tssfq2, 
		'-memory', memory, '-maprate', maprate, '-threads', threads, '-maxreads', maxreads, '-pairdepth', pairdepth,
		'-output', output, '-prefix', sample ])
	command3 = ' '.join([ 'mv', output + '/supernova_out/supernova_out.mri.tgz', output ])
	command4 = ' '.join([ 'rm -rf', output + '/supernova_out/' ])
	command5 = ' '.join([ 'gunzip -c', output+'/'+sample+'_supernova_result.fasta.gz', '>', output + '/'+sample + '_scaffold.fa'])
	command6 = ' '.join([ 'rm -rf', output + '/*.fastq.gz'])
	command = '\n'.join([ command1, command2, command3, command4, command5, command6 ])
	return command

def lunchFunc(command):
	print(command)

def MetaAssembly(args):
	memory = args['memory']
	thread = args['thread']
	maprate = args['maprate']
	maxreads = args['maxreads']
	pairdepth = args['pairdepth']

	outdir = args['outdir']
	runnow = args['runnow']

	taxReadDepth = outdir + '/dir2_taxonomy/SSRlist/' + 'tax_reads_depth.txt'
	TaskCMD = []

	cmddir = outdir + '/all_command_shell/'
	create_folder(cmddir)
	shellfile = cmddir + '/stp3.1.MetaAssembly.sh'

	with open(shellfile, 'w') as CMDFILE:
		for tax in open(taxReadDepth, 'r').readlines():
			taxid, readnum, bareadnum, depth = tax.split()
			if float(depth) >= 300:
				readIdFile = '300X.id_' + taxid + '.allbarcode.txt'
				tssfq1 = outdir + '/dir2_taxonomy/SSRlist/' + readIdFile + '_list_1.fq.gz'
				tssfq2 = outdir + '/dir2_taxonomy/SSRlist/' + readIdFile + '_list_2.fq.gz'
				if not os.path.exists(tssfq1):
					task = supernova_assembly(tssfq1, tssfq2, memory, maprate, threads, maxreads, pairdepth, outdir, taxid)
					TaskCMD.append(task)
					CMDFILE.write('%s\n' % ( task ) )
				else:
					pass
			elif float(depth) >= 10:
				readIdFile = '10X.id_' + taxid + '.allbarcode.txt'
				tssfq1 = outdir + '/dir2_taxonomy/SSRlist/' + readIdFile + '_list_1.fq.gz'
				tssfq2 = outdir + '/dir2_taxonomy/SSRlist/' + readIdFile + '_list_2.fq.gz'
				if not os.path.exists(tssfq1):
					task = supernova_assembly(tssfq1, tssfq2, memory, maprate, threads, maxreads, pairdepth, outdir, taxid)
					TaskCMD.append(task)
					CMDFILE.write('%s\n' % ( task ) )
				else:
					pass
			else:
				pass

	if runnow:
		report_logger('###step3.1 MetaAssembly starting', cmddir + '/run.log', runnow)
		with Pool(int(threads)) as p:
			p.map(lunchFunc, TaskCMD)
		report_logger('###step3.1 MetaAssembly end', cmddir + '/run.log', runnow)

if __name__ == '__main__':

	# arguments for MetaAssembly
	parser = argparse.ArgumentParser()


	parser.add_argument('-thread',      required=False, type=str,   default='6',          	help='number of threads use(default = 6)')
	parser.add_argument('-memory',      required=False, type=str,   default='150',        	help='number of memory use(GB,default = 150)')
	parser.add_argument('-maprate',     required=False, type=str,   default='8',          	help='mapping ratio (default=8)')
	parser.add_argument('-maxreads',    required=False, type=str,   default='2140000000', 	help='maximumreads for supernova(default = 2140000000)')
	parser.add_argument('-pairdepth',   required=False, type=str,   default='2',          	help='filter less X pair barcode reads(default = 2)')

	parser.add_argument('-outdir',      required=True,  type=str,                       	help='output folder') 
	parser.add_argument('-runnow',      required=False, type=str,           				help='Run this script immediately') 

	args = vars(parser.parse_args())
	MetaAssembly(args)