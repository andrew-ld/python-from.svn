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

/* Python version information */

#include "patchlevel.h"

/* Return the version string.  This is constructed from the official
   version number, the patch level, and the current date (if known to
   the compiler, else a manually inserted date). */

#define VERSION "1.0.%d BETA 5 (%s)"

#ifdef __DATE__
#define DATE __DATE__
#else
#define DATE "January 1994"
#endif

char *
getversion()
{
	static char version[80];
	sprintf(version, VERSION, PATCHLEVEL, DATE);
	return version;
}


/* Return the copyright string.  This is updated manually. */

char *
getcopyright()
{
	return "Copyright 1991-1994 Stichting Mathematisch Centrum, Amsterdam";
}
