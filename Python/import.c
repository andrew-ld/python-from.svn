/***********************************************************
Copyright 1991, 1992, 1993, 1994 by Stichting Mathematisch Centrum,
Amsterdam, The Netherlands.

                        All Rights Reserved

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

******************************************************************/

/* Module definition and import implementation */

#include "allobjects.h"

#include "node.h"
#include "token.h"
#include "graminit.h"
#include "import.h"
#include "errcode.h"
#include "sysmodule.h"
#include "pythonrun.h"
#include "marshal.h"
#include "compile.h"
#include "eval.h"
#include "osdefs.h"

extern int verbose; /* Defined in pythonrun.c */

extern long getmtime(); /* In getmtime.c */

#ifdef DEBUG
#define D(x) x
#else
#define D(x)
#endif

/* Explanation of some of the the various #defines used by dynamic linking...

   symbol	-- defined for:

   DYNAMIC_LINK -- any kind of dynamic linking
   USE_RLD	-- NeXT dynamic linking
   USE_DL	-- Jack's dl for IRIX 4 or GNU dld with emulation for Jack's dl
   USE_SHLIB	-- SunOS or IRIX 5 (SVR4?) shared libraries
   _AIX		-- AIX style dynamic linking
   _DL_FUNCPTR_DEFINED	-- if the typedef dl_funcptr has been defined
   WITH_MAC_DL	-- Mac dynamic linking (highly experimental)

   (The other WITH_* symbols are used only once, to set the
   appropriate symbols.)
*/

/* Configure dynamic linking */

#if defined(NeXT) || defined(WITH_RLD)
#define DYNAMIC_LINK
#define USE_RLD
#endif

#ifdef WITH_SGI_DL
#define DYNAMIC_LINK
#define USE_DL
#endif

#ifdef WITH_DL_DLD
#define DYNAMIC_LINK
#define USE_DL
#endif

#ifdef WITH_MAC_DL
#define DYNAMIC_LINK
#endif

#if !defined(DYNAMIC_LINK) && defined(HAVE_DLFCN_H) && defined(HAVE_DLOPEN)
#define DYNAMIC_LINK
#define USE_SHLIB
#endif

#ifdef _AIX
#define DYNAMIC_LINK
#include <sys/ldr.h>
typedef void (*dl_funcptr)();
#define _DL_FUNCPTR_DEFINED
static void aix_loaderror(char *name);
#endif

#ifdef DYNAMIC_LINK

#ifdef USE_SHLIB
#include <dlfcn.h>
#ifndef _DL_FUNCPTR_DEFINED
typedef void (*dl_funcptr)();
#endif
#ifndef RTLD_LAZY
#define RTLD_LAZY 1
#endif
#endif /* USE_SHLIB */

#ifdef USE_DL
#include "dl.h"
#endif

#ifdef WITH_MAC_DL
#include "dynamic_load.h"
#endif

#ifdef USE_RLD
#include <mach-o/rld.h>
#define FUNCNAME_PATTERN "_init%s"
#ifndef _DL_FUNCPTR_DEFINED
typedef void (*dl_funcptr)();
#endif
#endif /* USE_RLD */

extern char *getprogramname();

#ifndef FUNCNAME_PATTERN
#define FUNCNAME_PATTERN "init%s"
#endif

#endif /* DYNAMIC_LINK */

/* Magic word to reject .pyc files generated by other Python versions */

#define MAGIC 0x999903L /* Increment by one for each incompatible change */

static object *modules;

/* Forward */
static int init_builtin PROTO((char *));

/* Initialization */

void
initimport()
{
	if ((modules = newdictobject()) == NULL)
		fatal("no mem for dictionary of modules");
}

object *
get_modules()
{
	return modules;
}

object *
add_module(name)
	char *name;
{
	object *m;
	if ((m = dictlookup(modules, name)) != NULL && is_moduleobject(m))
		return m;
	m = newmoduleobject(name);
	if (m == NULL)
		return NULL;
	if (dictinsert(modules, name, m) != 0) {
		DECREF(m);
		return NULL;
	}
	DECREF(m); /* Yes, it still exists, in modules! */
	return m;
}

enum filetype {SEARCH_ERROR, PY_SOURCE, PY_COMPILED, C_EXTENSION};

static struct filedescr {
	char *suffix;
	char *mode;
	enum filetype type;
} filetab[] = {
#ifdef DYNAMIC_LINK
#ifdef USE_SHLIB
	{"module.so", "rb", C_EXTENSION},
#else /* !USE_SHLIB */
	{"module.o", "rb", C_EXTENSION},
#endif /* !USE_SHLIB */
#endif /* DYNAMIC_LINK */
	{".py", "r", PY_SOURCE},
	{".pyc", "rb", PY_COMPILED},
	{0, 0}
};

#ifdef DYNAMIC_LINK
static object *
load_dynamic_module(name, namebuf, m, m_ret)
	char *name;
	char *namebuf;
	object *m;
	object **m_ret;
{
	char funcname[258];
	dl_funcptr p = NULL;
	if (m != NULL) {
		err_setstr(ImportError,
			   "cannot reload dynamically loaded module");
		return NULL;
	}
	sprintf(funcname, FUNCNAME_PATTERN, name);
#ifdef WITH_MAC_DL
	{
		object *v = dynamic_load(namebuf);
		if (v == NULL)
			return NULL;
	}
#else /* !WITH_MAC_DL */
#ifdef USE_SHLIB
	{
#ifdef RTLD_NOW
		/* RTLD_NOW: resolve externals now
		   (i.e. core dump now if some are missing) */
		void *handle = dlopen(namebuf, RTLD_NOW);
#else
		void *handle;
		if (verbose)
			printf("dlopen(\"%s\", %d);\n", namebuf, RTLD_LAZY);
		handle = dlopen(namebuf, RTLD_LAZY);
#endif /* RTLD_NOW */
		if (handle == NULL) {
			err_setstr(ImportError, dlerror());
			return NULL;
		}
		p = (dl_funcptr) dlsym(handle, funcname);
	}
#endif /* USE_SHLIB */
#ifdef _AIX
	p = (dl_funcptr) load(namebuf, 1, 0);
	if (p == NULL) {
		aix_loaderror(namebuf);
		return NULL;
	}
#endif /* _AIX */
#ifdef USE_DL
	p =  dl_loadmod(getprogramname(), namebuf, funcname);
#endif /* USE_DL */
#ifdef USE_RLD
	{
		NXStream *errorStream;
		struct mach_header *new_header;
		const char *filenames[2];
		long ret;
		unsigned long ptr;

		errorStream = NXOpenMemory(NULL, 0, NX_WRITEONLY);
		filenames[0] = namebuf;
		filenames[1] = NULL;
		ret = rld_load(errorStream, &new_header, 
				filenames, NULL);

		/* extract the error messages for the exception */
		if(!ret) {
			char *streamBuf;
			int len, maxLen;

			NXPutc(errorStream, (char)0);

			NXGetMemoryBuffer(errorStream,
				&streamBuf, &len, &maxLen);
			err_setstr(ImportError, streamBuf);
		}

		if(ret && rld_lookup(errorStream, funcname, &ptr))
			p = (dl_funcptr) ptr;

		NXCloseMemory(errorStream, NX_FREEBUFFER);

		if(!ret)
			return NULL;
	}
#endif /* USE_RLD */

	if (p == NULL) {
		err_setstr(ImportError,
		   "dynamic module does not define init function");
		return NULL;
	}
	(*p)();

#endif /* !WITH_MAC_DL */
	*m_ret = m = dictlookup(modules, name);
	if (m == NULL) {
		err_setstr(SystemError,
			   "dynamic module not initialized properly");
		return NULL;
	}
	if (verbose)
		fprintf(stderr,
			"import %s # dynamically loaded from %s\n",
			name, namebuf);
	INCREF(None);
	return None;
}
#endif /* DYNAMIC_LINK */

static object *
get_module(m, name, m_ret)
	/*module*/object *m;
	char *name;
	object **m_ret;
{
	int err, npath, i, len;
	long magic;
	long mtime, pyc_mtime;
	char namebuf[MAXPATHLEN+1];
	struct filedescr *fdp;
	FILE *fp = NULL, *fpc = NULL;
	node *n = NULL;
	object *path, *v, *d;
	codeobject *co = NULL;

	path = sysget("path");
	if (path == NULL || !is_listobject(path)) {
		err_setstr(ImportError,
			   "sys.path must be list of directory names");
		return NULL;
	}
	npath = getlistsize(path);
	for (i = 0; i < npath; i++) {
		v = getlistitem(path, i);
		if (!is_stringobject(v))
			continue;
		strcpy(namebuf, getstringvalue(v));
		len = getstringsize(v);
		if (len > 0 && namebuf[len-1] != SEP)
			namebuf[len++] = SEP;
		strcpy(namebuf+len, name);
		len += strlen(name);
		for (fdp = filetab; fdp->suffix != NULL; fdp++) {
			strcpy(namebuf+len, fdp->suffix);
			if (verbose > 1)
				fprintf(stderr, "# trying %s\n", namebuf);
			fp = fopen(namebuf, fdp->mode);
			if (fp != NULL)
				break;
		}
		if (fp != NULL)
			break;
	}
	if (fp == NULL) {
		sprintf(namebuf, "No module named %s", name);
		err_setstr(ImportError, namebuf);
		return NULL;
	}

	switch (fdp->type) {

	case PY_SOURCE:
		mtime = getmtime(namebuf);
		len = strlen(namebuf);
		strcpy(namebuf + len, "c");
		fpc = fopen(namebuf, "rb");
		if (fpc != NULL) {
			magic = rd_long(fpc);
			if (magic != MAGIC) {
				if (verbose)
					fprintf(stderr,
						"# %s has bad magic\n",
						namebuf);
			}
			else {
				pyc_mtime = rd_long(fpc);
				if (pyc_mtime != mtime) {
					if (verbose)
						fprintf(stderr,
						  "# %s has bad mtime\n",
						  namebuf);
				}
				else {
					fclose(fp);
					fp = fpc;
					if (verbose)
					   fprintf(stderr,
					     "# %s matches %s.py\n",
						   namebuf, name);
					goto use_compiled;
				}
			}
			fclose(fpc);
		}
		namebuf[len] = '\0';
		n = parse_file(fp, namebuf, file_input);
		fclose(fp);
		if (n == NULL)
			return NULL;
		co = compile(n, namebuf);
		freetree(n);
		if (co == NULL)
			return NULL;
		if (verbose)
			fprintf(stderr,
				"import %s # from %s\n", name, namebuf);
		/* Now write the code object to the ".pyc" file */
		strcpy(namebuf + len, "c");
		fpc = fopen(namebuf, "wb");
		if (fpc == NULL) {
			if (verbose)
				fprintf(stderr,
					"# can't create %s\n", namebuf);
		}
		else {
			wr_long(MAGIC, fpc);
			/* First write a 0 for mtime */
			wr_long(0L, fpc);
			wr_object((object *)co, fpc);
			if (ferror(fpc)) {
				if (verbose)
					fprintf(stderr,
						"# can't write %s\n", namebuf);
				/* Don't keep partial file */
				fclose(fpc);
				(void) unlink(namebuf);
			}
			else {
				/* Now write the true mtime */
				fseek(fpc, 4L, 0);
				wr_long(mtime, fpc);
				fflush(fpc);
				fclose(fpc);
				if (verbose)
					fprintf(stderr,
						"# wrote %s\n", namebuf);
			}
		}
		break;

	case PY_COMPILED:
		if (verbose)
			fprintf(stderr, "# %s without %s.py\n",
				namebuf, name);
		magic = rd_long(fp);
		if (magic != MAGIC) {
			err_setstr(ImportError,
				   "Bad magic number in .pyc file");
			return NULL;
		}
		(void) rd_long(fp);
	use_compiled:
		v = rd_object(fp);
		fclose(fp);
		if (v == NULL || !is_codeobject(v)) {
			XDECREF(v);
			err_setstr(ImportError,
				   "Bad code object in .pyc file");
			return NULL;
		}
		co = (codeobject *)v;
		if (verbose)
			fprintf(stderr,
				"import %s # precompiled from %s\n",
				name, namebuf);
		break;

#ifdef DYNAMIC_LINK
	case C_EXTENSION:
		fclose(fp);
		return load_dynamic_module(name, namebuf, m, m_ret);
#endif /* DYNAMIC_LINK */

	default:
		fclose(fp);
		err_setstr(SystemError,
			   "search loop returned unexpected result");
		return NULL;

	}

	/* We get here for either PY_SOURCE or PY_COMPILED */
	if (m == NULL) {
		m = add_module(name);
		if (m == NULL) {
			freetree(n);
			return NULL;
		}
		*m_ret = m;
	}
	d = getmoduledict(m);
	v = eval_code(co, d, d, d, (object *)NULL);
	DECREF(co);
	return v;
}

static object *
load_module(name)
	char *name;
{
	object *m, *v;
	v = get_module((object *)NULL, name, &m);
	if (v == NULL)
		return NULL;
	DECREF(v);
	return m;
}

object *
import_module(name)
	char *name;
{
	object *m;
	int n;
	if ((m = dictlookup(modules, name)) == NULL) {
		if ((n = init_builtin(name)) || (n = init_frozen(name))) {
			if (n < 0)
				return NULL;
			if ((m = dictlookup(modules, name)) == NULL)
				err_setstr(SystemError,
					   "builtin module missing");
		}
		else {
			m = load_module(name);
		}
	}
	return m;
}

object *
reload_module(m)
	object *m;
{
	char *name;
	int i;
	if (m == NULL || !is_moduleobject(m)) {
		err_setstr(TypeError, "reload() argument must be module");
		return NULL;
	}
	name = getmodulename(m);
	if (name == NULL)
		return NULL;
	/* Check for built-in modules */
	for (i = 0; inittab[i].name != NULL; i++) {
		if (strcmp(name, inittab[i].name) == 0) {
			err_setstr(ImportError,
				   "cannot reload built-in module");
			return NULL;
		}
	}
	/* Check for frozen modules */
	if ((i = init_frozen(name)) != 0) {
		if (i < 0)
			return NULL;
		INCREF(None);
		return None;
	}
	return get_module(m, name, (object **)NULL);
}

void
doneimport()
{
	if (modules != NULL) {
		int pos;
		object *modname, *module;
		/* Explicitly erase all modules; this is the safest way
		   to get rid of at least *some* circular dependencies */
		pos = 0;
		while (mappinggetnext(modules, &pos, &modname, &module)) {
			if (is_moduleobject(module)) {
				object *dict;
				dict = getmoduledict(module);
				if (dict != NULL && is_dictobject(dict))
					mappingclear(dict);
			}
		}
		mappingclear(modules);
	}
	DECREF(modules);
	modules = NULL;
}


/* Initialize built-in modules when first imported */

static int
init_builtin(name)
	char *name;
{
	int i;
	for (i = 0; inittab[i].name != NULL; i++) {
		if (strcmp(name, inittab[i].name) == 0) {
			if (inittab[i].initfunc == NULL) {
				err_setstr(ImportError,
					   "cannot re-init internal module");
				return -1;
			}
			if (verbose)
				fprintf(stderr, "import %s # builtin\n",
					name);
			(*inittab[i].initfunc)();
			return 1;
		}
	}
	return 0;
}

extern struct frozen {
	char *name;
	char *code;
	int size;
} frozen_modules[];

int
init_frozen(name)
	char *name;
{
	struct frozen *p;
	codeobject *co;
	object *m, *d, *v;
	for (p = frozen_modules; ; p++) {
		if (p->name == NULL)
			return 0;
		if (strcmp(p->name, name) == 0)
			break;
	}
	if (verbose)
		fprintf(stderr, "import %s # frozen\n", name);
	co = (codeobject *) rds_object(p->code, p->size);
	if (co == NULL)
		return -1;
	if ((m = add_module(name)) == NULL ||
	    (d = getmoduledict(m)) == NULL ||
	    (v = eval_code(co, d, d, d, (object*)NULL)) == NULL) {
		DECREF(co);
		return -1;
	}
	DECREF(co);
	DECREF(v);
	return 1;
}


#ifdef _AIX

#include <ctype.h>	/* for isdigit()	*/
#include <errno.h>	/* for global errno	*/
#include <string.h>	/* for strerror()	*/

void aix_loaderror(char *namebuf)
{

	char *message[8], errbuf[1024];
	int i,j;

	struct errtab { 
		int errno;
		char *errstr;
	} load_errtab[] = {
		{L_ERROR_TOOMANY,	"to many errors, rest skipped."},
		{L_ERROR_NOLIB,		"can't load library:"},
		{L_ERROR_UNDEF,		"can't find symbol in library:"},
		{L_ERROR_RLDBAD,
		 "RLD index out of range or bad relocation type:"},
		{L_ERROR_FORMAT,	"not a valid, executable xcoff file:"},
		{L_ERROR_MEMBER,
		 "file not an archive or does not contain requested member:"},
		{L_ERROR_TYPE,		"symbol table mismatch:"},
		{L_ERROR_ALIGN,		"text allignment in file is wrong."},
		{L_ERROR_SYSTEM,	"System error:"},
		{L_ERROR_ERRNO,		NULL}
	};

#define LOAD_ERRTAB_LEN	(sizeof(load_errtab)/sizeof(load_errtab[0]))
#define ERRBUF_APPEND(s)	strncat(errbuf, s, sizeof(errbuf))

	sprintf(errbuf, " from module %s ", namebuf);

	if (!loadquery(1, &message[0], sizeof(message))) 
		ERRBUF_APPEND(strerror(errno));
	for(i = 0; message[i] && *message[i]; i++) {
		int nerr = atoi(message[i]);
		for (j=0; j<LOAD_ERRTAB_LEN ; j++) {
		    if (nerr == load_errtab[i].errno && load_errtab[i].errstr)
			ERRBUF_APPEND(load_errtab[i].errstr);
		}
		while (isdigit(*message[i])) message[i]++ ; 
		ERRBUF_APPEND(message[i]);
		ERRBUF_APPEND("\n");
	}
	errbuf[strlen(errbuf)-1] = '\0' ;	/* trim off last newline */
	err_setstr(ImportError, errbuf); 
	return; 
}

#endif /* _AIX */
