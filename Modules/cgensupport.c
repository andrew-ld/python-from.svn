/***********************************************************
Copyright 1991-1995 by Stichting Mathematisch Centrum, Amsterdam,
The Netherlands.

                        All Rights Reserved

Copyright (c) 2000, BeOpen.com.
Copyright (c) 1995-2000, Corporation for National Research Initiatives.
Copyright (c) 1990-1995, Stichting Mathematisch Centrum.
All rights reserved.

See the file "Misc/COPYRIGHT" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

******************************************************************/

/* Functions used by cgen output */

#include "Python.h"
#include "cgensupport.h"


/* Functions to extract arguments.
   These needs to know the total number of arguments supplied,
   since the argument list is a tuple only of there is more than
   one argument. */

int
PyArg_GetObject(args, nargs, i, p_arg)
	register PyObject *args;
	int nargs, i;
	PyObject **p_arg;
{
	if (nargs != 1) {
		if (args == NULL || !PyTuple_Check(args) ||
				nargs != PyTuple_Size(args) ||
				i < 0 || i >= nargs) {
			return PyErr_BadArgument();
		}
		else {
			args = PyTuple_GetItem(args, i);
		}
	}
	if (args == NULL) {
		return PyErr_BadArgument();
	}
	*p_arg = args;
	return 1;
}

int
PyArg_GetLong(args, nargs, i, p_arg)
	register PyObject *args;
	int nargs, i;
	long *p_arg;
{
	if (nargs != 1) {
		if (args == NULL || !PyTuple_Check(args) ||
				nargs != PyTuple_Size(args) ||
				i < 0 || i >= nargs) {
			return PyErr_BadArgument();
		}
		args = PyTuple_GetItem(args, i);
	}
	if (args == NULL || !PyInt_Check(args)) {
		return PyErr_BadArgument();
	}
	*p_arg = PyInt_AsLong(args);
	return 1;
}

int
PyArg_GetShort(args, nargs, i, p_arg)
	register PyObject *args;
	int nargs, i;
	short *p_arg;
{
	long x;
	if (!PyArg_GetLong(args, nargs, i, &x))
		return 0;
	*p_arg = (short) x;
	return 1;
}

static int
extractdouble(v, p_arg)
	register PyObject *v;
	double *p_arg;
{
	if (v == NULL) {
		/* Fall through to error return at end of function */
	}
	else if (PyFloat_Check(v)) {
		*p_arg = PyFloat_AS_DOUBLE((PyFloatObject *)v);
		return 1;
	}
	else if (PyInt_Check(v)) {
		*p_arg = PyInt_AS_LONG((PyIntObject *)v);
		return 1;
	}
	else if (PyLong_Check(v)) {
		*p_arg = PyLong_AsDouble(v);
		return 1;
	}
	return PyErr_BadArgument();
}

static int
extractfloat(v, p_arg)
	register PyObject *v;
	float *p_arg;
{
	if (v == NULL) {
		/* Fall through to error return at end of function */
	}
	else if (PyFloat_Check(v)) {
		*p_arg = (float) PyFloat_AS_DOUBLE((PyFloatObject *)v);
		return 1;
	}
	else if (PyInt_Check(v)) {
		*p_arg = (float) PyInt_AS_LONG((PyIntObject *)v);
		return 1;
	}
	else if (PyLong_Check(v)) {
		*p_arg = (float) PyLong_AsDouble(v);
		return 1;
	}
	return PyErr_BadArgument();
}

int
PyArg_GetFloat(args, nargs, i, p_arg)
	register PyObject *args;
	int nargs, i;
	float *p_arg;
{
	PyObject *v;
	float x;
	if (!PyArg_GetObject(args, nargs, i, &v))
		return 0;
	if (!extractfloat(v, &x))
		return 0;
	*p_arg = x;
	return 1;
}

int
PyArg_GetString(args, nargs, i, p_arg)
	PyObject *args;
	int nargs, i;
	string *p_arg;
{
	PyObject *v;
	if (!PyArg_GetObject(args, nargs, i, &v))
		return 0;
	if (!PyString_Check(v)) {
		return PyErr_BadArgument();
	}
	*p_arg = PyString_AsString(v);
	return 1;
}

int
PyArg_GetChar(args, nargs, i, p_arg)
	PyObject *args;
	int nargs, i;
	char *p_arg;
{
	string x;
	if (!PyArg_GetString(args, nargs, i, &x))
		return 0;
	if (x[0] == '\0' || x[1] != '\0') {
		/* Not exactly one char */
		return PyErr_BadArgument();
	}
	*p_arg = x[0];
	return 1;
}

int
PyArg_GetLongArraySize(args, nargs, i, p_arg)
	PyObject *args;
	int nargs, i;
	long *p_arg;
{
	PyObject *v;
	if (!PyArg_GetObject(args, nargs, i, &v))
		return 0;
	if (PyTuple_Check(v)) {
		*p_arg = PyTuple_Size(v);
		return 1;
	}
	if (PyList_Check(v)) {
		*p_arg = PyList_Size(v);
		return 1;
	}
	return PyErr_BadArgument();
}

int
PyArg_GetShortArraySize(args, nargs, i, p_arg)
	PyObject *args;
	int nargs, i;
	short *p_arg;
{
	long x;
	if (!PyArg_GetLongArraySize(args, nargs, i, &x))
		return 0;
	*p_arg = (short) x;
	return 1;
}

/* XXX The following four are too similar.  Should share more code. */

int
PyArg_GetLongArray(args, nargs, i, n, p_arg)
	PyObject *args;
	int nargs, i;
	int n;
	long *p_arg; /* [n] */
{
	PyObject *v, *w;
	if (!PyArg_GetObject(args, nargs, i, &v))
		return 0;
	if (PyTuple_Check(v)) {
		if (PyTuple_Size(v) != n) {
			return PyErr_BadArgument();
		}
		for (i = 0; i < n; i++) {
			w = PyTuple_GetItem(v, i);
			if (!PyInt_Check(w)) {
				return PyErr_BadArgument();
			}
			p_arg[i] = PyInt_AsLong(w);
		}
		return 1;
	}
	else if (PyList_Check(v)) {
		if (PyList_Size(v) != n) {
			return PyErr_BadArgument();
		}
		for (i = 0; i < n; i++) {
			w = PyList_GetItem(v, i);
			if (!PyInt_Check(w)) {
				return PyErr_BadArgument();
			}
			p_arg[i] = PyInt_AsLong(w);
		}
		return 1;
	}
	else {
		return PyErr_BadArgument();
	}
}

int
PyArg_GetShortArray(args, nargs, i, n, p_arg)
	PyObject *args;
	int nargs, i;
	int n;
	short *p_arg; /* [n] */
{
	PyObject *v, *w;
	if (!PyArg_GetObject(args, nargs, i, &v))
		return 0;
	if (PyTuple_Check(v)) {
		if (PyTuple_Size(v) != n) {
			return PyErr_BadArgument();
		}
		for (i = 0; i < n; i++) {
			w = PyTuple_GetItem(v, i);
			if (!PyInt_Check(w)) {
				return PyErr_BadArgument();
			}
			p_arg[i] = (short) PyInt_AsLong(w);
		}
		return 1;
	}
	else if (PyList_Check(v)) {
		if (PyList_Size(v) != n) {
			return PyErr_BadArgument();
		}
		for (i = 0; i < n; i++) {
			w = PyList_GetItem(v, i);
			if (!PyInt_Check(w)) {
				return PyErr_BadArgument();
			}
			p_arg[i] = (short) PyInt_AsLong(w);
		}
		return 1;
	}
	else {
		return PyErr_BadArgument();
	}
}

int
PyArg_GetDoubleArray(args, nargs, i, n, p_arg)
	PyObject *args;
	int nargs, i;
	int n;
	double *p_arg; /* [n] */
{
	PyObject *v, *w;
	if (!PyArg_GetObject(args, nargs, i, &v))
		return 0;
	if (PyTuple_Check(v)) {
		if (PyTuple_Size(v) != n) {
			return PyErr_BadArgument();
		}
		for (i = 0; i < n; i++) {
			w = PyTuple_GetItem(v, i);
			if (!extractdouble(w, &p_arg[i]))
				return 0;
		}
		return 1;
	}
	else if (PyList_Check(v)) {
		if (PyList_Size(v) != n) {
			return PyErr_BadArgument();
		}
		for (i = 0; i < n; i++) {
			w = PyList_GetItem(v, i);
			if (!extractdouble(w, &p_arg[i]))
				return 0;
		}
		return 1;
	}
	else {
		return PyErr_BadArgument();
	}
}

int
PyArg_GetFloatArray(args, nargs, i, n, p_arg)
	PyObject *args;
	int nargs, i;
	int n;
	float *p_arg; /* [n] */
{
	PyObject *v, *w;
	if (!PyArg_GetObject(args, nargs, i, &v))
		return 0;
	if (PyTuple_Check(v)) {
		if (PyTuple_Size(v) != n) {
			return PyErr_BadArgument();
		}
		for (i = 0; i < n; i++) {
			w = PyTuple_GetItem(v, i);
			if (!extractfloat(w, &p_arg[i]))
				return 0;
		}
		return 1;
	}
	else if (PyList_Check(v)) {
		if (PyList_Size(v) != n) {
			return PyErr_BadArgument();
		}
		for (i = 0; i < n; i++) {
			w = PyList_GetItem(v, i);
			if (!extractfloat(w, &p_arg[i]))
				return 0;
		}
		return 1;
	}
	else {
		return PyErr_BadArgument();
	}
}
