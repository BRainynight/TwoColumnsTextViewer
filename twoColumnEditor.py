import argparse
import curses
import sys
import difflib
import textwrap

import os
from control_class import Buffer, Cursor, Window
from compare_diff import Status, parse_diff_content
from compare_diff import container_to_status_and_text_list, container_to_plain_text

def read_file_lines(fp):
    f = open(fp, "r", encoding="utf-8")
    return f.readlines()

def color_256_to_1000(color256):
    color1000 = []
    for c in color256:
        color1000.append(int(c/256*1000))
    return color1000

def set_color():
    '''
    0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
    curses.init_pair(index, font_color, background)
    color should use this style: curses.COLOR_XXXX, ex. curses.COLOR_WHITE
    '''
    os.environ["TERM"] = "xterm-256color"
    curses.start_color()
    default = curses.COLOR_BLACK
    curses.init_pair(Status.is_del, curses.COLOR_RED, default)
    curses.init_pair(Status.is_add, curses.COLOR_GREEN, default)
    curses.init_pair(Status.is_diff, curses.COLOR_YELLOW, default)
    curses.init_pair(Status.is_hightlight_file_name, curses.COLOR_CYAN, default)

    if curses.can_change_color():
        curses.init_color(50, *color_256_to_1000([118,215,208]))
        curses.init_color(51, *color_256_to_1000([219,245,243]))
        curses.init_color(52, *color_256_to_1000([255,69,69]))  # pink

        curses.init_pair(Status.is_hightlight_file_name, 50, default)
        curses.init_pair(Status.is_del, 52, default)
        pass

def resize_win(win, lines, width, delta_y=0, delta_x=0):
    win.resize(lines, width)
    win.mvderwin(delta_y, delta_x)

def create_wins(stdscr, lines, half_width, delta_y, delta_x):
    left_window = stdscr.derwin(lines, half_width, 0, 0)    # child window from stdscr
    left_window.nodelay(True)    
    right_window = stdscr.derwin(lines, half_width, delta_y, delta_x)

    winl  = Window(left_window, curses.LINES - 1, half_width)
    winr  = Window(right_window, curses.LINES - 1, half_width, delta_y, -delta_x)
    cursor = Cursor(delta_y, delta_x)
    return winl, winr, cursor

def update_text(win, buf, status=False, max_col=None):
    try:
        for row, line in enumerate(buf[win.row:win.row + win.n_rows]):
            if status:
                s, l = line
                s = 0 if s <0 or s==4 else s
                if s == Status.is_hightlight_file_name:
                    style = curses.color_pair(s) | curses.A_BOLD
                else:
                    style = curses.color_pair(s)
                if max_col is None:
                    win.write(row, 0, l, style)
                else:
                    win.write(row, 0, textwrap.shorten(l, max_col, placeholder="..."), style)
            else:
                win.write(row, 0, line)
        win.refresh()
    except curses.error:
        pass

def get_win(stdscr, fromfile, tofile):
    screen = curses.initscr()
    screen.border(0)
    curses.echo()
    set_color()

    half_width, winl, winr, cursor, status, bufl, bufr = initialize(stdscr, fromfile, tofile)

    control_win = winr.curses_win
    while True:
        stdscr.erase()
        update_text(winr, bufr, status, max_col=half_width)
        update_text(winl, bufl, status, max_col=half_width)

        try :
            new_y, new_x = winr.translate(cursor)
            stdscr.move(new_y, new_x)            
        except curses.error:
            pass
        
        k = stdscr.getkey()
        if k == "q":
            sys.exit(0)
        elif k == "KEY_UP" or k== "k":
            cursor.up(bufr)
            winr.up(cursor)
            winl.up(cursor)
        elif k == "KEY_DOWN" or k== "j":
            cursor.down(bufr)
            winr.down(bufr, cursor)
            winl.down(bufl, cursor)
            
        elif k == "KEY_LEFT" or k== "h":
            cursor.left(bufr)
            winr.up(cursor)
        elif k == "KEY_RIGHT" or k== "l":
            cursor.right(bufr)
            winr.down(bufr, cursor)
        elif k == "KEY_RESIZE":
            curses.update_lines_cols()
            half_width, winl, winr, cursor, status, bufl, bufr = initialize(stdscr, fromfile, tofile)


            
def initialize(stdscr, fromfile, tofile):
    lines = int(curses.LINES - 1)
    columns = int(curses.COLS - 1)
    half_width = int(columns / 2) -2
    delta_y, delta_x = 0, half_width+2

    winl, winr, cursor = create_wins(stdscr, lines, half_width, delta_y, delta_x)
    g = get_diff_text(fromfile, tofile, stdout=False)
    before, after = parse_diff_content(g, fromfile=fromfile, tofile=tofile)

    status = True
    if status:
        bufl = Buffer(container_to_status_and_text_list(before, half_width))
        bufr = Buffer(container_to_status_and_text_list(after, half_width))
    else:
        bufl = Buffer(container_to_plain_text(before))
        bufr = Buffer(container_to_plain_text(after))
    return half_width,winl,winr,cursor,status,bufl,bufr

def get_diff_text(fromfile, tofile, stdout=False):
    s1 = read_file_lines(fromfile)
    s2 = read_file_lines(tofile)    
    if stdout:
        sys.stdout.writelines(difflib.context_diff(s1, s2, fromfile=fromfile, tofile=tofile,n=1))
    else:
        return difflib.context_diff(s1, s2, fromfile=fromfile, tofile=tofile,n=1)

if __name__ == "__main__":
    path1 = './exp_filecmp/cmp1'
    path2 = './exp_filecmp/cmp2'
    file = "line_compare.txt"
    fromfile = os.path.join(path1, file)
    tofile = os.path.join(path2, file)

    while True:
        try:
            curses.wrapper(get_win, fromfile, tofile)
        except ValueError:
            curses.wrapper(get_win, fromfile, tofile)
