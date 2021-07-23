
import os
import argparse


from MetaTrass.ToolConfig import config_dict
from MetaTrass.ToolConfig import report_logger
from MetaTrass.ToolConfig import create_folder
from MetaTrass.ToolConfig import remove_folder

AP_usage = '''
====================================== filter_HGT example commands ======================================
# get HGTs detected at at least TWO levels
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 2
# get HGTs detected at at least THREE levels and copy their flanking region plots into a new folder
MetaCHIP filter_HGT -i NorthSea_pcofg_detected_HGTs.txt -n 3 -plot NorthSea_pcofg_Flanking_region_plots
=========================================================================================================
'''

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




def AP(args):
	

if __name__ == '__main__':

	# arguments for AP
	parser = argparse.ArgumentParser()

	parser.add_argument('-cleanfq1',           required=True,  type=str,            help='Paired-end data: cleanfq1 fastq.gz')
	parser.add_argument('-cleanfq2',           required=True,  type=str,            help='Paired-end data: cleanfq2 fastq.gz')
	parser.add_argument('-outdir',			required=True, type=str,            help='Output folder')
	parser.add_argument('-runnow',			required=False, type=str,           help='Run this script immediately') 

	args = vars(parser.parse_args())
	AP(args)