import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

ContigPurify_usage = '''
====================================== filter_HGT example commands ======================================
# get HGTs detected at at least TWO levels
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 2
# get HGTs detected at at least THREE levels and copy their flanking region plots into a new folder
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 3 -plot NorthSea_pcofg_Flanking_region_plots
=========================================================================================================
'''


def quast_bin_for_single_fasta(shfile, quastPY, taxidbin, taxidref, threads, outdir, IDY):
    command = ' '.join([ quastPY, '-r', taxidref, '-t', str(threads), '--min-identity', str(IDY), '-o', outdir, taxidbin ])
    create_shell_script("quast_bin_for_single_fasta", shfile, command)

### filter bin after quast
def create_binfilter_sh(shfile, binFilterPY, assemblyFa, filteredFa, refGenomeFa, quastAlnTsv, IDY, PCT):
	command = ' '.join(['python', binFilterPY, '-i', assemblyFa, '-o', filteredFa, '-r', refGenomeFa, '-q', quastAlnTsv, '-IDY', IDY, '-PCT', PCT])
	create_shell_script("filter_assmbled_species_bin", shfile, command)


def filter_by_IDY_PCT(assemblyFa, filteredFa, refGenomeFa, quastAlnTsv, IDY, PCT):
	query_list = {}
	with open(quastAlnTsv, 'r') as file:
		for i in file:
			data = i.split('\t')
			if 'True' in i:
				start, end = int(data[2]), int(data[3])
				aligment_length = abs(end - start)
				name, idy = data[5], data[6]
				if name not in query_list.keys() and idy >= IDY:
					query_list[name] = aligment_length
				else:
					query_list[name] += aligment_length
	outbin = open(filteredFa, 'w')
	with open(assemblyFa, 'r') as binfasta:
		FA = binfasta.read()
		for fa in FA.split('>'):
			if len(fa.split('\n')) > 1:
				fs = fa.split('\n')
				qid, seq= fs[0], fs[1:]
				seq = ''.join(seq)
				qid = qid.split(' ')[0]
				if qid in query_list.keys():
					if len(seq) * args.per <= query_list[qid]:
						outbin.write('>' + fs[0] + '\n' + seq + '\n')
	outbin.close()

def ContigPurify(args):
	pass
if __name__ == '__main__':

	# arguments for ContigPurify
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', help='assembly fasta [not support fasta.gz]', required=True, type=str)
	parser.add_argument('-o', help='filtered fasta ', required=True, type=str)
	parser.add_argument('-r', help='taxid genomic reference fasta', required=True, type=str)
	parser.add_argument('-q', help='all_alignments.tsv by quast', required=True, type=str) 
	parser.add_argument('-PCT', help='Threshold of contig lnegth(0-1)', required=True, type=float)
	parser.add_argument('-IDY', help='Threshold of IDY (80 - 100)', required=True, type=float)

	args = vars(parser.parse_args())
	ContigPurify(args)

	assemblyFa = args.i
	filteredFa = args.o
	refGenomeFa = args.r
	quastAlnTsv = args.q
	IDY = args.IDY
	PCT = args.PCT

	filter_by_IDY_PCT( assemblyFa, filteredFa, refGenomeFa, quastAlnTsv, IDY, PCT)





