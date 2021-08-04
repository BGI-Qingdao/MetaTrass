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

def supernova_assembly(tssfq1, tssfq2, memory, maprate, thread, maxreads, pairdepth, outdir, sample):
	create_folder(outdir + 'dir3_assembly/')
	create_folder(outdir + 'dir3_assembly/supernova/')
	output = outdir + 'dir3_assembly/supernova/' + sample
	create_folder(output)

	command1 = ' '.join([ 'mkdir -p ', output, ' && cd ', output ])
	command2 = ' '.join([ config_dict['python'], config_dict['sflfr2supernova'], '-fastq1', tssfq1, '-fastq2', tssfq2, 
		'-memory', memory, '-maprate', maprate, '-thread', thread, '-maxreads', maxreads, '-pairdepth', pairdepth,
		'-outdir', output, '-prefix', sample, '-supernova', config_dict['supernova'] ])
	command3 = ' '.join([ 'mv', output + '/supernova_out/supernova_out.mri.tgz', output ])
	command4 = ' '.join([ 'rm -rf', output + '/supernova_out/' ])
	command5 = ' '.join([ 'gunzip -c', output+'/'+sample+'_supernova_result.fasta.gz', '>', output + '/'+sample + '_scaffold.fa'])
	command6 = ' '.join([ 'rm -rf', output + '/*.fastq.gz'])
	command = '\n'.join([ command1, command2, command3, command4, command5, command6 ])
	return command

def lunchFunc(command):
	os.system(command)

def MetaAssembly(args):
	memory = args['memory']
	parallel = args['parallel']
	maprate = args['maprate']
	maxreads = args['maxreads']
	pairdepth = args['pairdepth']
	max_depth = args['max_depth']
	min_depth = args['min_depth']
	outdir = args['outdir']
	runnow = args['runnow']

	taxReadDepth = outdir + '/dir2_taxonomy/SSRlist/' + 'tax_reads_depth.txt'
	TaskCMD = []

	cmddir = outdir + '/all_command_shell/'
	create_folder(cmddir)
	shellfile = cmddir + '/stp3.1.MetaAssembly.sh'

	with open(shellfile, 'w') as CMDFILE:
		if os.path.exists(taxReadDepth):
			for tax in open(taxReadDepth, 'r').readlines():
				taxid, readnum, bareadnum, depth = tax.split()
				if float(depth) >= float(max_depth):
					readIdFile = max_depth + 'X.id_' + taxid + '.allbarcode.txt'
					tssfq1 = outdir + '/dir2_taxonomy/ID2FQ/' + readIdFile + '_list_1.fq.gz'
					tssfq2 = outdir + '/dir2_taxonomy/ID2FQ/' + readIdFile + '_list_2.fq.gz'
					if os.path.exists(tssfq1):
						task = supernova_assembly(tssfq1, tssfq2, memory, maprate, '10', maxreads, pairdepth, outdir, taxid)
						TaskCMD.append(task)
						CMDFILE.write('%s\n' % ( task ) )
					else:
						pass
				elif float(depth) >= float(min_depth):
					readIdFile = min_depth +'X.id_' + taxid + '.allbarcode.txt'
					tssfq1 = outdir + '/dir2_taxonomy/ID2FQ/' + readIdFile + '_list_1.fq.gz'
					tssfq2 = outdir + '/dir2_taxonomy/ID2FQ/' + readIdFile + '_list_2.fq.gz'
					if os.path.exists(tssfq1):
						task = supernova_assembly(tssfq1, tssfq2, memory, maprate, '10', maxreads, pairdepth, outdir, taxid)
						TaskCMD.append(task)
						CMDFILE.write('%s\n' % ( task ) )
					else:
						pass
				else:
					pass
		else:
			print('!!!%s not found! Please run the step2.2 TABrefiner at first!!! ' %( taxReadDepth))

	if runnow == 'yes':
		report_logger('###step3.1 MetaAssembly starting', cmddir + '/run.log', runnow)
		with Pool(int(parallel)) as p:
			p.map(lunchFunc, TaskCMD)
		report_logger('###step3.1 MetaAssembly end', cmddir + '/run.log', runnow)
	elif runnow == 'no':
		print('this step3.1 MetaAssembly is skipped!\n')
	else:
		print('the runnow parameter is wrong with %s\n' %(runnow))


if __name__ == '__main__':

	# arguments for MetaAssembly
	parser = argparse.ArgumentParser()

	parser.add_argument('-parallel',    required=False, type=str,  default='10',          		help='number of threads use(default = 10)')
	parser.add_argument('-memory',      required=False, type=str,  default='150',        		help='number of memory use(GB,default = 150)')
	parser.add_argument('-maprate',     required=False, type=str,  default='8',          		help='mapping ratio (default=8)')
	parser.add_argument('-maxreads',    required=False, type=str,  default='2140000000', 		help='maximumreads for supernova(default = 2140000000)')
	parser.add_argument('-pairdepth',   required=False, type=str,  default='2',          		help='filter less X pair barcode reads(default = 2)')
	parser.add_argument('-max_depth',   required=False, type=str,  default = '300',             help='Species Maximum-Depth Required Assembly')
	parser.add_argument('-min_depth',   required=False, type=str,  default = '10',              help='Species Minimum-Depth Required Assembly')
	parser.add_argument('-outdir',      required=True,  type=str,                       		help='output folder') 
	parser.add_argument('-runnow',      required=True,  type=str,  default='no',                help='Set \'yes\' with launch the step immediately')

	args = vars(parser.parse_args())
	MetaAssembly(args)
