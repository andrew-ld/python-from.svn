"""Generate ast module from specification"""

import fileinput
import getopt
import re
import sys
from StringIO import StringIO

SPEC = "ast.txt"
COMMA = ", "

def load_boilerplate(file):
    f = open(file)
    buf = f.read()
    f.close()
    i = buf.find('### ''PROLOGUE')
    j = buf.find('### ''EPILOGUE')
    pro = buf[i+12:j].strip()
    epi = buf[j+12:].strip()
    return pro, epi

def strip_default(arg):
    """Return the argname from an 'arg = default' string"""
    i = arg.find('=')
    if i == -1:
        return arg
    return arg[:i].strip()

class NodeInfo:
    """Each instance describes a specific AST node"""
    def __init__(self, name, args):
        self.name = name
        self.args = args.strip()
        self.argnames = self.get_argnames()
        self.nargs = len(self.argnames)
        self.children = COMMA.join(["self.%s" % c
                                    for c in self.argnames])
        self.init = []

    def get_argnames(self):
        if '(' in self.args:
            i = self.args.find('(')
            j = self.args.rfind(')')
            args = self.args[i+1:j]
        else:
            args = self.args
        return [strip_default(arg.strip())
                for arg in args.split(',') if arg]

    def gen_source(self):
        buf = StringIO()
        print >> buf, "class %s(Node):" % self.name
        print >> buf, '    nodes["%s"] = "%s"' % (self.name.lower(), self.name)
        self._gen_init(buf)
        self._gen_getChildren(buf)
        self._gen_repr(buf)
        buf.seek(0, 0)
        return buf.read()

    def _gen_init(self, buf):
        print >> buf, "    def __init__(self, %s):" % self.args
        if self.argnames:
            for name in self.argnames:
                print >> buf, "        self.%s = %s" % (name, name)
        else:
            print >> buf, "        pass"
        if self.init:
            print >> buf, "".join(["    " + line for line in self.init])

    def _gen_getChildren(self, buf):
        print >> buf, "    def _getChildren(self):"
        if self.argnames:
            if self.nargs == 1:
                print >> buf, "        return %s," % self.children
            else:
                print >> buf, "        return %s" % self.children
        else:
            print >> buf, "        return ()"

    def _gen_repr(self, buf):
        print >> buf, "    def __repr__(self):"
        if self.argnames:
            fmt = COMMA.join(["%s"] * self.nargs)
            vals = ["repr(self.%s)" % name for name in self.argnames]
            vals = COMMA.join(vals)
            if self.nargs == 1:
                vals = vals + ","
            print >> buf, '        return "%s(%s)" %% (%s)' % \
                  (self.name, fmt, vals)
        else:
            print >> buf, '        return "%s()"' % self.name

rx_init = re.compile('init\((.*)\):')

def parse_spec(file):
    classes = {}
    cur = None
    for line in fileinput.input(file):
        mo = rx_init.search(line)
        if mo is None:
            if cur is None:
                # a normal entry
                try:
                    name, args = line.split(':')
                except ValueError:
                    continue
                classes[name] = NodeInfo(name, args)
                cur = None
            else:
                # some code for the __init__ method
                cur.init.append(line)
        else:
            # some extra code for a Node's __init__ method
            name = mo.group(1)
            cur = classes[name]
    return classes.values()

def main():
    prologue, epilogue = load_boilerplate(sys.argv[-1])
    print prologue
    print
    classes = parse_spec(SPEC)
    for info in classes:
        print info.gen_source()
    print epilogue

if __name__ == "__main__":
    main()
    sys.exit(0)

### PROLOGUE
"""Python abstract syntax node definitions

This file is automatically generated.
"""
from types import TupleType, ListType
from consts import CO_VARARGS, CO_VARKEYWORDS

def flatten(list):
    l = []
    for elt in list:
        t = type(elt)
        if t is TupleType or t is ListType:
            for elt2 in flatten(elt):
                l.append(elt2)
        else:
            l.append(elt)
    return l

def asList(nodes):
    l = []
    for item in nodes:
        if hasattr(item, "asList"):
            l.append(item.asList())
        else:
            t = type(item)
            if t is TupleType or t is ListType:
                l.append(tuple(asList(item)))
            else:
                l.append(item)
    return l

nodes = {}

class Node:
    lineno = None
    def getType(self):
        pass
    def getChildren(self):
        # XXX It would be better to generate flat values to begin with
        return flatten(self._getChildren())
    def asList(self):
        return tuple(asList(self.getChildren()))

class EmptyNode(Node):
    def __init__(self):
        self.lineno = None

### EPILOGUE
klasses = globals()
for k in nodes.keys():
    nodes[k] = klasses[nodes[k]]
