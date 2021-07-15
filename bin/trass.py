#!/usr/bin/env python3

# Copyright (C) 2021, Yanwei Qi, Lidong Guo.
# qiyanwei1@genomics.cn, or qiyanweii@icloud.com.

# MetaTrass is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# MetaTrass is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import argparse

import MetaTrass.GC as GC
import MetaTrass.TB as TB
import MetaTrass.AP as AP

def version():
    version_file = open('%s/VERSION' % MetaTrass_config.config_file_path)
    return version_file.readline().strip()


def print_main_help():

    help_message = ''' 
            ...:::=== MetaTrass v%s ===:::...
        
    Core modules:
       GC              ->  Get stLFR Cleandata 
       TB              ->  Taxonomic Reads And Co-Barcoding Reads Refining (TABrefiner) 
       AP              ->  Single-species Assembly and Contigs Purifying

    Supplementary modules:
       SplitBarcode    ->  Covert barcode sequences to digital code
       GetCleandata    ->  Cleandata filtered by SOAPfilter
       Kraken2Taxon    ->  Taxonomic total reads under references database by Kraken
       TAB_refining    ->  Refining read id by using Taxonomic information and superior coBarcoding set
       ReadID2Fastq    ->  Covert the refined read id from total fastq to each speices
       MetaAssembly    ->  Co-barcoding genome assembly by using SUPERNOVA
       ContigPurify    ->  Purifying the initial assembly sequences to the final MAG based on the references

    # for command specific help info
    MetaTrass GC -h
    MetaTrass TB -h
    MetaTrass AP -h
    
    ''' % version()

    print(help_message)

if __name__ == '__main__':

    ############################################## initialize subparsers ###############################################

    # initialize the options parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="--", dest='subparser_name')

    GC_parser =              subparsers.add_parser('GC',              description='Get stLFR Cleandata',                   epilog='Example: MetaTrass GC -h')
    TB_parser =              subparsers.add_parser('TB',              description='Taxnomic and Barcoding',                epilog='Example: MetaTrass TB -h')
    AP_parser =              subparsers.add_parser('AP',              description='Assembly and Purifying',                epilog='Example: MetaTrass AP -h') 

    SplitBarcode_parser =    subparsers.add_parser('SplitBarcode',    description=' ',                                     usage=filter_HGT.filter_HGT_usage)
    GetCleandata_parser =    subparsers.add_parser('GetCleandata',    description='update hmm profiles',                   usage=update_hmms.update_hmms_usage)
    Kraken2Taxon_parser =    subparsers.add_parser('Kraken2Taxon',    description='get SCG tree',                          usage=get_SCG_tree.get_SCG_tree_usage)
    TAB_refining_parser =    subparsers.add_parser('TAB_refining',    description='rename sequences in a file',            usage=rename_seqs.rename_seqs_usage)
    ReadID2Fastq_parser =    subparsers.add_parser('ReadID2Fastq',    description='rename sequences in a file',            usage=rename_seqs.rename_seqs_usage)
    MetaAssembly_parser =    subparsers.add_parser('MetaAssembly',    description='rename sequences in a file',            usage=rename_seqs.rename_seqs_usage)
    ContigPurify_parser =    subparsers.add_parser('ContigPurify',    description='rename sequences in a file',            usage=rename_seqs.rename_seqs_usage)

    ######################################### define arguments for subparsers ##########################################

    # add arguments for PI_parser
    GC_parser.add_argument('-i',       required=True,                       help='input genome folder')
    GC_parser.add_argument('-o',       required=False,                      help='taxonomic classification of input genomes')
    GC_parser.add_argument('-p',       required=True,                       help='output prefix')
    GC_parser.add_argument('-r',       required=False, default=None,        help='grouping rank, choose from p (phylum), c (class), o (order), f (family), g (genus) or any combination of them')
    PI_parser.add_argument('-g',       required=False, default=None,        help='grouping file')
    PI_parser.add_argument('-x',       required=False, default='fasta',     help='file extension')
    PI_parser.add_argument('-nonmeta', required=False, action="store_true", help='provide if input genomes are NOT metagenome-assembled genomes')
    PI_parser.add_argument('-t',       required=False, type=int, default=1, help='number of threads, default: 1')
    PI_parser.add_argument('-quiet',   required=False, action="store_true", help='not report progress')
    PI_parser.add_argument('-force',   required=False, action="store_true", help='force overwrite existing results')
    PI_parser.add_argument('-noblast', required=False, action="store_true", help='skip running all-vs-all blastn, provide if you have other ways (e.g. with job scripts) to speed up the blastn step')

    # add arguments for BP_parser
    BP_parser.add_argument('-p',             required=True,                                help='output prefix')
    BP_parser.add_argument('-r',             required=False, default=None,                 help='grouping rank')
    BP_parser.add_argument('-g',             required=False, default=None,                 help='grouping file')
    BP_parser.add_argument('-cov',           required=False, type=int,     default=75,     help='coverage cutoff, default: 75')
    BP_parser.add_argument('-al',            required=False, type=int,     default=200,    help='alignment length cutoff, default: 200')
    BP_parser.add_argument('-flk',           required=False, type=int,     default=10,     help='the length of flanking sequences to plot (Kbp), default: 10')
    BP_parser.add_argument('-ip',            required=False, type=int,     default=90,     help='identity percentile cutoff, default: 90')
    BP_parser.add_argument('-ei',            required=False, type=float,   default=80,     help='end match identity cutoff, default: 80')
    BP_parser.add_argument('-t',             required=False, type=int,     default=1,      help='number of threads, default: 1')
    BP_parser.add_argument('-NoEbCheck',     required=False, action="store_true",          help='disable end break and contig match check for fast processing, not recommend for metagenome-assembled genomes (MAGs)')
    BP_parser.add_argument('-force',         required=False, action="store_true",          help='overwrite previous results')
    BP_parser.add_argument('-quiet',         required=False, action="store_true",          help='Do not report progress')
    BP_parser.add_argument('-tmp',           required=False, action="store_true",          help='keep temporary files')

    # add arguments for filter_HGT_parser
    filter_HGT_parser.add_argument('-i',                required=True,                          help='txt file containing detected HGTs, e.g. [prefix]_[ranks]_detected_HGTs.txt ')
    filter_HGT_parser.add_argument('-n',                required=True, type=int,                help='HGTs detected at least n levels, 2 <= n <= 5')
    filter_HGT_parser.add_argument('-plot',             required=False,                         help='flanking plots folder')
    filter_HGT_parser.add_argument('-ffn',              required=False, default=None,           help='get nucleotide sequences for qualified HGTs')
    filter_HGT_parser.add_argument('-faa',              required=False, default=None,           help='get amino acid sequences for qualified HGTs')

    # add arguments for update_hmm
    update_hmms_parser.add_argument('-hmm',             required=True,                          help='MetaCHIP_phylo.hmm file')
    update_hmms_parser.add_argument('-p_db',            required=False, default=None,           help='Pfam db file, e.g. Pfam-A.hmm')
    update_hmms_parser.add_argument('-t_db',            required=False, default=None,           help='TIGRFAMs db folder, e.g. TIGRFAMs_14.0_HMM')

    # add arguments for get_SCG_tree
    get_SCG_tree_parser.add_argument('-i',              required=True,                          help='input genome folder')
    get_SCG_tree_parser.add_argument('-p',              required=True,                          help='output prefix')
    get_SCG_tree_parser.add_argument('-x',              required=False, default='fasta',        help='file extension')
    get_SCG_tree_parser.add_argument('-nonmeta',        required=False, action="store_true",    help='annotate Non-metagenome-assembled genomes (Non-MAGs)')
    get_SCG_tree_parser.add_argument('-t',              required=False, type=int, default=1,    help='number of threads, default: 1')

    # add arguments for rename_seqs
    rename_seqs_parser.add_argument('-in',         required=True,                          help='input sequence file')
    rename_seqs_parser.add_argument('-inc_suffix', required=False, action="store_true",    help='rename sequences by incrementally adding suffix to file name')
    rename_seqs_parser.add_argument('-sep_in',     required=False, default=None,           help='separator for input sequences')
    rename_seqs_parser.add_argument('-sep_out',    required=False, default=None,           help='separator for output sequences, default: same as sep_in')
    rename_seqs_parser.add_argument('-n',          required=False, default=None, type=int, help='the number of columns to keep')
    rename_seqs_parser.add_argument('-prefix',     required=False, default=None,           help='add prefix to sequence')
    rename_seqs_parser.add_argument('-x',          required=False,                         help='file extension')


    ############################## parse provided arguments and run corresponding function #############################

    # get and check options
    args = None
    if (len(sys.argv) == 1) or (sys.argv[1] == '-h') or (sys.argv[1] == '-help') or (sys.argv[1] == '--help'):
        print_main_help()
        sys.exit(0)

    else:
        args = vars(parser.parse_args())

    if args['subparser_name'] == 'PI':
        PI(args, MetaCHIP_config.config_dict)

    if args['subparser_name'] == 'BP':
        BP(args, MetaCHIP_config.config_dict)

    if args['subparser_name'] == 'filter_HGT':
        filter_HGT.filter_HGT(args)

    if args['subparser_name'] == 'update_hmms':
        update_hmms.update_hmms(args)

    if args['subparser_name'] == 'get_SCG_tree':
        get_SCG_tree.get_SCG_tree(args, MetaCHIP_config.config_dict)

    if args['subparser_name'] == 'rename_seqs':
        rename_seqs.rename_seqs(args)

    # if args['subparser_name'] == 'circos_HGT':
    #     circos_HGT.circos_HGT(args, MetaCHIP_config.config_dict)

'''
cd /Users/songweizhi/PycharmProjects/MetaCHIP
rm -r build
rm -r dist
rm -r MetaCHIP.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*
songweizhi

pip install --upgrade MetaCHIP
pip install --upgrade -i https://test.pypi.org/simple/ MetaCHIP

'''
