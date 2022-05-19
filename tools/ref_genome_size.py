import re, os, sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-refdir',             required=True,  type=str,        help="the single species reference fasta files stored path")

args = vars(parser.parse_args())


taxDict = {}


def callRefLength(refFile):
	with open(refFile, 'r') as RF:
		seq = {}
		for line in RF:
			if line.startswith('>'):
				name=line.replace('>','').split()[0]
				seq[name]=''
			else:
				seq[name]+=line.replace('\n','').strip()
		refLength = 0
		for key, val in seq.items():
			refLength += len(val)
		return refLength
refLEN = {}


####
#ref_genome_size.txt
#taxid	ref_length	path_to_XXX_genomic.fa
#10002	12345678	/home/database/10002_genomic.fa

filefold = {}

for filename in os.listdir(args['refdir']):
	if os.path.splitext(filename)[-1] == ".fa":
		taxid = filename.split('_')[0]
		filefold[taxid] = args['refdir']+'/'+filename
#		print( taxid, args['refdir']+'/'+filename)

with open(args['refdir']+'ref_genome_size2.txt', 'w') as f:
	for tid, fadir in filefold.items():
		ref_len = str(callRefLength(fadir))
		f.write(' '.join([taxid, ref_len, fadir, '\n']))
	f.closed()
print(f.closed)
