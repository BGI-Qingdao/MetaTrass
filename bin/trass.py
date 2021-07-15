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

import MetaTrass.ToolConfig as ToolConfig

import MetaTrass.SplitBarcode as SplitBarcode
import MetaTrass.GetCleandata as GetCleandata
import MetaTrass.Kraken2Taxon as Kraken2Taxon
import MetaTrass.TAB_refining as TAB_refining
import MetaTrass.ReadID2Fastq as ReadID2Fastq
import MetaTrass.MetaAssembly as MetaAssembly
import MetaTrass.ContigPurify as ContigPurify

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

    # add arguments for GC_parser
    GC_parser.add_argument('-i',       required=True,                       help='input genome folder')
    GC_parser.add_argument('-o',       required=False,                      help='taxonomic classification of input genomes')
    GC_parser.add_argument('-p',       required=True,                       help='output prefix')
    GC_parser.add_argument('-r',       required=False, default=None,        help='grouping rank, choose from p (phylum), c (class), o (order), f (family), g (genus) or any combination of them')

    # add arguments for TB_parser
    TB_parser.add_argument('-p',             required=True,                                help='output prefix')
    TB_parser.add_argument('-r',             required=False, default=None,                 help='grouping rank')
    TB_parser.add_argument('-g',             required=False, default=None,                 help='grouping file')
    TB_parser.add_argument('-cov',           required=False, type=int,     default=75,     help='coverage cutoff, default: 75')
    TB_parser.add_argument('-al',            required=False, type=int,     default=200,    help='alignment length cutoff, default: 200')
    TB_parser.add_argument('-flk',           required=False, type=int,     default=10,     help='the length of flanking sequences to plot (Kbp), default: 10')
    TB_parser.add_argument('-ip',            required=False, type=int,     default=90,     help='identity percentile cutoff, default: 90')

    # add arguments for AP_parser
    AP_parser.add_argument('-p',             required=True,                                help='output prefix')
    AP_parser.add_argument('-r',             required=False, default=None,                 help='grouping rank')
    AP_parser.add_argument('-g',             required=False, default=None,                 help='grouping file')
    AP_parser.add_argument('-cov',           required=False, type=int,     default=75,     help='coverage cutoff, default: 75')
    AP_parser.add_argument('-al',            required=False, type=int,     default=200,    help='alignment length cutoff, default: 200')
    AP_parser.add_argument('-flk',           required=False, type=int,     default=10,     help='the length of flanking sequences to plot (Kbp), default: 10')
    AP_parser.add_argument('-ip',            required=False, type=int,     default=90,     help='identity percentile cutoff, default: 90')

    # add arguments for SplitBarcode_parse
    SplitBarcode_parser.add_argument('-i',                required=True,                          help='txt file containing detected HGTs, e.g. [prefix]_[ranks]_detected_HGTs.txt ')
    SplitBarcode_parser.add_argument('-n',                required=True, type=int,                help='HGTs detected at least n levels, 2 <= n <= 5')
    SplitBarcode_parser.add_argument('-plot',             required=False,                         help='flanking plots folder')
    SplitBarcode_parser.add_argument('-ffn',              required=False, default=None,           help='get nucleotide sequences for qualified HGTs')
    SplitBarcode_parser.add_argument('-faa',              required=False, default=None,           help='get amino acid sequences for qualified HGTs')

    # add argument for GetCleandata_parser
    GetCleandata_parser.add_argument('-i',                required=True,                          help='txt file containing detected HGTs, e.g. [prefix]_[ranks]_detected_HGTs.txt ')
    GetCleandata_parser.add_argument('-n',                required=True, type=int,                help='HGTs detected at least n levels, 2 <= n <= 5')
    GetCleandata_parser.add_argument('-plot',             required=False,                         help='flanking plots folder')
    GetCleandata_parser.add_argument('-ffn',              required=False, default=None,           help='get nucleotide sequences for qualified HGTs')
    GetCleandata_parser.add_argument('-faa',              required=False, default=None,           help='get amino acid sequences for qualified HGTs')

    # add argument for Kraken2Taxon_parser 
    Kraken2Taxon_parser.add_argument('-i',                required=True,                          help='txt file containing detected HGTs, e.g. [prefix]_[ranks]_detected_HGTs.txt ')
    Kraken2Taxon_parser.add_argument('-n',                required=True, type=int,                help='HGTs detected at least n levels, 2 <= n <= 5')
    Kraken2Taxon_parser.add_argument('-plot',             required=False,                         help='flanking plots folder')
    Kraken2Taxon_parser.add_argument('-ffn',              required=False, default=None,           help='get nucleotide sequences for qualified HGTs')
    Kraken2Taxon_parser.add_argument('-faa',              required=False, default=None,           help='get amino acid sequences for qualified HGTs')

    # add argument for TAB_refining_parser
    TAB_refining_parser.add_argument('-i',                required=True,                          help='txt file containing detected HGTs, e.g. [prefix]_[ranks]_detected_HGTs.txt ')
    TAB_refining_parser.add_argument('-n',                required=True, type=int,                help='HGTs detected at least n levels, 2 <= n <= 5')
    TAB_refining_parser.add_argument('-plot',             required=False,                         help='flanking plots folder')
    TAB_refining_parser.add_argument('-ffn',              required=False, default=None,           help='get nucleotide sequences for qualified HGTs')
    TAB_refining_parser.add_argument('-faa',              required=False, default=None,           help='get amino acid sequences for qualified HGTs')

    # add argument for ReadID2Fastq_parser
    ReadID2Fastq_parser.add_argument('-i',                required=True,                          help='txt file containing detected HGTs, e.g. [prefix]_[ranks]_detected_HGTs.txt ')
    ReadID2Fastq_parser.add_argument('-n',                required=True, type=int,                help='HGTs detected at least n levels, 2 <= n <= 5')
    ReadID2Fastq_parser.add_argument('-plot',             required=False,                         help='flanking plots folder')
    ReadID2Fastq_parser.add_argument('-ffn',              required=False, default=None,           help='get nucleotide sequences for qualified HGTs')
    ReadID2Fastq_parser.add_argument('-faa',              required=False, default=None,           help='get amino acid sequences for qualified HGTs')

    # add argument for MetaAssembly_parser
    MetaAssembly_parser.add_argument('-i',                required=True,                          help='txt file containing detected HGTs, e.g. [prefix]_[ranks]_detected_HGTs.txt ')
    MetaAssembly_parser.add_argument('-n',                required=True, type=int,                help='HGTs detected at least n levels, 2 <= n <= 5')
    MetaAssembly_parser.add_argument('-plot',             required=False,                         help='flanking plots folder')
    MetaAssembly_parser.add_argument('-ffn',              required=False, default=None,           help='get nucleotide sequences for qualified HGTs')
    MetaAssembly_parser.add_argument('-faa',              required=False, default=None,           help='get amino acid sequences for qualified HGTs')

    # add argument for ContigPurify_parser
    ContigPurify_parser.add_argument('-i',                required=True,                          help='txt file containing detected HGTs, e.g. [prefix]_[ranks]_detected_HGTs.txt ')
    ContigPurify_parser.add_argument('-n',                required=True, type=int,                help='HGTs detected at least n levels, 2 <= n <= 5')
    ContigPurify_parser.add_argument('-plot',             required=False,                         help='flanking plots folder')
    ContigPurify_parser.add_argument('-ffn',              required=False, default=None,           help='get nucleotide sequences for qualified HGTs')
    ContigPurify_parser.add_argument('-faa',              required=False, default=None,           help='get amino acid sequences for qualified HGTs')



    ############################## parse provided arguments and run corresponding function #############################

    # get and check options
    args = None
    if (len(sys.argv) == 1) or (sys.argv[1] == '-h') or (sys.argv[1] == '-help') or (sys.argv[1] == '--help'):
        print_main_help()
        sys.exit(0)

    else:
        args = vars(parser.parse_args())

    if args['subparser_name'] == 'GC':
        GC(args, MetaTrass_config.config_dict)

    if args['subparser_name'] == 'TB':
        TB(args, MetaCHIP_config.config_dict)

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
