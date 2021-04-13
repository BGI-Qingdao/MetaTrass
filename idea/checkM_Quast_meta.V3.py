import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='store all the same taxid\'s fasta [not support fasta.gz]', required=True, type=str)
parser.add_argument('-o', help='storage the output [eg. output bin_qa/bin_qa_plot]', required=True, type=str)
parser.add_argument('-quast', help='quast software path', required=True, type=str)
parser.add_argument('-taxid', help='taxid', required=True, type=str)
parser.add_argument('-classic', help='classic', required=True, type=str)
parser.add_argument('-ref', help='reference fasta', required=True, type=str)
parser.add_argument('-per', help='Threshold of contig lnegth(0-1)', required=True, type=float)
parser.add_argument('-idy', help='Threshold of IDY (80 - 100)', required=True, type=float)
args = parser.parse_args()

intaxid = args.i + '/' + args.taxid
outaxid = args.o + '/' + args.taxid + '/' + args.taxid

os.system(args.quast + '/quast.py -r ' + args.ref + ' --min-identity '  + str(args.idy) + ' -o ' + outaxid + '_Quast_Raw_Classic ' + args.classic)

os.system(args.quast + '/quast.py -r ' + args.ref + ' --min-identity '  + str(args.idy) + ' -o ' + outaxid + '_Quast_AR_IDBA-UD ' + intaxid + '/' + args.taxid + '_AR_IDBA-UD.fasta')
os.system(args.quast + '/quast.py -r ' + args.ref + ' --min-identity '  + str(args.idy) + ' -o ' + outaxid + '_Quast_AR_Supernova ' + intaxid + '/' + args.taxid + '_AR_Supernova.fasta')
os.system(args.quast + '/quast.py -r ' + args.ref + ' --min-identity '  + str(args.idy) + ' -o ' + outaxid + '_Quast_AB_IDBA-UD ' + intaxid + '/' + args.taxid + '_AB_IDBA-UD.fasta')
os.system(args.quast + '/quast.py -r ' + args.ref + ' --min-identity '  + str(args.idy) + ' -o ' + outaxid + '_Quast_AB_Supernova ' + intaxid + '/' + args.taxid + '_AB_Supernova.fasta')

def quastFilterBin(quastReport, prefix, suffix, intaxid, outaxid, rawFasta):
    query_list = {}
    with open(outaxid + prefix + quastReport, 'r') as file:
        for i in file:
            data = i.split('\t')
            if 'True' in i:
                start, end = int(data[2]), int(data[3])
                aligment_length = abs(end - start)
                name, idy = data[5], data[6]
                if name not in query_list.keys() and idy >= args.idy:
                    query_list[name] = aligment_length
                else:
                    query_list[name] += aligment_length

    outbin = open(intaxid + '/' + args.taxid + suffix, 'w')
    with open(rawFasta, 'r') as binfasta:
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

# Bin Classic filter
quastReport = 'all_alignments_' + 'CL100164780_L01_output' + '.tsv'
prefix = '_Quast_Raw_Classic/contigs_reports/'
suffix = '_Bin_Classic.fasta'
rawFasta = args.classic
quastFilterBin(quastReport, prefix, suffix, intaxid, outaxid, rawFasta)

# Bin AR IDBA-UD filter
quastReport = 'all_alignments_'+ args.taxid + '_AR_IDBA_UD' + '.tsv'
prefix = '_Quast_AR_IDBA-UD/contigs_reports/'
suffix = '_AR_IDBA-UD_Filt.fasta'
rawFasta = intaxid + '/' + args.taxid + '_AR_IDBA-UD.fasta'
if os.path.exists( outaxid + prefix + quastReport ):
    quastFilterBin(quastReport, prefix, suffix, intaxid, outaxid, rawFasta)
else:
    pass
# Bin AB IDBA-UD filter
quastReport = 'all_alignments_'+ args.taxid + '_AB_IDBA_UD' + '.tsv'
prefix = '_Quast_AB_IDBA-UD/contigs_reports/'
suffix = '_AB_IDBA-UD_Filt.fasta'
rawfasta = intaxid + '/' + args.taxid + '_AB_IDBA-UD.fasta'
if os.path.exists( outaxid + prefix + quastReport ):
    quastFilterBin(quastReport, prefix, suffix, intaxid, outaxid, rawFasta)
else:
    pass

# Bin AR Supernova filter
quastReport = 'all_alignments_'+ args.taxid + '_AR_Supernova' + '.tsv'
prefix = '_Quast_AR_Supernova/contigs_reports/'
suffix = '_AR_Supernova_Filt.fasta'
rawFasta = intaxid + '/' + args.taxid + '_AR_Supernova.fasta'
if os.path.exists( outaxid + prefix + quastReport ):
    quastFilterBin(quastReport, prefix, suffix, intaxid, outaxid, rawFasta)
else:
    pass

# Bin AB Supernova filter
quastReport = 'all_alignments_'+ args.taxid + '_AB_Supernova' + '.tsv'
prefix = '_Quast_AB_Supernova/contigs_reports/'
suffix = '_AB_Supernova_Filt.fasta'
rawFasta = intaxid + '/' + args.taxid + '_AB_Supernova.fasta'
if os.path.exists( outaxid + prefix + quastReport ):
    quastFilterBin(quastReport, prefix, suffix, intaxid, outaxid, rawFasta)
else:
    pass

os.system(args.quast + '/quast.py -r ' + args.ref + ' -o ' + outaxid + '_Quast_Bin_Classic ' + intaxid + '/' + args.taxid + '_Bin_Classic.fasta')

os.system(args.quast + '/quast.py -r ' + args.ref + ' -o ' + outaxid + '_Quast_AR_IDBA-UD_Filt ' + intaxid + '/' + args.taxid + '_AR_IDBA-UD_Filt.fasta')
os.system(args.quast + '/quast.py -r ' + args.ref + ' -o ' + outaxid + '_Quast_AR_Supernova_Filt ' + intaxid + '/' + args.taxid + '_AR_Supernova_Filt.fasta')
os.system(args.quast + '/quast.py -r ' + args.ref + ' -o ' + outaxid + '_Quast_AB_IDBA-UD_Filt ' + intaxid + '/' + args.taxid + '_AB_IDBA-UD_Filt.fasta')
os.system(args.quast + '/quast.py -r ' + args.ref + ' -o ' + outaxid + '_Quast_AB_Supernova_Filt ' + intaxid + '/' + args.taxid + '_AB_Supernova_Filt.fasta')

os.system('source /zfsqd1/ST_OCEAN/USRS/st_ocean/MetaWRAP/source.sh')

os.system('checkm lineage_wf -f ' +  outaxid + '_checkM_qa.txt '+ ' -t 20 -x fasta ' + intaxid + ' '+ outaxid )
os.system('checkm bin_qa_plot --image_type pdf -x fasta ' + outaxid + ' ' + intaxid + ' ' + outaxid + '_checkM_qa_plots' )
os.system('mv ' + outaxid + '_checkM_qa_plots/bin_qa_plot.pdf ' + outaxid + '_checkM_qa_plot.pdf')

