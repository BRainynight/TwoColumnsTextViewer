import argparse, curses
from twoColumnEditor import get_diff_text, get_win

def get_args():
    description = "Based on fromfile, compare the difference fromfile to tofile."
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', action='store_true', default=False,
                        help='Only print diff the text.')
    parser.add_argument('-r', '--reverse', action='store_true', default=False,
                        help="Reverse the position of 'fromfile' and 'tofile'")
    
    parser.add_argument('fromfile')
    parser.add_argument('tofile')
    options = parser.parse_args()
    return options

def main(args=None):    
    fromfile = ".\exp_filecmp\cmp1\line_compare.txt" # args.fromfile
    tofile = ".\exp_filecmp\cmp2\line_compare.txt" # args.tofile

    fromfile = args.fromfile
    tofile = args.tofile

    if args.reverse:
        fromfile, tofile = tofile, fromfile
    if args.text:
        get_diff_text(fromfile, tofile, stdout=True)
    else:
        curses.wrapper(get_win, fromfile, tofile)

if __name__=="__main__":
    args = get_args()
    main(args)