import argparse, curses
from twoColumnEditor import get_diff_text, get_win

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', action='store_true', default=False,
                        help='Only print diff the text.')
    parser.add_argument('fromfile')
    parser.add_argument('tofile')
    options = parser.parse_args()
    return options

def main(args):
    
    fromfile = args.fromfile
    tofile = args.tofile

    if args.text:
        get_diff_text(fromfile, tofile, stdout=True)
    else:
        curses.wrapper(get_win, fromfile, tofile)