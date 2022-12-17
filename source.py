"""
Require Python 3
"""

import os
import re
import sys


def auto_rename_exist_filename(file_path):
    """
    For example: a.txt, a(1).txt, a(2).txt

    Source: https://gist.github.com/nodewee/9ae9b0b461b4bcaf30bc2b84ca8c4743.js
    """
    if not os.path.exists(file_path):
        return file_path

    dir_path = os.path.dirname(file_path)
    src_filename = os.path.basename(file_path)
    [file_title, ext_name] = os.path.splitext(src_filename)

    pattern = r"\((\d+?)\)$"
    r = re.search(pattern, file_title)
    if r:
        serial = str(int(r.groups()[0]) + 1)
        new_title = re.sub(pattern, "(" + serial + ")", file_title)
    else:
        new_title = file_title + "(1)"

    new_filepath = os.path.join(dir_path, new_title + ext_name)

    if os.path.exists(new_filepath):
        return auto_rename_exist_filename(new_filepath)
    else:
        return new_filepath


def paste_to_file():
    # parse argument
    input_arg = " ".join(sys.argv[1:])
    if not input_arg:
        return "ERROR: Missing arguments"
    pos = input_arg.find("|")
    if pos < 0:
        return 'ERROR: Invalid arguments. Must be "file-path|text"'
    in_path = input_arg[:pos]
    text = input_arg[pos + 1 :]
    if not os.path.exists(in_path):
        return "ERROR: File/directory path not exist"
    if not text:
        return "ERROR: No text from input"

    # prepare file name
    dir_path = in_path if os.path.isdir(in_path) else os.path.dirname(in_path)
    file_path = os.path.join(dir_path, "untitled.txt")
    file_path = auto_rename_exist_filename(file_path)

    open(file_path, "wt").write(text)
    return file_path


print(paste_to_file())
