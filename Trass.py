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
    version_file = open('%s/VERSION' % ToolConfig.config_file_path)
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
       TXACBrefiner    ->  Refining read id by using Taxonomic information and superior coBarcoding set
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

    SplitBarcode_parser =    subparsers.add_parser('SplitBarcode',    description='Split Barcode',                                  usage=SplitBarcode.SplitBarcode_usage)
    GetCleandata_parser =    subparsers.add_parser('GetCleandata',    description='Get Cleandata',                                  usage=GetCleandata.GetCleandata_usage)
    Kraken2Taxon_parser =    subparsers.add_parser('Kraken2Taxon',    description='Taxnomic reads by Kraken2',                      usage=Kraken2Taxon.Kraken2Taxon_usage)
    TXACBrefiner_parser =    subparsers.add_parser('TXACBrefiner',    description='Refining reads set by Taxnomic and Barcode',     usage=TXACBrefiner.TXACBrefiner_usage)
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
    SplitBarcode_parser.add_argument('-rawfq1',             required=True,  type=str,            help='Paired-end data: raw 1 fastq.gz ')
    SplitBarcode_parser.add_argument('-rawfq2',             required=True,  type=str,            help='Paired-end data: raw 2 fastq.gz')
    SplitBarcode_parser.add_argument('-outdir',             required=True,  type=str,            help='Output folder')
    SplitBarcode_parser.add_argument('-runnow',             required=True,  type=str,            help='Run this script immediately')

    # add argument for GetCleandata_parser
    GetCleandata_parser.add_argument('-thread',             required=True,  type=str,            help='Running Thread Number')
    GetCleandata_parser.add_argument('-outdir',             required=True,  type=str,            help='Output folder')
    GetCleandata_parser.add_argument('-runnow',             required=True,  type=str,            help='Runing immediately')
    GetCleandata_parser.add_argument('-parameter',          required=False, type=str,   default='-y -F CTGTCTCTTATACACATCTTAGGAAGACAAGCACTGACGACATGA -R TCTGCTGAGTCGAGAACGTCTCTGTGAGCCAAGGAGTTGCTCTGG -p -M 2 -f -1 -Q 10',          
                                                         help='Default parameter : -y -F CTGTCTCTTATACACATCTTAGGAAGACAAGCACTGACGACATGA -R TCTGCTGAGTCGAGAACGTCTCTGTGAGCCAAGGAGTTGCTCTGG -p -M 2 -f -1 -Q 10') 

    # add argument for Kraken2Taxon_parser 
    Kraken2Taxon_parser.add_argument('-cleanfq1',           required=True,  type=str,            help='Paired-end data: cleanfq1 fastq.gz')
    Kraken2Taxon_parser.add_argument('-cleanfq2',           required=True,  type=str,            help='Paired-end data: cleanfq2 fastq.gz')
    Kraken2Taxon_parser.add_argument('-thread',             required=True,  type=str,   default = '20',            help='Kraken parameter')
    Kraken2Taxon_parser.add_argument('-sample',             required=True,  type=str,            help='Output FileName Prefix')
    Kraken2Taxon_parser.add_argument('-ref_db',             required=True,  type=str,            help='Taxonomy references database' )
    Kraken2Taxon_parser.add_argument('-outdir',             required=True,  type=str,            help='Output folder')
    Kraken2Taxon_parser.add_argument('-runnow',             required=True,  type=str,   default = 'False',         help='Run this script immediately') 
    
    # add argument for TXACBrefiner_parser
    TXACBrefiner_parser.add_argument('-kraken_file',        required=True,  type=str,            help='Paired-end data: raw 1 fastq.gz')
    TXACBrefiner_parser.add_argument('-genome_size',        required=True,  type=str,            help='Paired-end data: raw 2 fastq.gz')
    TXACBrefiner_parser.add_argument('-max_depth',          required=False, type=str,   default = '300',         help='Species Maxima-Depth Required Assembly')
    TXACBrefiner_parser.add_argument('-min_depth',          required=False, type=str,   default = '10',          help='Species Minima-Depth Required Assembly')
    TXACBrefiner_parser.add_argument('-outdir',             required=True,  type=str,            help='Output folder')
    TXACBrefiner_parser.add_argument('-runnow',             required=False, type=str,           help='Run this script immediately') 

    # add argument for ReadID2Fastq_parser
    ReadID2Fastq_parser.add_argument('-cleanfq1',           required=True,  type=str,            help='Paired-end data: cleanfq1 fastq.gz')
    ReadID2Fastq_parser.add_argument('-cleanfq2',           required=True,  type=str,            help='Paired-end data: cleanfq2 fastq.gz')
    ReadID2Fastq_parser.add_argument('-thread',             required=True,  type=str,   default = '10',            help='Number of Threads')
    ReadID2Fastq_parser.add_argument('-outdir',             required=True,  type=str,            help='Output folder')
    ReadID2Fastq_parser.add_argument('-runnow',             required=True,  type=str,   default = 'False',         help='Run this script immediately')

    # add argument for MetaAssembly_parser
    MetaAssembly_parser.add_argument('-maprate',            required=False, type=str,   default='8',          help='mapping ratio (default=8)')
    MetaAssembly_parser.add_argument('-thread',             required=False, type=str,   default='6',          help='number of threads use(default = 6)')
    MetaAssembly_parser.add_argument('-memory',             required=False, type=str,   default='150',        help='number of memory use(GB,default = 150)',)
    MetaAssembly_parser.add_argument('-maxreads',           required=False, type=str,   default='2140000000', help='maximumreads for supernova(default = 2140000000)')
    MetaAssembly_parser.add_argument('-pairdepth',          required=False, type=str,   default='2',          help='filter less X pair barcode reads(default = 2)')
    MetaAssembly_parser.add_argument('-outdir',             required=True,  type=str,                       help='output folder') 
    MetaAssembly_parser.add_argument('-runnow',             required=False, type=str,                       help='Run this script immediately') 

    # add argument for ContigPurify_parser
    ContigPurify_parser.add_argument('-PCT',                required=False, type=str,   default = '50',               help='Threshold of contig lnegth(0-1)')
    ContigPurify_parser.add_argument('-IDY',                required=False, type=str,   default = '90',               help='Threshold of IDY (80 - 100)')
    ContigPurify_parser.add_argument('-thread',             required=False, type=str,   default = '10',               help='Number of Threads')
    ContigPurify_parser.add_argument('-outdir',             required=True,  type=str,                               help='Output folder')
    ContigPurify_parser.add_argument('-ref_fa',             required=True,  type=str,                               help='Taxonomic reference genome fasta folder')
    ContigPurify_parser.add_argument('-runnow',             required=False, type=str,                               help='Run this script immediately')

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
        GetCleandata.GetCleandata(args)

    if args['subparser_name'] == 'Kraken2Taxon':
        Kraken2Taxon.Kraken2Taxon(args)

    if args['subparser_name'] == 'ReadID2Fastq':
        ReadID2Fastq.ReadID2Fastq(args)
        
    if args['subparser_name'] == 'TXACBrefiner':
        TXACBrefiner.TXACBrefiner(args)

    if args['subparser_name'] == 'MetaAssembly':
        MetaAssembly.MetaAssembly(args)

    if args['subparser_name'] == 'ContigPurify':
        ContigPurify.ContigPurify(args)



