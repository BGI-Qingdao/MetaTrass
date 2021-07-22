import os
from time import sleep
from datetime import datetime

# get the path to this config file
pwd_config_file = os.path.realpath(__file__)

config_file_path = '/'.join(pwd_config_file.split('/')[:-1])
config_tool_path = '/'.join(pwd_config_file.split('/')[:-2]) + '/tools/'
config_main_path = '/'.join(pwd_config_file.split('/')[:-2])

# specify full path to corresponding executables at the right side of colon
config_dict = {
               'MetaTrass'            : '%s'                       % config_main_path,

               'python'               : 'python3',
               'perl'                 : 'perl',

               # third-party tools 
               'split_barcode'        : '%s/split_barcode.pl'      % config_tool_path,
               'SOAPfilter'           : '%s/SOAPfilter'            % config_tool_path,
               'kraken'               : '%s/kraken2'               % config_tool_path,
               'TABrefiner'           : '%s/TABrefiner'            % config_tool_path,
               'seqtk'                : '%s/seqtk'                 % config_tool_path,
               'supernova'            : '%s/supernova/'            % config_tool_path,
               'quast'                : '%s/quast.py'              % config_tool_path,

               # modules
               'sflfr2supernova'      : '%s/stlfr2supernova/clean_stlfr2supernova.py'       % config_tool_path,
               'contig_purify'        : '%s/contig_purify.py'      % config_tool_path,

               # script
               'SplitBarcode'         : '%s/SplitBarcode.py'       % config_file_path,   # do not edit this line
               'GetCleandata'         : '%s/GetCleandata.py'       % config_file_path,   # do not edit this line
               'Kraken2Taxon'         : '%s/Kraken2Taxon.py'       % config_file_path,   # do not edit this line
               'TAB_refining'         : '%s/TAB_refining.py'       % config_file_path,   # do not edit this line
               'MetaAssembly'         : '%s/ReadID2Fastq.py'       % config_file_path,   # do not edit this line
               'ContigPurify'         : '%s/ReadID2Fastq.py'       % config_file_path    # do not edit this line

               }

def report_logger(message_for_report, log_file, keep_quiet):

    time_format = '[%Y-%m-%d %H:%M:%S]'
    with open(log_file, 'a') as log_handle:
        log_handle.write('%s %s\n' % ((datetime.now().strftime(time_format)), message_for_report))

    if keep_quiet:
        print('%s %s' % ((datetime.now().strftime(time_format)), message_for_report))

def create_folder(create_folder_dir):
  if os.path.exists(create_folder_dir):
    print('1')
  else:
    os.mkdir(create_folder_dir)


def remove_folder(remove_folder_dir):
    target_list = glob.glob(target_re)

    for target in target_list:

        if os.path.isdir(target) is True:
            os.system('rm -r %s' % target)

        elif os.path.isfile(target) is True:
            os.system('rm %s' % target)

