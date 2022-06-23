import os
import argparse

def contig_purify(args):
	rawContig = args['rawContig']
	purifySeq = args['purifySeq']
	quastAlnTsv = args['quastAlnTsv']
	IDY = args['IDY']
	PCT = args['PCT']
	query_list = {}
	with open(quastAlnTsv, 'r') as file:
		for i in file:
			data = i.split('\t')
			if 'True' in i:
				start, end = int(data[2]), int(data[3])
				aligment_length = abs(end - start)
				name, idy = data[5], data[6]
				if name not in query_list.keys() and float(idy) >= float(IDY):
					query_list[name] = aligment_length
				else:
					query_list[name] += aligment_length
	AF = float(PCT) / 100
	outbin = open(purifySeq, 'w')
	with open(rawContig, 'r') as binfasta:
		FA = binfasta.read()
		for fa in FA.split('>'):
			if len(fa.split('\n')) > 1:
				fs = fa.split('\n')
				qid, seq= fs[0], fs[1:]
				seq = ''.join(seq)
				qid = qid.split(' ')[0]
				if qid in query_list.keys():
					if len(seq) * AF <= query_list[qid]:
						outbin.write('>' + fs[0] + '\n' + seq + '\n')
	outbin.close()


if __name__ == '__main__':

	# arguments for ContigPurify
	parser = argparse.ArgumentParser()
	parser.add_argument('-rawContig',		required=True, 	 type=str,	help='Purifyed fasta ')
	parser.add_argument('-purifySeq',		required=True, 	 type=str, 	help='taxid genomic reference fasta')
	parser.add_argument('-quastAlnTsv',		required=True, 	 type=str, 	help='taxid genomic reference fasta')

	parser.add_argument('-PCT', 			required=False,  type=str,  default = '50',	  help='Threshold of contig lnegth(0-1)')
	parser.add_argument('-IDY', 			required=False,  type=str, 	default = '90',   help='Threshold of IDY (80 - 100)')
	args = vars(parser.parse_args())
	contig_purify(args)
