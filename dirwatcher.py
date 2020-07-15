import signal
import time
import argparse
import os
import logging


exit_flag = False



dir_files = {}

def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name
    logger.warn('Received ' + signal.Signals(sig_num).name)
    exit_flag = True

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    for path, dirs, files in os.walk(rootdir):
       for file in files:
           if file not in dir.keys():
               dir[file] = 1
    print(dir)
    return dir

def scan_single_file(file_to_scan, magic_text):
    """function to scan a single file for the 'magic string'"""
    with open(file_to_scan) as f:
        datafile = f.readlines()
        for line_index, line in enumerate(datafile):
            if magic_text in line:
                # print("true")
                # if file is not in the 
                if file_to_scan not in dir_files.keys():
                    dir_files[file_to_scan] = line_index
                if file_to_scan in dir_files.keys() and line_index >= dir_files[file_to_scan]
                    dir_files[file_to_scan] +=1

detect_added_files():
    pass
detect_removed_files():
    pass
watch_directory():
    pass
def magic_text_locator(dir, extension, magic_text):

    pass

def dir_watcher_parser(args):
    """This is the functions that creates the argument parser. In the past this 
        has been donein main(), but main() seems a little crowded at the moment"""
    parser = argparse.ArgumentParser(
                                    prog='dir_watcher',
                                    description='Watches Dirs for magic strings',
                                    usage='%(prog)s [options]',
                                    epilog="Lookin for those magic strings")

    parser.add_argument('dirname', help='What Dir to watch')
    parser.add_argument('magictext', help='what is the magic text')
    parser.add_argument('--extname', help='What type of file extension to search with-in', default='.txt')
    parser.add_argument('--howoften', help='(Number) how often to search for magic-text', default=1)
    return parser


def main():
    # maybe put in while / try
    starting_time = time.time()
    parser = dir_watcher_parser()
    args = parser.parse_args()
    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    while not exit_flag:
        try:
            magic_text_locator(args.dirname, args.magictext, args.extname)
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            pass

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(args.howoften)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start





if __name__ == "__main__":
    main(sys.argv[1:])
