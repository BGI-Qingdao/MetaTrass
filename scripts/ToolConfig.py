import os

# extract path to this config file
pwd_config_file = os.path.realpath(__file__)
config_file_path = '/'.join(pwd_config_file.split('/')[:-1])


# specify full path to corresponding executables at the right side of colon
config_dict = {'python'               : 'python3',
               'perl'                 : 'perl',
               'split_barcode'        : 'split_barcode.pl',
               'SOAPfilter'           : 'SOAPfilter',
               'kraken'               : 'kraken2',
               'seqtk'                : 'seqtk',
               'sflfr2supernova'      : 'stlfr2supernova',
               'quast'                : 'quast',
               'SplitBarcode'    : '%s/SplitBarcode.py'  % config_file_path,   # do not edit this line
               'GetCleandata'    : '%s/GetCleandata.py'  % config_file_path,   # do not edit this line
               'Kraken2Taxon'    : '%s/Kraken2Taxon.py'  % config_file_path,   # do not edit this line
               'TAB_refining'    : '%s/TAB_refining.py'  % config_file_path,   # do not edit this line
               'MetaAssembly'    : '%s/ReadID2Fastq.py'  % config_file_path,   # do not edit this line
               'ContigPurify'    : '%s/ReadID2Fastq.py'  % config_file_path    # do not edit this line

               }


def report_logger(message_for_report, log_file, keep_quiet):

    time_format = '[%Y-%m-%d %H:%M:%S]'
    with open(log_file, 'a') as log_handle:
        log_handle.write('%s %s\n' % ((datetime.now().strftime(time_format)), message_for_report))

    if keep_quiet is False:
        print('%s %s' % ((datetime.now().strftime(time_format)), message_for_report))


def create_folder(create_folder_dir):
    if os.path.isdir(folder_to_create):
        shutil.rmtree(folder_to_create, ignore_errors=True)
        if os.path.isdir(folder_to_create):
            shutil.rmtree(folder_to_create, ignore_errors=True)
            if os.path.isdir(folder_to_create):
                shutil.rmtree(folder_to_create, ignore_errors=True)
                if os.path.isdir(folder_to_create):
                    shutil.rmtree(folder_to_create, ignore_errors=True)
    os.mkdir(folder_to_create)


def remove_folder(remove_folder_dir):
    target_list = glob.glob(target_re)

    for target in target_list:

        if os.path.isdir(target) is True:
            os.system('rm -r %s' % target)

        elif os.path.isfile(target) is True:
            os.system('rm %s' % target)

