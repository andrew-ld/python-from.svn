/***********************************************************
Copyright 1991-1995 by Stichting Mathematisch Centrum, Amsterdam,
The Netherlands.

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the names of Stichting Mathematisch
Centrum or CWI or Corporation for National Research Initiatives or
CNRI not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior
permission.

While CWI is the initial source for this software, a modified version
is made available by the Corporation for National Research Initiatives
(CNRI) at the Internet address ftp://ftp.python.org.

STICHTING MATHEMATISCH CENTRUM AND CNRI DISCLAIM ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH
CENTRUM OR CNRI BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

******************************************************************/

/* Module definition and import implementation */

#include "Python.h"

#include "node.h"
#include "token.h"
#include "graminit.h"
#include "errcode.h"
#include "marshal.h"
#include "compile.h"
#include "eval.h"
#include "osdefs.h"
#include "importdl.h"
#ifdef macintosh
/* 'argument' is a grammar symbol, but also used in some mac header files */
#undef argument
#include "macglue.h"
#endif

#ifdef HAVE_UNISTD_H
#include <unistd.h>
#endif

extern long PyOS_GetLastModificationTime(); /* In getmtime.c */

/* Magic word to reject .pyc files generated by other Python versions */
/* Change for each incompatible change */
/* The value of CR and LF is incorporated so if you ever read or write
   a .pyc file in text mode the magic number will be wrong; also, the
   Apple MPW compiler swaps their values, botching string constants */
/* XXX Perhaps the magic number should be frozen and a version field
   added to the .pyc file header? */
/* New way to come up with the magic number: (YEAR-1995), MONTH, DAY */
#define MAGIC (20121 | ((long)'\r'<<16) | ((long)'\n'<<24))

PyObject *import_modules; /* This becomes sys.modules */


/* Initialize things */

void
PyImport_Init()
{
	if (import_modules != NULL)
		Py_FatalError("duplicate initimport() call");
	if ((import_modules = PyDict_New()) == NULL)
		Py_FatalError("no mem for dictionary of modules");
	if (Py_OptimizeFlag) {
		/* Replace ".pyc" with ".pyo" in import_filetab */
		struct filedescr *p;
		for (p = _PyImport_Filetab; p->suffix != NULL; p++) {
			if (strcmp(p->suffix, ".pyc") == 0)
				p->suffix = ".pyo";
		}
	}
}


/* Un-initialize things, as good as we can */

void
PyImport_Cleanup()
{
	if (import_modules != NULL) {
		PyObject *tmp = import_modules;
		import_modules = NULL;
		/* This deletes all modules from sys.modules.
		   When a module is deallocated, it in turn clears its
		   dictionary, thus hopefully breaking any circular
		   references between modules and between a module's
		   dictionary and its functions.  Note that "import"
		   will fail while we are cleaning up.  */
		PyDict_Clear(tmp);
		Py_DECREF(tmp);
	}
}


/* Helper for pythonrun.c -- return magic number */

long
PyImport_GetMagicNumber()
{
	return MAGIC;
}


/* Helper for sysmodule.c -- return modules dictionary */

PyObject *
PyImport_GetModuleDict()
{
	return import_modules;
}


/* Get the module object corresponding to a module name.
   First check the modules dictionary if there's one there,
   if not, create a new one and insert in in the modules dictionary.
   Because the former action is most common, THIS DOES NOT RETURN A
   'NEW' REFERENCE! */

PyObject *
PyImport_AddModule(name)
	char *name;
{
	PyObject *m;

	if (import_modules == NULL) {
		PyErr_SetString(PyExc_SystemError,
				"sys.modules has been deleted");
		return NULL;
	}
	if ((m = PyDict_GetItemString(import_modules, name)) != NULL &&
	    PyModule_Check(m))
		return m;
	m = PyModule_New(name);
	if (m == NULL)
		return NULL;
	if (PyDict_SetItemString(import_modules, name, m) != 0) {
		Py_DECREF(m);
		return NULL;
	}
	Py_DECREF(m); /* Yes, it still exists, in modules! */

	return m;
}


/* Execute a code object in a module and return the module object
   WITH INCREMENTED REFERENCE COUNT */

PyObject *
PyImport_ExecCodeModule(name, co)
	char *name;
	PyObject *co;
{
	PyObject *m, *d, *v;

	m = PyImport_AddModule(name);
	if (m == NULL)
		return NULL;
	d = PyModule_GetDict(m);
	if (PyDict_GetItemString(d, "__builtins__") == NULL) {
		if (PyDict_SetItemString(d, "__builtins__",
					 PyEval_GetBuiltins()) != 0)
			return NULL;
	}
	/* Remember the filename as the __file__ attribute */
	if (PyDict_SetItemString(d, "__file__",
				 ((PyCodeObject *)co)->co_filename) != 0)
		PyErr_Clear(); /* Not important enough to report */
	v = PyEval_EvalCode((PyCodeObject *)co, d, d); /* XXX owner? */
	if (v == NULL)
		return NULL;
	Py_DECREF(v);
	Py_INCREF(m);

	return m;
}


/* Given a pathname for a Python source file, fill a buffer with the
   pathname for the corresponding compiled file.  Return the pathname
   for the compiled file, or NULL if there's no space in the buffer.
   Doesn't set an exception. */

static char *
make_compiled_pathname(pathname, buf, buflen)
	char *pathname;
	char *buf;
	int buflen;
{
	int len;

	len = strlen(pathname);
	if (len+2 > buflen)
		return NULL;
	strcpy(buf, pathname);
	strcpy(buf+len, Py_OptimizeFlag ? "o" : "c");

	return buf;
}


/* Given a pathname for a Python source file, its time of last
   modification, and a pathname for a compiled file, check whether the
   compiled file represents the same version of the source.  If so,
   return a FILE pointer for the compiled file, positioned just after
   the header; if not, return NULL.
   Doesn't set an exception. */

static FILE *
check_compiled_module(pathname, mtime, cpathname)
	char *pathname;
	long mtime;
	char *cpathname;
{
	FILE *fp;
	long magic;
	long pyc_mtime;

	fp = fopen(cpathname, "rb");
	if (fp == NULL)
		return NULL;
	magic = PyMarshal_ReadLongFromFile(fp);
	if (magic != MAGIC) {
		if (Py_VerboseFlag)
			fprintf(stderr, "# %s has bad magic\n", cpathname);
		fclose(fp);
		return NULL;
	}
	pyc_mtime = PyMarshal_ReadLongFromFile(fp);
	if (pyc_mtime != mtime) {
		if (Py_VerboseFlag)
			fprintf(stderr, "# %s has bad mtime\n", cpathname);
		fclose(fp);
		return NULL;
	}
	if (Py_VerboseFlag)
		fprintf(stderr, "# %s matches %s\n", cpathname, pathname);
	return fp;
}


/* Read a code object from a file and check it for validity */

static PyCodeObject *
read_compiled_module(fp)
	FILE *fp;
{
	PyObject *co;

	co = PyMarshal_ReadObjectFromFile(fp);
	/* Ugly: rd_object() may return NULL with or without error */
	if (co == NULL || !PyCode_Check(co)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_ImportError,
				   "Non-code object in .pyc file");
		Py_XDECREF(co);
		return NULL;
	}
	return (PyCodeObject *)co;
}


/* Load a module from a compiled file, execute it, and return its
   module object WITH INCREMENTED REFERENCE COUNT */

static PyObject *
load_compiled_module(name, cpathname, fp)
	char *name;
	char *cpathname;
	FILE *fp;
{
	long magic;
	PyCodeObject *co;
	PyObject *m;

	magic = PyMarshal_ReadLongFromFile(fp);
	if (magic != MAGIC) {
		PyErr_SetString(PyExc_ImportError,
				"Bad magic number in .pyc file");
		return NULL;
	}
	(void) PyMarshal_ReadLongFromFile(fp);
	co = read_compiled_module(fp);
	if (co == NULL)
		return NULL;
	if (Py_VerboseFlag)
		fprintf(stderr, "import %s # precompiled from %s\n",
			name, cpathname);
	m = PyImport_ExecCodeModule(name, (PyObject *)co);
	Py_DECREF(co);

	return m;
}

/* Parse a source file and return the corresponding code object */

static PyCodeObject *
parse_source_module(pathname, fp)
	char *pathname;
	FILE *fp;
{
	PyCodeObject *co;
	node *n;

	n = PyParser_SimpleParseFile(fp, pathname, file_input);
	if (n == NULL)
		return NULL;
	co = PyNode_Compile(n, pathname);
	PyNode_Free(n);

	return co;
}


/* Write a compiled module to a file, placing the time of last
   modification of its source into the header.
   Errors are ignored, if a write error occurs an attempt is made to
   remove the file. */

static void
write_compiled_module(co, cpathname, mtime)
	PyCodeObject *co;
	char *cpathname;
	long mtime;
{
	FILE *fp;

	fp = fopen(cpathname, "wb");
	if (fp == NULL) {
		if (Py_VerboseFlag)
			fprintf(stderr,
				"# can't create %s\n", cpathname);
		return;
	}
	PyMarshal_WriteLongToFile(MAGIC, fp);
	/* First write a 0 for mtime */
	PyMarshal_WriteLongToFile(0L, fp);
	PyMarshal_WriteObjectToFile((PyObject *)co, fp);
	if (ferror(fp)) {
		if (Py_VerboseFlag)
			fprintf(stderr, "# can't write %s\n", cpathname);
		/* Don't keep partial file */
		fclose(fp);
		(void) unlink(cpathname);
		return;
	}
	/* Now write the true mtime */
	fseek(fp, 4L, 0);
	PyMarshal_WriteLongToFile(mtime, fp);
	fflush(fp);
	fclose(fp);
	if (Py_VerboseFlag)
		fprintf(stderr, "# wrote %s\n", cpathname);
#ifdef macintosh
	setfiletype(cpathname, 'Pyth', 'PYC ');
#endif
}


/* Load a source module from a given file and return its module
   object WITH INCREMENTED REFERENCE COUNT.  If there's a matching
   byte-compiled file, use that instead. */

static PyObject *
load_source_module(name, pathname, fp)
	char *name;
	char *pathname;
	FILE *fp;
{
	long mtime;
	FILE *fpc;
	char buf[MAXPATHLEN+1];
	char *cpathname;
	PyCodeObject *co;
	PyObject *m;

	mtime = PyOS_GetLastModificationTime(pathname);
	cpathname = make_compiled_pathname(pathname, buf, MAXPATHLEN+1);
	if (cpathname != NULL &&
	    (fpc = check_compiled_module(pathname, mtime, cpathname))) {
		co = read_compiled_module(fpc);
		fclose(fpc);
		if (co == NULL)
			return NULL;
		if (Py_VerboseFlag)
			fprintf(stderr, "import %s # precompiled from %s\n",
				name, cpathname);
	}
	else {
		co = parse_source_module(pathname, fp);
		if (co == NULL)
			return NULL;
		if (Py_VerboseFlag)
			fprintf(stderr, "import %s # from %s\n",
				name, pathname);
		write_compiled_module(co, cpathname, mtime);
	}
	m = PyImport_ExecCodeModule(name, (PyObject *)co);
	Py_DECREF(co);

	return m;
}


/* Search the path (default sys.path) for a module.  Return the
   corresponding filedescr struct, and (via return arguments) the
   pathname and an open file.  Return NULL if the module is not found. */

static struct filedescr *
find_module(name, path, buf, buflen, p_fp)
	char *name;
	PyObject *path;
	/* Output parameters: */
	char *buf;
	int buflen;
	FILE **p_fp;
{
	int i, npath, len, namelen;
	struct filedescr *fdp = NULL;
	FILE *fp = NULL;

#ifdef MS_COREDLL
	extern FILE *PyWin_FindRegisteredModule();
	if ((fp=PyWin_FindRegisteredModule(name, &fdp, buf, buflen))!=NULL) {
		*p_fp = fp;
		return fdp;
	}
#endif


	if (path == NULL)
		path = PySys_GetObject("path");
	if (path == NULL || !PyList_Check(path)) {
		PyErr_SetString(PyExc_ImportError,
			   "sys.path must be a list of directory names");
		return NULL;
	}
	npath = PyList_Size(path);
	namelen = strlen(name);
	for (i = 0; i < npath; i++) {
		PyObject *v = PyList_GetItem(path, i);
		if (!PyString_Check(v))
			continue;
		len = PyString_Size(v);
		if (len + 2 + namelen + _PyImport_MaxSuffixSize >= buflen)
			continue; /* Too long */
		strcpy(buf, PyString_AsString(v));
		if ((int)strlen(buf) != len)
			continue; /* v contains '\0' */
#ifdef macintosh
		if ( PyMac_FindResourceModule(name, buf) ) {
			static struct filedescr resfiledescr =
				{"", "", PY_RESOURCE};
			
			return &resfiledescr;
		}
#endif
		if (len > 0 && buf[len-1] != SEP)
			buf[len++] = SEP;
#ifdef IMPORT_8x3_NAMES
		/* see if we are searching in directory dos_8x3 */
		if (len > 7 && !strncmp(buf + len - 8, "dos_8x3", 7)){
			int j;
			char ch;  /* limit name to 8 lower-case characters */
			for (j = 0; (ch = name[j]) && j < 8; j++)
				if (isupper(ch))
					buf[len++] = tolower(ch);
				else
					buf[len++] = ch;
		}
		else /* Not in dos_8x3, use the full name */
#endif
		{
			strcpy(buf+len, name);
			len += namelen;
		}
		for (fdp = _PyImport_Filetab; fdp->suffix != NULL; fdp++) {
			strcpy(buf+len, fdp->suffix);
			if (Py_VerboseFlag > 1)
				fprintf(stderr, "# trying %s\n", buf);
			fp = fopen(buf, fdp->mode);
			if (fp != NULL)
				break;
		}
		if (fp != NULL)
			break;
	}
	if (fp == NULL) {
		char buf[256];
		sprintf(buf, "No module named %.200s", name);
		PyErr_SetString(PyExc_ImportError, buf);
		return NULL;
	}

	*p_fp = fp;
	return fdp;
}


/* Load an external module using the default search path and return
   its module object WITH INCREMENTED REFERENCE COUNT */

static PyObject *
load_module(name)
	char *name;
{
	char buf[MAXPATHLEN+1];
	struct filedescr *fdp;
	FILE *fp = NULL;
	PyObject *m;

	fdp = find_module(name, (PyObject *)NULL, buf, MAXPATHLEN+1, &fp);
	if (fdp == NULL)
		return NULL;

	switch (fdp->type) {

	case PY_SOURCE:
		m = load_source_module(name, buf, fp);
		break;

	case PY_COMPILED:
		m = load_compiled_module(name, buf, fp);
		break;

	case C_EXTENSION:
		m = _PyImport_LoadDynamicModule(name, buf, fp);
		break;

#ifdef macintosh
	case PY_RESOURCE:
		m = PyMac_LoadResourceModule(name, buf);
		break;
#endif

	default:
		PyErr_SetString(PyExc_SystemError,
			   "find_module returned unexpected result");
		m = NULL;

	}
	if ( fp )
		fclose(fp);

	return m;
}


/* Initialize a built-in module.
   Return 1 for succes, 0 if the module is not found, and -1 with
   an exception set if the initialization failed. */

static int
init_builtin(name)
	char *name;
{
	int i;
	for (i = 0; _PyImport_Inittab[i].name != NULL; i++) {
		if (strcmp(name, _PyImport_Inittab[i].name) == 0) {
			if (_PyImport_Inittab[i].initfunc == NULL) {
				PyErr_SetString(PyExc_ImportError,
					   "Cannot re-init internal module");
				return -1;
			}
			if (Py_VerboseFlag)
				fprintf(stderr, "import %s # builtin\n",
					name);
			(*_PyImport_Inittab[i].initfunc)();
			if (PyErr_Occurred())
				return -1;
			return 1;
		}
	}
	return 0;
}


/* Frozen modules */

static struct _frozen *
find_frozen(name)
	char *name;
{
	struct _frozen *p;

	for (p = PyImport_FrozenModules; ; p++) {
		if (p->name == NULL)
			return NULL;
		if (strcmp(p->name, name) == 0)
			break;
	}
	return p;
}

static PyObject *
get_frozen_object(name)
	char *name;
{
	struct _frozen *p = find_frozen(name);

	if (p == NULL) {
		PyErr_SetString(PyExc_ImportError, "No such frozen object");
		return NULL;
	}
	return PyMarshal_ReadObjectFromString((char *)p->code, p->size);
}

/* Initialize a frozen module.
   Return 1 for succes, 0 if the module is not found, and -1 with
   an exception set if the initialization failed.
   This function is also used from frozenmain.c */

int
PyImport_ImportFrozenModule(name)
	char *name;
{
	struct _frozen *p = find_frozen(name);
	PyObject *co;
	PyObject *m;

	if (p == NULL)
		return 0;
	if (Py_VerboseFlag)
		fprintf(stderr, "import %s # frozen\n", name);
	co = PyMarshal_ReadObjectFromString((char *)p->code, p->size);
	if (co == NULL)
		return -1;
	if (!PyCode_Check(co)) {
		Py_DECREF(co);
		PyErr_SetString(PyExc_TypeError,
				"frozen object is not a code object");
		return -1;
	}
	m = PyImport_ExecCodeModule(name, co);
	Py_DECREF(co);
	if (m == NULL)
		return -1;
	Py_DECREF(m);
	return 1;
}


/* Import a module, either built-in, frozen, or external, and return
   its module object WITH INCREMENTED REFERENCE COUNT */

PyObject *
PyImport_ImportModule(name)
	char *name;
{
	PyObject *m;

	if (import_modules == NULL) {
		PyErr_SetString(PyExc_SystemError,
				"sys.modules has been deleted");
		return NULL;
	}
	if ((m = PyDict_GetItemString(import_modules, name)) != NULL) {
		Py_INCREF(m);
	}
	else {
		int i;
		if ((i = init_builtin(name)) ||
		    (i = PyImport_ImportFrozenModule(name))) {
			if (i < 0)
				return NULL;
			if ((m = PyDict_GetItemString(import_modules,
						      name)) == NULL) {
			    if (PyErr_Occurred() == NULL)
			        PyErr_SetString(PyExc_SystemError,
				 "built-in module not initialized properly");
			}
			else
				Py_INCREF(m);
		}
		else
			m = load_module(name);
	}

	return m;
}


/* Re-import a module of any kind and return its module object, WITH
   INCREMENTED REFERENCE COUNT */

PyObject *
PyImport_ReloadModule(m)
	PyObject *m;
{
	char *name;
	int i;

	if (m == NULL || !PyModule_Check(m)) {
		PyErr_SetString(PyExc_TypeError,
				"reload() argument must be module");
		return NULL;
	}
	name = PyModule_GetName(m);
	if (name == NULL)
		return NULL;
	if (import_modules == NULL) {
		PyErr_SetString(PyExc_SystemError,
				"sys.modules has been deleted");
		return NULL;
	}
	if (m != PyDict_GetItemString(import_modules, name)) {
		PyErr_SetString(PyExc_ImportError,
				"reload() module not in sys.modules");
		return NULL;
	}
	/* Check for built-in and frozen modules */
	if ((i = init_builtin(name)) ||
	    (i = PyImport_ImportFrozenModule(name))) {
		if (i < 0)
			return NULL;
		Py_INCREF(m);
	}
	else
		m = load_module(name);
	return m;
}


/* Module 'imp' provides Python access to the primitives used for
   importing modules.
*/

static PyObject *
imp_get_magic(self, args)
	PyObject *self;
	PyObject *args;
{
	char buf[4];

	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	buf[0] = (char) ((MAGIC >>  0) & 0xff);
	buf[1] = (char) ((MAGIC >>  8) & 0xff);
	buf[2] = (char) ((MAGIC >> 16) & 0xff);
	buf[3] = (char) ((MAGIC >> 24) & 0xff);

	return PyString_FromStringAndSize(buf, 4);
}

static PyObject *
imp_get_suffixes(self, args)
	PyObject *self;
	PyObject *args;
{
	PyObject *list;
	struct filedescr *fdp;

	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	list = PyList_New(0);
	if (list == NULL)
		return NULL;
	for (fdp = _PyImport_Filetab; fdp->suffix != NULL; fdp++) {
		PyObject *item = Py_BuildValue("ssi",
				       fdp->suffix, fdp->mode, fdp->type);
		if (item == NULL) {
			Py_DECREF(list);
			return NULL;
		}
		if (PyList_Append(list, item) < 0) {
			Py_DECREF(list);
			Py_DECREF(item);
			return NULL;
		}
		Py_DECREF(item);
	}
	return list;
}

static PyObject *
imp_find_module(self, args)
	PyObject *self;
	PyObject *args;
{
	extern int fclose Py_PROTO((FILE *));
	char *name;
	PyObject *path = NULL;
	PyObject *fob, *ret;
	struct filedescr *fdp;
	char pathname[MAXPATHLEN+1];
	FILE *fp;
	if (!PyArg_ParseTuple(args, "s|O!", &name, &PyList_Type, &path))
		return NULL;
	fdp = find_module(name, path, pathname, MAXPATHLEN+1, &fp);
	if (fdp == NULL)
		return NULL;
	fob = PyFile_FromFile(fp, pathname, fdp->mode, fclose);
	if (fob == NULL) {
		fclose(fp);
		return NULL;
	}
	ret = Py_BuildValue("Os(ssi)",
		      fob, pathname, fdp->suffix, fdp->mode, fdp->type);
	Py_DECREF(fob);
	return ret;
}

static PyObject *
imp_init_builtin(self, args)
	PyObject *self;
	PyObject *args;
{
	char *name;
	int ret;
	PyObject *m;
	if (!PyArg_ParseTuple(args, "s", &name))
		return NULL;
	ret = init_builtin(name);
	if (ret < 0)
		return NULL;
	if (ret == 0) {
		Py_INCREF(Py_None);
		return Py_None;
	}
	m = PyImport_AddModule(name);
	Py_XINCREF(m);
	return m;
}

static PyObject *
imp_init_frozen(self, args)
	PyObject *self;
	PyObject *args;
{
	char *name;
	int ret;
	PyObject *m;
	if (!PyArg_ParseTuple(args, "s", &name))
		return NULL;
	ret = PyImport_ImportFrozenModule(name);
	if (ret < 0)
		return NULL;
	if (ret == 0) {
		Py_INCREF(Py_None);
		return Py_None;
	}
	m = PyImport_AddModule(name);
	Py_XINCREF(m);
	return m;
}

static PyObject *
imp_get_frozen_object(self, args)
	PyObject *self;
	PyObject *args;
{
	char *name;

	if (!PyArg_ParseTuple(args, "s", &name))
		return NULL;
	return get_frozen_object(name);
}

static PyObject *
imp_is_builtin(self, args)
	PyObject *self;
	PyObject *args;
{
	int i;
	char *name;
	if (!PyArg_ParseTuple(args, "s", &name))
		return NULL;
	for (i = 0; _PyImport_Inittab[i].name != NULL; i++) {
		if (strcmp(name, _PyImport_Inittab[i].name) == 0) {
			if (_PyImport_Inittab[i].initfunc == NULL)
				return PyInt_FromLong(-1);
			else
				return PyInt_FromLong(1);
		}
	}
	return PyInt_FromLong(0);
}

static PyObject *
imp_is_frozen(self, args)
	PyObject *self;
	PyObject *args;
{
	struct _frozen *p;
	char *name;
	if (!PyArg_ParseTuple(args, "s", &name))
		return NULL;
	for (p = PyImport_FrozenModules; ; p++) {
		if (p->name == NULL)
			break;
		if (strcmp(p->name, name) == 0)
			return PyInt_FromLong(1);
	}
	return PyInt_FromLong(0);
}

static FILE *
get_file(pathname, fob, mode)
	char *pathname;
	PyObject *fob;
	char *mode;
{
	FILE *fp;
	if (fob == NULL) {
		fp = fopen(pathname, mode);
		if (fp == NULL)
			PyErr_SetFromErrno(PyExc_IOError);
	}
	else {
		fp = PyFile_AsFile(fob);
		if (fp == NULL)
			PyErr_SetString(PyExc_ValueError,
					"bad/closed file object");
	}
	return fp;
}

static PyObject *
imp_load_compiled(self, args)
	PyObject *self;
	PyObject *args;
{
	char *name;
	char *pathname;
	PyObject *fob = NULL;
	PyObject *m;
	FILE *fp;
	if (!PyArg_ParseTuple(args, "ssO!", &name, &pathname,
			      &PyFile_Type, &fob))
		return NULL;
	fp = get_file(pathname, fob, "rb");
	if (fp == NULL)
		return NULL;
	m = load_compiled_module(name, pathname, fp);
	return m;
}

static PyObject *
imp_load_dynamic(self, args)
	PyObject *self;
	PyObject *args;
{
	char *name;
	char *pathname;
	PyObject *fob = NULL;
	PyObject *m;
	FILE *fp = NULL;
	if (!PyArg_ParseTuple(args, "ss|O!", &name, &pathname,
			      &PyFile_Type, &fob))
		return NULL;
	if (fob)
		fp = get_file(pathname, fob, "r");
	m = _PyImport_LoadDynamicModule(name, pathname, fp);
	return m;
}

static PyObject *
imp_load_source(self, args)
	PyObject *self;
	PyObject *args;
{
	char *name;
	char *pathname;
	PyObject *fob = NULL;
	PyObject *m;
	FILE *fp;
	if (!PyArg_ParseTuple(args, "ssO!", &name, &pathname,
			      &PyFile_Type, &fob))
		return NULL;
	fp = get_file(pathname, fob, "r");
	if (fp == NULL)
		return NULL;
	m = load_source_module(name, pathname, fp);
	return m;
}

#ifdef macintosh
static PyObject *
imp_load_resource(self, args)
	PyObject *self;
	PyObject *args;
{
	char *name;
	char *pathname;
	PyObject *m;

	if (!PyArg_ParseTuple(args, "ss", &name, &pathname))
		return NULL;
	m = PyMac_LoadResourceModule(name, pathname);
	return m;
}
#endif /* macintosh */

static PyObject *
imp_new_module(self, args)
	PyObject *self;
	PyObject *args;
{
	char *name;
	if (!PyArg_ParseTuple(args, "s", &name))
		return NULL;
	return PyModule_New(name);
}

static PyMethodDef imp_methods[] = {
	{"get_frozen_object",	imp_get_frozen_object,	1},
	{"get_magic",		imp_get_magic,		1},
	{"get_suffixes",	imp_get_suffixes,	1},
	{"find_module",		imp_find_module,	1},
	{"init_builtin",	imp_init_builtin,	1},
	{"init_frozen",		imp_init_frozen,	1},
	{"is_builtin",		imp_is_builtin,		1},
	{"is_frozen",		imp_is_frozen,		1},
	{"load_compiled",	imp_load_compiled,	1},
	{"load_dynamic",	imp_load_dynamic,	1},
	{"load_source",		imp_load_source,	1},
	{"new_module",		imp_new_module,		1},
#ifdef macintosh
	{"load_resource",	imp_load_resource,	1},
#endif
	{NULL,			NULL}		/* sentinel */
};

void
initimp()
{
	PyObject *m, *d, *v;

	m = Py_InitModule("imp", imp_methods);
	d = PyModule_GetDict(m);

	v = PyInt_FromLong(SEARCH_ERROR);
	PyDict_SetItemString(d, "SEARCH_ERROR", v);
	Py_XDECREF(v);

	v = PyInt_FromLong(PY_SOURCE);
	PyDict_SetItemString(d, "PY_SOURCE", v);
	Py_XDECREF(v);

	v = PyInt_FromLong(PY_COMPILED);
	PyDict_SetItemString(d, "PY_COMPILED", v);
	Py_XDECREF(v);

	v = PyInt_FromLong(C_EXTENSION);
	PyDict_SetItemString(d, "C_EXTENSION", v);
	Py_XDECREF(v);

#ifdef macintosh
	v = PyInt_FromLong(PY_RESOURCE);
	PyDict_SetItemString(d, "PY_RESOURCE", v);
	Py_XDECREF(v);
#endif


	if (PyErr_Occurred())
		Py_FatalError("imp module initialization failed");
}
