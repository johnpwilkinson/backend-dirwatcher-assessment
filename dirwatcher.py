import sys
import argparse
import os
import logging
import time
import signal
from blessings import Terminal

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s:%(message)s:')
logger = logging.getLogger(__name__)

dir_dict = {}
init_time = time.time()
exit_flag = False

t = Terminal()
w = t.width
g = t.green


def get_directory_structure(argz):
    """
    Creates a dictionary that represents the
    contents of the target dir
    """
    flash_dict = {}
    try:
        if os.path.isdir(argz.dirname[0]):
            for dir_content in os.walk(argz.dirname[0]):
                files = dir_content[2]
            for file in files:
                if file.endswith(argz.extname[0]):
                    flash_dict.setdefault(file, [])
        else:
            logger.info(f"{argz.dirname[0]} does not exist ")
    except Exception as e:
        logger.exception(f"Alert! {e}")
    compare_dict_sizes(flash_dict, argz)


def compare_dict_sizes(flash_dict, argz):
    """
    Compares flash_dict to dir_dict to determine if the size of the
    dict has changed... and if so, in what way.
    """
    try:
        for flash_file in flash_dict:
            if flash_file not in dir_dict:
                logger.info(
                    f"{g}{flash_file} has been added to {argz.dirname[0]}")
                dir_dict[flash_file] = []
        for actualfile in list(dir_dict):
            if actualfile not in flash_dict:
                logger.info(
                    f"{g}{actualfile} has been removed from {argz.dirname[0]}")
                del dir_dict[actualfile]
    except Exception as e:
        logger.exception(f"Alert! {e}")
    scan_for_magic_text(argz)


def scan_for_magic_text(argz):
    """
    Scans the files for instances of the magic text
    """
    try:
        for file in dir_dict:
            with open(argz.dirname[0]+"/"+file, "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if argz.magic_text[0] in line:
                        if i not in dir_dict[file]:
                            dir_dict[file].append(i)
                            logger.info(
                                f"{g}magic text in {file} @ line {str(i+1)}")
    except Exception as e:
        logger.exception(f"Alert! {e}")


def create_parser():
    """Command Line Parser"""
    parser = argparse.ArgumentParser(
        prog='dir_watcher',
        description='Watches Dirs for magic strings',
        usage='%(prog)s [options]',
        epilog="Lookin for those magic strings")
    parser.add_argument('dirname', help='What Dir to watch?', nargs='+')
    parser.add_argument(
        'magic_text', help='What is the magic text?', nargs='+')
    parser.add_argument('--extname', default='.txt',
                        help='What type of file?', nargs='+')
    parser.add_argument('--how_often', default=1,
                        help='How long between scans?',
                        nargs='+')
    return parser


def signal_handler(sig_num, frame):
    """
     This is a handler for SIGTERM and SIGINT. Other signals can be mapped
    here as well. Basically, it just sets a global flag, and main() will
    exit its loop if the signal is trapped.
    """
    global exit_flag
    run_time = time.time() - init_time
    message = "Dir_Watcher Terminating"
    r = f"Run Time was {run_time}"
    b = t.bold_red
    logger.info(
        f"{b}\n{'$'*w}\n{message.center(int(w))}\n{r.center(int(w))}\n{'$'*w}")
    exit_flag = True


def main(args):
    """executes Dir watcher, logs errors, and listens for OS Signals"""
    message = "Dir_Watcher Initialized"
    logger.info(
        f"{t.bold_green}\n{'$'*w}\n{message.center(int(w))}\n{'$'*w}\n")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    parser = create_parser()
    argz = parser.parse_args(args)
    polling_interval = argz.how_often

    while not exit_flag:
        try:
            get_directory_structure(argz)
        except Exception as e:
            logger.exception(f"Alert! {e}")
            get_directory_structure([])
        time.sleep(polling_interval)


if __name__ == '__main__':
    main(sys.argv[1:])
