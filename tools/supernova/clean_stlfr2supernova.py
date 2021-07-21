import argparse
import os

config_file_pwd = os.path.realpath(__file__)

parser = argparse.ArgumentParser()
parser.add_argument('-r1', help='stlfr clean reads1', required=True, type=str)
parser.add_argument('-r2', help='stlfr clean reads2', required=True, type=str)
parser.add_argument('-supernova', help='supernova soft path', required=True, type=str)
parser.add_argument('-o', help='output folder', required=False, type=str)
parser.add_argument('-f', help='filter less X pair barcode reads(default = 2)', default=2, required=False, type=int)
parser.add_argument('-m', help='mapping ratio (default=8)', default=8, required=False, type=int)
parser.add_argument('-n', help='output prefix', required=True, type=str)
parser.add_argument('-t', help='number of threads use(default = 6)', default=6, required=False, type=int)
parser.add_argument('-g', help='number of memory use(GB,default = 150)', default=150, required=False, type=int)
parser.add_argument('-x', help='maxreads for supernova(default = 2140000000)', default=2140000000, required=False, type=int)
args = parser.parse_args()
thread=str(args.t)
memory=str(args.g)
maxreads=str(args.x)
filter_num = args.f
mapratio_num = args.m
if os.listdir(args.o):
    os.system('rm -rf '+args.o+'/*')
os.system('ln -s ' + args.r1 +' '+ args.o+'/split_reads.1.fq.gz.clean.gz')
os.system('ln -s ' + args.r2 +' '+ args.o+'/split_reads.2.fq.gz.clean.gz')
os.system('/bin/sh ' + config_file_pwd + 'shell_barcode')
wl = args.supernova + '/supernova-cs/*/tenkit/lib/python/tenkit/barcodes/4M-with-alts-february-2016.txt'
os.system('perl ' + config_file_pwd + 'merge_barcodes.pl barcode_clean_freq.txt ' + wl + ' merge.txt ' + str(filter_num) + ' ' + str(mapratio_num) +' 1> merge_barcode.log  2>merge_barcode.err')
os.system('perl ' + config_file_pwd + 'fake_10x.pl ' + args.r1 + ' ' + args.r2 + ' merge.txt >fake_10X.log 2>fake_10X.err')
os.system('mv read-I1_si-TTCACGCG_lane-001-chunk-001.fastq.gz ' + args.o + '/sample_S1_L001_I1_001.fastq.gz')
os.system('mv read-R1_si-TTCACGCG_lane-001-chunk-001.fastq.gz ' + args.o + '/sample_S1_L001_R1_001.fastq.gz')
os.system('mv read-R2_si-TTCACGCG_lane-001-chunk-001.fastq.gz ' + args.o + '/sample_S1_L001_R2_001.fastq.gz')
os.system('mv *.log ' + args.o)
os.system('mv *.err ' + args.o)
print( 'fake over' )
os.system(args.supernova + 'supernova run --id=supernova_out --maxreads='+maxreads+' --fastqs=' + args.o + ' --accept-extreme-coverage --localcores='+thread+' --localmem='+memory+' --nopreflight 1>_log 2>_err')
os.system(args.supernova + 'supernova mkoutput --style=pseudohap --asmdir=supernova_out/outs/assembly --outprefix='+args.n+'_supernova_result')
print( 'pip line over')
