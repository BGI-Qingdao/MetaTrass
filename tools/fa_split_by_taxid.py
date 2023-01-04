import re, os, sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-reffna',             required=True,  type=str,                               help='must be followed the kraken reference file format: library.fna. Each fasta query name should be set as ">kraken:taxid|400667|SpeciesName"')
parser.add_argument('-outdir',             required=True,  type=str,                               help='Output folder: each species fasta file name should be contained taxid and "_genomic.fa"')

args = vars(parser.parse_args())


fna = open(args['reffna'])

FA = fna.read()
taxid = '4302'

outfa = args['outdir'] +'/'+taxid+'_genomic.fa'
OUTFA = open(outfa, 'a')
for i in FA.split('\n>'):
	j = i.split('\n')
	k = j[0].split('|')[1]
#	k = t[1]
	if taxid == k:
		outfa =  args['outdir'] +'/'+taxid+'_genomic.fa'
		OUTFA = open(outfa, 'a+')
		OUTFA.write('>'+i + '\n')
	else:
		OUTFA.close()
		taxid = k	
		outfa =  args['outdir'] +'/'+taxid+'_genomic.fa'
		OUTFA = open(outfa, 'a')
		OUTFA.write('>'+i+'\n')
