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

from MetaTrass import GC
from MetaTrass import TB
from MetaTrass import AP

from MetaTrass import ToolConfig

from MetaTrass import SplitBarcode
from MetaTrass import GetCleandata
from MetaTrass import Kraken2Taxon
from MetaTrass import TXACBrefiner
from MetaTrass import ReadID2Fastq
from MetaTrass import MetaAssembly
from MetaTrass import ContigPurify

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
    # subparsers = parser.add_subparsers(help="--", dest='subparser_name')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')
    


    GC_parser =              subparsers.add_parser('GC',              description='Get stLFR Cleandata',                   epilog='Example: MetaTrass GC -h')
    TB_parser =              subparsers.add_parser('TB',              description='Taxnomic and Barcoding',                epilog='Example: MetaTrass TB -h')
    AP_parser =              subparsers.add_parser('AP',              description='Assembly and Purifying',                epilog='Example: MetaTrass AP -h') 

    SplitBarcode_parser =    subparsers.add_parser('SplitBarcode',    description='split barcode',                                 )
    GetCleandata_parser =    subparsers.add_parser('GetCleandata',    description='Get Cleandata',                                  usage=GetCleandata.GetCleandata_usage)
    Kraken2Taxon_parser =    subparsers.add_parser('Kraken2Taxon',    description='Taxnomic reads by Kraken2',                      usage=Kraken2Taxon.Kraken2Taxon_usage)
    TXACBrefiner_parser =    subparsers.add_parser('TXACBrefiner',    description='Refining reads set by Taxnomic and Barcode',     usage=TXACBrefiner.TXACBrefiner)
    ReadID2Fastq_parser =    subparsers.add_parser('ReadID2Fastq',    description='Covert Read ids to Fqstq',                       usage=ReadID2Fastq.ReadID2Fastq_usage)
    MetaAssembly_parser =    subparsers.add_parser('MetaAssembly',    description='Single-species assmebly by supernova',           usage=MetaAssembly.MetaAssembly_usage)
    ContigPurify_parser =    subparsers.add_parser('ContigPurify',    description='Purifying Contigs and Scaffolds',                usage=ContigPurify.ContigPurify_usage)

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
    SplitBarcode_parser.add_argument('-rawfq1',         required=True, type=str,            help='Paired-end data: raw 1 fastq.gz ')
    SplitBarcode_parser.add_argument('-rawfq2',         required=True, type=str,            help='Paired-end data: raw 2 fastq.gz')
    SplitBarcode_parser.add_argument('-outdir',         required=True, type=str,            help='Output folder')
    SplitBarcode_parser.add_argument('-runnow',         required=False, type=str,           help='Run this script immediately') 

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

    # add argument for TXACBrefiner_parser
    TXACBrefiner_parser.add_argument('-i',                required=True,                          help='txt file containing detected HGTs, e.g. [prefix]_[ranks]_detected_HGTs.txt ')
    TXACBrefiner_parser.add_argument('-n',                required=True, type=int,                help='HGTs detected at least n levels, 2 <= n <= 5')
    TXACBrefiner_parser.add_argument('-plot',             required=False,                         help='flanking plots folder')
    TXACBrefiner_parser.add_argument('-ffn',              required=False, default=None,           help='get nucleotide sequences for qualified HGTs')
    TXACBrefiner_parser.add_argument('-faa',              required=False, default=None,           help='get amino acid sequences for qualified HGTs')

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
    ContigPurify_parser.add_argument('-i',                required=True, type=str,                  help='assembly fasta [not support fasta.gz]')
    ContigPurify_parser.add_argument('-o',                required=True, type=str,                  help='filtered fasta ')
    ContigPurify_parser.add_argument('-r',                required=True, type=str,                  help='taxid genomic reference fasta')
    ContigPurify_parser.add_argument('-q',                required=True, type=str,                  help='all_alignments.tsv by quast') 
    ContigPurify_parser.add_argument('-PCT',              required=True, type=float,                help='Threshold of contig lnegth(0-1)')
    ContigPurify_parser.add_argument('-IDY',              required=True, type=float,                help='Threshold of IDY (80 - 100)')  

    ############################## parse provided arguments and run corresponding function #############################

    # get and check options
#    args = None
    if (len(sys.argv) == 1) or (sys.argv[1] == '-h') or (sys.argv[1] == '-help') or (sys.argv[1] == '--help'):
        print_main_help()
        sys.exit(0)     

    else:
        args = vars(parser.parse_args())
    print(args)

    if args['subparser_name'] == 'GC':
        GC.GC(args, MetaTrass_config.config_dict)

    if args['subparser_name'] == 'TB':
        TB.TB(args, MetaTrass_config.config_dict)

    if args['subparser_name'] == 'AP':
        AP.AP(args)

    if args['subparser_name'] == 'SplitBarcode':
        SplitBarcode.SplitBarcode(args)

    if args['subparser_name'] == 'GetCleandata':
        GetCleandata.GetCleandata(args, MetaTrass_ToolConfig.config_dict)

    if args['subparser_name'] == 'Kraken2Taxon':
        Kraken2Taxon.Kraken2Taxon(args, MetaTrass_ToolConfig.config_dict)

    if args['subparser_name'] == 'ReadID2Fastq':
        ReadID2Fastq.ReadID2Fastq(args, MetaTrass_ToolConfig.config_dict)
        
    if args['subparser_name'] == 'TXACBrefiner':
        TXACBrefiner.TXACBrefiner(args, MetaTrass_ToolConfig.config_dict)

    if args['subparser_name'] == 'MetaAssembly':
        MetaAssembly.MetaAssembly(args, MetaTrass_ToolConfig.config_dict)

    if args['subparser_name'] == 'ContigPurify':
        ContigPurify.ContigPurify(args, MetaTrass_ToolConfig.config_dict)



