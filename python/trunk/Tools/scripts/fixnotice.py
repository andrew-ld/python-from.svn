#! /usr/bin/env python

OLD_NOTICE = """
Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the names of Stichting Mathematisch
Centrum or CWI not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior permission.

STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE
FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

NEW_NOTICE = """
Copyright (c) 2000, BeOpen.com.
Copyright (c) 1995-2000, Corporation for National Research Initiatives.
Copyright (c) 1990-1995, Stichting Mathematisch Centrum.
All rights reserved.

See the file "Misc/COPYRIGHT" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.
"""

# " <-- Help Emacs

import os, sys, string

def main():
    args = sys.argv[1:]
    if not args:
        print "No arguments."
    for arg in args:
        process(arg)

def process(arg):
    f = open(arg)
    data = f.read()
    f.close()
    i = string.find(data, OLD_NOTICE)
    if i < 0:
##         print "No old notice in", arg
        return
    data = data[:i] + NEW_NOTICE + data[i+len(OLD_NOTICE):]
    new = arg + ".new"
    backup = arg + ".bak"
    print "Replacing notice in", arg, "...",
    sys.stdout.flush()
    f = open(new, "w")
    f.write(data)
    f.close()
    os.rename(arg, backup)
    os.rename(new, arg)
    print "done"

if __name__ == '__main__':
    main()
