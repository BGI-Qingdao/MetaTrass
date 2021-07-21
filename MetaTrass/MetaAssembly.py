import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

MetaAssembly_usage = '''
====================================== MetaAssembly example commands ======================================

# 
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 2

=========================================================================================================
'''


def supernova_assembly(supernova_parameter, tssfq1, tssfq2, sample, outdir):
	output = outdir + 'dir3_assembly/supernova/' + sample
	command1 = ' '.join([ 'mkdir -p ', output, ' && cd ', output ])
	command2 = ' '.join([ config_dict['python'], supernovaPY, supernova_parameter, '-n', sample, '-r1', tssfq1, '-r2', tssfq2,'-o', output ])
	command3 = ' '.join([ 'mv', output + '/supernova_out/supernova_out.mri.tgz', output ])
	command4 = ' '.join([ 'rm -rf', output + '/supernova_out/' ])
	command5 = ' '.join([ 'gunzip -c', output+'/'+sample+'_supernova_result.fasta.gz', '>', output + '/'+sample + '/scaffold.fa'])
	command6 = ' '.join([ 'rm -rf', output + '/*.fastq.gz'])
	command = '\n'.join([ command1, command2, command3, command4, command5, command6 ])
	return command

def lunchFunc(command):
	print(command)

def MetaAssembly(args):
	taxReadDepth = indir + 'tax_reads_depth.txt'
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
				if os.path.exists(ssfq1):
					task = supernova_assembly(outdir, readIdFile, tssfq1, tssfq2)
					TaskCMD.append(task)
					CMDFILE.write('%s\n' % ( task ) )
				else:
					pass
			elif float(depth) >= 10:
				readIdFile = '10X.id_' + taxid + '.allbarcode.txt'
				tssfq1 = outdir + '/dir2_taxonomy/SSRlist/' + readIdFile + '_list_1.fq.gz'
				tssfq2 = outdir + '/dir2_taxonomy/SSRlist/' + readIdFile + '_list_2.fq.gz'
				if os.path.exists(ssfq1):
					task = supernova_assembly(outdir, readIdFile, tssfq1, tssfq2)
					TaskCMD.append(task)
					CMDFILE.write('%s\n' % ( task ) )
				else:
					pass
			else:
				pass

	if runnow:
		report_logger('###step3.1 MetaAssembly starting', cmddir + '/run.log', runnow)
		with Pool(thread) as p:
			p.map(lunchFunc, TaskCMD)
		report_logger('###step3.1 MetaAssembly end', cmddir + '/run.log', runnow)


if __name__ == '__main__':

	# arguments for MetaAssembly
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-thread',			required=True, type=str, 			default = '10',           	help='Number of Threads')
	parser.add_argument('-sample',			required=True, type=str,            help='Output FileName Prefix')
	parser.add_argument('-outdir',			required=True, type=str,            help='Output folder')
	parser.add_argument('-runnow',			required=False, type=str,           help='Run this script immediately') 

	args = vars(parser.parse_args())
	MetaAssembly(args)