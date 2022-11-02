
class Status:    
    none = 0
    is_del  = 1
    is_add  = 2
    is_diff = 3
    is_content = 4
    is_file = -1
    is_section = -2
    is_lineno = -3

class Block:
    def __init__(self, index) -> None:
        self.index = index
        self.lt = []
    
    def add_content(self, status, content):
        self.lt.append((status, content))
   
class Content:
    def __init__(self, before, title="") -> None:
        self.is_before = before
        self.block_ind = 0
        self.title = title
        self.container = []
    
    def new_section(self, ):
        b = Block(self.block_ind)
        self.container.append(b)
        self.block_ind += 1

    def add_content(self, status, content):
        self.container[-1].add_content(status, content)

def get_stage(l):
    prefix = l[0]
    if prefix=='*':
        return get_file_related_info(l)
    elif prefix=="-":
        if l[:2] == "--":
            return get_file_related_info(l)
        else:
            return Status.is_del

    elif prefix==' ':
        return Status.is_content
    elif prefix=='!':
        return Status.is_diff
    elif prefix=='+':
        return Status.is_add
    else:
        print(l)

def get_version(line):
    if line[:3] == "*"*3:
        return "left"
    elif line[:3] == "-"*3:
        return "right"
    else:
        return "none"

def get_file_related_info(line):
    '''
    Get the file infomation. Like file name, 
    line number range of captured text, or seperated line.
    '''
    if len(line) < 3:
        return Status.none
    
    v = get_version(line)    
    if v == "left":
        return identify_file_or_line_num(line, prefix="*")
    elif v == "right":
        return identify_file_or_line_num(line, prefix="-")
    else:
        return Status.none

def identify_file_or_line_num(line, prefix="*"):
    line = line.replace("\n", "")
    res = "before " if prefix=="*" else "after "

    if line=="***************":
        return Status.is_section
    elif line[-3:]==prefix*3:
        return Status.is_lineno
    else:
        return Status.is_file

def container_to_plain_text(c: Content):
    '''
    Flatten each block to single list. (Only text)
    Return style : [text, text, text, ...]
    '''
    text_lt = []
    for block in c.container:
        for l in block.lt:
            text_lt.append(l[1])
        text_lt.append("="*30)
    return text_lt

def container_to_status_and_text_list(c: Content, num):
    '''
    Flatten each block to single list. (Status & text)
    Return style : [(status, text), (status, text), (status, text), ...]
    '''
    text_lt = []
    text_lt.append((Status.none, c.title))
    text_lt.append((Status.none, "="*num))
    for block in c.container:
        text_lt += block.lt
        text_lt.append((Status.none, "="*num))
    return text_lt

def fill_blank_line(before_c:Content, after_c:Content):
    '''
    Let block in 2 container has same length (filled by blank line).
    '''
    blen = len(before_c.container[-1].lt)
    alen = len(after_c.container[-1].lt) 
    num = abs(alen-blen)
    if blen < alen:        
        before_c.container[-1].lt += [(0, "\n")]*num
    elif alen < blen:
        after_c.container[-1].lt += [(0, "\n")]*num
    else:
        return before_c, after_c    
    return before_c, after_c

def parse_diff_content(g, fromfile="", tofile=""):
    '''
    Analyze the diff result (get by difflib.context_diff) to the custom container.
    '''
    before_content = Content(before=True, title=fromfile)
    after_content = Content(before=False, title=tofile)
    holden_content = before_content

    for l in g:
        s = get_stage(l)
        v = get_version(l)

        if v == "left":
            holden_content = before_content
        elif v == "right":
            holden_content = after_content
        
        if s == Status.is_section:
            if len(before_content.container) != 0 or len(after_content.container) !=0:
                before_content, after_content = fill_blank_line(before_content, after_content)
            before_content.new_section()
            after_content.new_section()
            continue

        if s in [Status.is_content, Status.is_del, Status.is_add, Status.is_diff]:
            holden_content.add_content(s, l)

    if len(before_content.container) != 0 or len(after_content.container) !=0:
        before_content, after_content = fill_blank_line(before_content, after_content)    
    return before_content, after_content 