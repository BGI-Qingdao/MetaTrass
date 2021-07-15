
import os
import re
import glob
import argparse
import warnings
import itertools
from time import sleep
from datetime import datetime

from MetaCHIP.MetaCHIP_config import config_dict

warnings.filterwarnings("ignore")






def report_and_log(message_for_report, log_file, keep_quiet):

    time_format = '[%Y-%m-%d %H:%M:%S]'
    with open(log_file, 'a') as log_handle:
        log_handle.write('%s %s\n' % ((datetime.now().strftime(time_format)), message_for_report))

    if keep_quiet is False:
        print('%s %s' % ((datetime.now().strftime(time_format)), message_for_report))
