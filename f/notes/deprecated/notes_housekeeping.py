#!/usr/bin/python

# https://github.com/python/cpython/blob/main/Tools/scripts/crlf.py
# ensure no windows line endings, only unix
import os
def lfcr_to_lf(filename):
    if os.path.isdir(filename):
        print(filename, "Directory!")
        return
    with open(filename, "rb") as f:
        data = f.read()
    if b'\0' in data:
        print(filename, "Binary!")
        return
    newdata = data.replace(b"\r\n", b"\n")
    if newdata != data:
        print(filename + " -> found lfcr line ending - processing")
        with open(filename, "wb") as f:
            f.write(newdata)
# for note in get_all_notes():
#     lfcr_to_lf(note)
