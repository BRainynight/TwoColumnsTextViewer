## Description
A simple text viewer for viewing differences between 2 files.

## Requirement 

- Python 3.8

## Usage

- Use keyboard or  vim-style arrow keys to control cursor up and down. 
- Refresh comparison by key `r`

```bash
python main.py <fromfile> <tofile>	 	# compare 2 file based on fromfile 
python main.py -r <fromfile> <tofile>	# compare 2 file based on tofile.
```





## Screenshot

![Example](img/README/Example.png)

## Update Logs
- 2022/11/10: 
  - Handle keyboard interrupt exception and resize event. 
  - Keep tab spacing in viewer.
  - Press `r` can refresh comparison. 
- 2022/11/03: 
  - Enable vim-style arrow keys (`k`, `j`, `h`, `l`). For my VS code terminal (PowerShell) , the keyboard arrow keys is unable because its return value of `getkey()` is differ from [the official key list](https://docs.python.org/3.8/library/curses.html#curses.ncurses_version).
  - Add file name in the top of viewer.
  - Add the line number range for each block. 
  - Add the argument `reverse` in CLI.



## Reference

- [Python Howto : Curses Programming with Python](https://docs.python.org/3.8/howto/curses.html)

- [Python curses — Terminal handling for character-cell displays](https://docs.python.org/3.8/library/curses.html#curses.resize_term)

- [Python difflib — Helpers for computing deltas](https://docs.python.org/3/library/difflib.html#difflib.context_diff)

- [Wasim Lorgat Build a text editor with Python and curses](https://wasimlorgat.com/posts/editor.html#scroll-the-window-to-the-cursor)

