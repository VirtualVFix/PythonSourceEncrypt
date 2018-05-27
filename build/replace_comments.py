# All rights reserved by forest fairy.
# You cannot modify or share anything without sacrifice.
# If you don't agree, keep calm and don't look on text below...

__author__ = "VirtualV <github.com/virtualvfix>"
__date__ = "09/22/17 14:23"

import re
import os

REPLACEMENT_COMMENT = ['Radiohead - "Creep"', '', 'When you were here before', "Couldn't look you in the eye",
                       "You're just like an angel", 'Your skin makes me cry', 'You float like a feather',
                       'In a beautiful world', 'And I wish I was special', "You're so fuckin' special",
                       "But I'm a creep, I'm a weirdo.", 'What the hell am I doing here?', "I don't belong here.",
                       "I don't care if it hurts", 'I want to have control', 'I want a perfect body',
                       'I want a perfect soul', 'I want you to notice', "When I'm not around",
                       "You're so fuckin' special", 'I wish I was special', "But I'm a creep, I'm a weirdo.",
                       'What the hell am I doing here?', "I don't belong here.", "She's running out again,",
                       "She's running out", "She's run run run run", 'Whatever makes you happy', 'Whatever you want',
                       "You're so fuckin' special", 'I wish I was special', "But I'm a creep, I'm a weirdo,",
                       'What the hell am I doing here?', "I don't belong here.", "I don't belong here.",
                       '', '', '',]
REPLACE_ITER = 0
# comment some tags
TAGS = ('__date__',)

def replaceRe(line):
    return line.group(1) + '@'*len(line.group(2)) + line.group(3)


def replaceComments(lines):
    """ replace comments and doc lines to text from song in REPLACEMENT_COMMENT list """

    new_lines = ''.encode('utf-8')
    is_quote_open = False   # string quote open
    is_doc_line = False     # doc line open
    doc_just_close = False  # found close tag of doc line
    doc_just_open = False   # found open tag of doc line
    doc_offset = 0          # Doc line offset in spaces

    quote = ''
    doc_quote = ''
    doc_line = -1
    tag_line = -1
    src = lines.splitlines()

    # replace text in source
    def __replaceText(text, replace_str=None, doc=False, offset=0):
        global REPLACE_ITER
        if replace_str is not None:
            result = (' ' * offset).encode('utf-8') + text + ('%s' % replace_str).encode('utf-8')
        else:
            if doc:
                result = (' ' * offset).encode('utf-8') + text + REPLACEMENT_COMMENT[REPLACE_ITER].encode('utf-8')
            else:
                result = (' ' * offset).encode('utf-8') + text \
                         + ('# ' + REPLACEMENT_COMMENT[REPLACE_ITER]).encode('utf-8')
            REPLACE_ITER = (REPLACE_ITER+1) % len(REPLACEMENT_COMMENT)
        return result

    for j in range(0, len(src), 1):
        _line = str(src[j], encoding='utf-8')
        # replace regexp
        _line = re.sub('(.*?)(re\..*?\(.*?\',.*?\))(.*)', replaceRe, _line)
        for i in range(len(_line)-1):
            lit = _line[i]
            if lit in ['\'', '"']:
                # lit is doc line
                if len(_line) >= i+2 and _line[i:i+3] in ['"""', '\'\'\'']:
                    if lit == doc_quote or doc_quote == '':
                        # doc line already opened
                        if is_doc_line:
                            doc_just_close = True
                            doc_just_open = False
                            is_doc_line = False
                            doc_quote = ''
                        else:
                            doc_offset = i
                            doc_just_open = True
                            doc_just_close = False
                            is_doc_line = True
                            doc_quote = lit
                # lit is quote
                elif quote == lit or quote == '':
                    if is_quote_open:
                        is_quote_open = False
                        quote = ''
                    else:
                        is_quote_open = True
                        quote = lit
            # replace tag
            if _line.startswith(TAGS) and j != tag_line:
                tag_line = j
                src[j] = __replaceText(src[j][:i])
                continue
            # replace doc line
            if (is_doc_line and j != doc_line or doc_just_close) and tag_line != j:
                if doc_just_open:
                    if _line.startswith('__doc__'):
                        src[j] = __replaceText(b'', replace_str='__doc__ = """', offset=0)
                    else:
                        src[j] = __replaceText(b'', replace_str='"""', offset=doc_offset)
                    doc_just_open = False
                elif doc_just_close:
                    if j == doc_line:
                        src[j] += ' """'.encode('utf-8')
                    else:
                        src[j] = __replaceText(b'', replace_str='"""', offset=doc_offset)
                    doc_just_close = False
                    break
                else:
                    src[j] = __replaceText(src[j][:i], doc=True, offset=doc_offset)

                doc_line = j
                continue
            # replace comment
            if lit == '#' and not is_quote_open and not is_doc_line:
                src[j] = __replaceText(src[j][:i])
                break
        # close quote if it not split to next line using symbol "\"
        if len(_line) > 0 and _line[len(_line)-1] != '\\':
            is_quote_open = False
            quote = ''
        new_lines += src[j] + os.linesep.encode('utf-8')
    return new_lines
