/***********************************************************
Copyright 1991-1997 by Stichting Mathematisch Centrum, Amsterdam,
The Netherlands.

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


#include "Python.h"

#include "macglue.h"
#include "marshal.h"
#include "import.h"
#include "importdl.h"
#include "pymactoolbox.h"

#include "pythonresources.h"

#ifdef WITHOUT_FRAMEWORKS
#include <OSUtils.h> /* for Set(Current)A5 */
#include <Files.h>
#include <StandardFile.h>
#include <Resources.h>
#include <Memory.h>
#include <Windows.h>
#include <Traps.h>
#include <Processes.h>
#include <Fonts.h>
#include <Menus.h>
#include <TextUtils.h>
#include <LowMem.h>
#include <Events.h>
#else
#include <Carbon/Carbon.h>
#endif

#ifdef __MWERKS__
#include <SIOUX.h>
extern void SIOUXSetupMenus(void);
extern void SIOUXDoAboutBox(void);
#endif
#ifdef USE_GUSI
/* Functions we redefine because they're in obscure libraries */
extern void SpinCursor(short x);
extern void RotateCursor(short x);
extern pascal unsigned char * PLstrcpy(unsigned char *, const unsigned char *);
extern pascal short PLstrcmp(const unsigned char *, const unsigned char *);
extern pascal char *PLstrrchr(const unsigned char *, short);

#endif

/* The ID of the Sioux apple menu */
#define SIOUX_APPLEID	32000

#include <signal.h>
#include <stdio.h>

/*
** When less than this amount of stackspace is left we
** raise a MemoryError.
*/
#ifndef MINIMUM_STACK_SIZE
#define MINIMUM_STACK_SIZE 8192
#endif

/*
** On MacOSX StackSpace() lies: it gives the distance from heap end to stack pointer,
** but the stack cannot grow that far due to rlimit values. We cannot get at this value
** from Carbon, so we set a maximum to the stack here that is based on the default
** stack limit of 512K.
*/
#define MAXIMUM_STACK_SIZE (256*1024)

/*
** We have to be careful, since we can't handle
** things like updates (and they'll keep coming back if we don't
** handle them). Note that we don't know who has windows open, so
** even handing updates off to SIOUX under MW isn't going to work.
*/
#define MAINLOOP_EVENTMASK (mDownMask|keyDownMask|osMask|activMask)

#include <signal.h>

/* XXX We should include Errors.h here, but it has a name conflict
** with the python errors.h. */
#define fnfErr -43

/* Interrupt code variables: */
static int interrupted;			/* Set to true when cmd-. seen */
static RETSIGTYPE intcatcher(int);

#if !TARGET_API_MAC_OSX
static int PyMac_Yield(void);
#endif

/*
** These are the real scheduling parameters that control what we check
** in the event loop, and how often we check. The values are initialized
** from pyMac_SchedParamStruct.
*/

struct real_sched_param_struct {
	int		check_interrupt;	/* if true check for command-dot */
	int		process_events;		/* if nonzero enable evt processing, this mask */
	int		besocial;		/* if nonzero be a little social with CPU */
	unsigned long	check_interval;		/* how often to check, in ticks */
	unsigned long	bg_yield;		/* yield so long when in background */
	/* these are computed from previous and clock and such */
	int		enabled;		/* check_interrupt OR process_event OR yield */
	unsigned long	next_check;		/* when to check/yield next, in ticks */
};

static struct real_sched_param_struct schedparams =
	{ 1, MAINLOOP_EVENTMASK, 1, 15, 15, 1, 0};

/*
** Workaround for sioux/gusi combo: set when we are exiting
*/
int PyMac_ConsoleIsDead;

/*
** Sioux menu bar, saved early so we can restore it
*/
static MenuBarHandle sioux_mbar;

/*
** The python-code event handler
*/
static PyObject *python_event_handler;

/* Given an FSSpec, return the FSSpec of the parent folder */

static OSErr
get_folder_parent (FSSpec * fss, FSSpec * parent)
{
	CInfoPBRec rec;
	short err;

        * parent = * fss;
        rec.hFileInfo.ioNamePtr = parent->name;
        rec.hFileInfo.ioVRefNum = parent->vRefNum;
        rec.hFileInfo.ioDirID = parent->parID;
		rec.hFileInfo.ioFDirIndex = -1;
        rec.hFileInfo.ioFVersNum = 0;
        if (err = PBGetCatInfoSync (& rec))
        	return err;
        parent->parID = rec.dirInfo.ioDrParID;
/*	parent->name[0] = 0; */
        return 0;
}

/* Given an FSSpec return a full, colon-separated pathname */

OSErr
PyMac_GetFullPathname (FSSpec *fss, char *buf, int length)
{
	short err;
	FSSpec fss_parent, fss_current;
	char tmpbuf[1024];
	int plen;

	fss_current = *fss;
	plen = fss_current.name[0];
	if ( plen+2 > length ) {
		*buf = 0;
		return errFSNameTooLong;
	}
	memcpy(buf, &fss_current.name[1], plen);
	buf[plen] = 0;
	/* Special case for disk names */
	if ( fss_current.parID <= 1 ) {
		buf[plen++] = ':';
		buf[plen] = 0;
		return 0;
	}
	while (fss_current.parID > 1) {
    		/* Get parent folder name */
                if (err = get_folder_parent(&fss_current, &fss_parent)) {
                	*buf = 0;
             		return err;
             	}
                fss_current = fss_parent;
                /* Prepend path component just found to buf */
    			plen = fss_current.name[0];
    			if (strlen(buf) + plen + 1 > 1024) {
    				/* Oops... Not enough space (shouldn't happen) */
    				*buf = 0;
    				return errFSNameTooLong;
    			}
    			memcpy(tmpbuf, &fss_current.name[1], plen);
    			tmpbuf[plen] = ':';
    			strcpy(&tmpbuf[plen+1], buf);
    			if ( strlen(tmpbuf) > length ) {
    				*buf = 0;
    				return errFSNameTooLong;
    			}
    			strcpy(buf, tmpbuf);
        }
        return 0;
}


#ifdef USE_GUSI
/*
** SpinCursor (needed by GUSI) drags in heaps of stuff, so we
** provide a dummy here.
*/
void SpinCursor(short x) { /* Dummy */ }
void RotateCursor(short x) { /* Dummy */ }


/* Called at exit() time thru atexit(), to stop event processing */
void
PyMac_StopGUSISpin() {
	PyMac_ConsoleIsDead = 1;
}

#endif /* USE_GUSI */


/* Convert C to Pascal string. Returns pointer to static buffer. */
unsigned char *
Pstring(char *str)
{
	static Str255 buf;
	int len;

	len = strlen(str);
	if (len > 255)
		len = 255;
	buf[0] = (unsigned char)len;
	strncpy((char *)buf+1, str, len);
	return buf;
}


#ifdef USE_STACKCHECK
/* Check for stack overflow */
int
PyOS_CheckStack()
{
	char here;
	static char *sentinel = 0;
	static PyThreadState *thread_for_sentinel = 0;
	
	if ( sentinel == 0 ) {
		unsigned long stackspace = StackSpace();
		
#ifdef MAXIMUM_STACK_SIZE
	/* See the comment at the definition */
	if ( stackspace > MAXIMUM_STACK_SIZE )
		stackspace = MAXIMUM_STACK_SIZE;
#endif	
		sentinel = &here - stackspace + MINIMUM_STACK_SIZE;
	}
	if ( thread_for_sentinel == 0 ) {
		thread_for_sentinel = PyThreadState_Get();
	}
	if ( &here < sentinel ) {
		if (thread_for_sentinel == PyThreadState_Get()) {
			return -1;
		}
	}
	return 0;
}
#endif /* USE_STACKCHECK */

#if !TARGET_API_MAC_OSX
void
PyErr_SetInterrupt(void)
{
	interrupted = 1;
}

/* The catcher routine (which may not be used for all compilers) */
static RETSIGTYPE
intcatcher(sig)
	int sig;
{
	interrupted = 1;
	signal(SIGINT, intcatcher);
}

void
PyOS_InitInterrupts()
{
	if (signal(SIGINT, SIG_IGN) != SIG_IGN)
		signal(SIGINT, intcatcher);
}

void
PyOS_FiniInterrupts()
{
}

/* Check whether we are in the foreground */
static int
PyMac_InForeground(void)
{
	static ProcessSerialNumber ours;
	static inited;
	ProcessSerialNumber curfg;
	Boolean eq;
	
	if ( inited == 0 ) {
		(void)GetCurrentProcess(&ours);
		inited = 1;
	}
	if ( GetFrontProcess(&curfg) < 0 )
		eq = 1;
	else if ( SameProcess(&ours, &curfg, &eq) < 0 )
		eq = 1;
	return (int)eq;
}

/*
** This routine scans the event queue looking for cmd-.
*/
static void
scan_event_queue(force)
	int force;
{
	if ( interrupted || (!schedparams.check_interrupt && !force) )
		return;
	if ( CheckEventQueueForUserCancel() )
		interrupted = 1;
}

int
PyErr_CheckSignals()
{
	if (schedparams.enabled) {
		if ( interrupted || (unsigned long)TickCount() > schedparams.next_check ) {
			scan_event_queue(0);
			if (interrupted) {
				interrupted = 0;
				PyErr_SetNone(PyExc_KeyboardInterrupt);
				return -1;
			}
			if ( PyMac_Yield() < 0)
				return -1;
			schedparams.next_check = (unsigned long)TickCount()
					 + schedparams.check_interval;
		}
	}
	return 0;
}

int
PyOS_InterruptOccurred()
{
	scan_event_queue(0);
	if ( !interrupted )
		return 0;
	interrupted = 0;
	return 1;
}
#endif

int
PyMac_SetEventHandler(PyObject *evh)
{
	if ( evh && python_event_handler ) {
		PyErr_SetString(PyExc_RuntimeError, "Python event handler already set");
		return 0;
	}
	if ( python_event_handler )
		Py_DECREF(python_event_handler);
	if ( evh )
		Py_INCREF(evh);
	python_event_handler = evh;
	return 1;
}

/*
** Handle an event, either one found in the mainloop eventhandler or
** one passed back from the python program.
*/
void
PyMac_HandleEventIntern(evp)
	EventRecord *evp;
{
#ifdef __MWERKS__
	{
		int siouxdidit;

		/* If SIOUX wants it we're done */
		siouxdidit = SIOUXHandleOneEvent(evp);
		if ( siouxdidit )
			return;
	}
#else
	/* Other compilers are just unlucky... */
#endif /* !__MWERKS__ */
}

/*
** Handle an event, either through HandleEvent or by passing it to the Python
** event handler.
*/
int
PyMac_HandleEvent(evp)
	EventRecord *evp;
{
	PyObject *rv;
	
	if ( python_event_handler ) {
		rv = PyObject_CallFunction(python_event_handler, "(O&)", 
			PyMac_BuildEventRecord, evp);
		if ( rv )
			Py_DECREF(rv);
		else
			return -1;	/* Propagate exception */
	} else {
		PyMac_HandleEventIntern(evp);
	}
	return 0;
}

#if !TARGET_API_MAC_OSX
/*
** Yield the CPU to other tasks without processing events.
*/
int
PyMac_DoYield(int maxsleep, int maycallpython)
{
	EventRecord ev;
	int gotone;
	long latest_time_ready;
	static int in_here = 0;
	
	in_here++;
		
	/*
	** Check which of the eventloop cases we have:
	** - process events
	** - don't process events but do yield
	** - do neither
	*/
	if( in_here > 1 || !schedparams.process_events || 
	    (python_event_handler && !maycallpython) ) {
		if ( maxsleep >= 0 ) {
			/* XXXX Need to do something here */
		}
	} else {
		latest_time_ready = TickCount() + maxsleep;
		do {
			/* XXXX Hack by Jack.
			** In time.sleep() you can click to another application
			** once only. If you come back to Python you cannot get away
			** again.
			**/
			gotone = WaitNextEvent(schedparams.process_events, &ev, maxsleep, NULL);	
			/* Get out quickly if nothing interesting is happening */
			if ( !gotone || ev.what == nullEvent )
				break;
			if ( PyMac_HandleEvent(&ev) < 0 ) {
				in_here--;
				return -1;
			}
			maxsleep = latest_time_ready - TickCount();
		} while ( maxsleep > 0 );
	}
	in_here--;
	return 0;
}

/*
** Process events and/or yield the CPU to other tasks if opportune
*/
int
PyMac_Yield() {
	unsigned long maxsleep;
	
	if( PyMac_InForeground() )
		maxsleep = 0;
	else
		maxsleep = schedparams.bg_yield;

	return PyMac_DoYield(maxsleep, 1);
}

/*
** Return current scheduler parameters
*/
void
PyMac_GetSchedParams(PyMacSchedParams *sp)
{
	sp->check_interrupt = schedparams.check_interrupt;
	sp->process_events = schedparams.process_events;
	sp->besocial = schedparams.besocial;
	sp->check_interval = schedparams.check_interval / 60.0;
	sp->bg_yield = schedparams.bg_yield / 60.0;
}

/*
** Set current scheduler parameters
*/
void
PyMac_SetSchedParams(PyMacSchedParams *sp)
{
	schedparams.check_interrupt = sp->check_interrupt;
	schedparams.process_events = sp->process_events;
	schedparams.besocial = sp->besocial;
	schedparams.check_interval = (unsigned long)(sp->check_interval*60);
	schedparams.bg_yield = (unsigned long)(sp->bg_yield*60);
	if ( schedparams.check_interrupt || schedparams.process_events ||
	     schedparams.besocial )
	     	schedparams.enabled = 1;
	else
		schedparams.enabled = 0;
	schedparams.next_check = 0;	/* Check immedeately */
}

/*
** Install our menu bar.
*/
void
PyMac_InitMenuBar()
{
	MenuHandle applemenu;
	Str255 about_text;
	static unsigned char about_sioux[] = "\pAbout SIOUX";
	
	if ( sioux_mbar ) return;
	if ( (sioux_mbar=GetMenuBar()) == NULL || GetMenuHandle(SIOUX_APPLEID) == NULL)  {
		/* Sioux menu not installed yet. Do so */
		SIOUXSetupMenus();
		if ( (sioux_mbar=GetMenuBar()) == NULL )
			return;
	}
	if ( (applemenu=GetMenuHandle(SIOUX_APPLEID)) == NULL ) return;
	GetMenuItemText(applemenu, 1, about_text);
	if ( about_text[0] == about_sioux[0] && 
		strncmp((char *)(about_text+1), (char *)(about_sioux+1), about_text[0]) == 0 )
		SetMenuItemText(applemenu, 1, "\pAbout Python...");
}

/*
** Restore sioux menu bar
*/
void
PyMac_RestoreMenuBar()
{
	MenuBarHandle curmenubar;
	
	curmenubar = GetMenuBar();
	if ( sioux_mbar ) {
		SetMenuBar(sioux_mbar);
		DrawMenuBar();
	} else {
		PyMac_InitMenuBar();
		DrawMenuBar();
	}
}

void
PyMac_RaiseConsoleWindow()
{
	/* Note: this is a hack. SIOUXTextWindow is SIOUX's internal structure
	** and we happen to know that the first entry is the window pointer.
	*/
	extern WindowRef *SIOUXTextWindow;

	if ( SIOUXTextWindow == NULL || *SIOUXTextWindow == NULL )
		return;
	if ( FrontWindow() != *SIOUXTextWindow )
		BringToFront(*SIOUXTextWindow);
}

/*
** Our replacement about box
*/

#include "patchlevel.h"

void
SIOUXDoAboutBox(void)
{
	DialogPtr theDialog;
	WindowPtr theWindow;
	short item;
	short fontID;
	
	if( (theDialog = GetNewDialog(ABOUT_ID, NULL, (WindowPtr)-1)) == NULL )
		return;
	theWindow = GetDialogWindow(theDialog);
	SetPortWindowPort(theWindow);
	GetFNum("\pPython-Sans", &fontID);
	if (fontID == 0)
		fontID = kFontIDGeneva;
	TextFont(fontID);
	TextSize(9);
	ParamText(Pstring(PY_VERSION), "\p", "\p", "\p");
	ShowWindow(theWindow);
	ModalDialog(NULL, &item);
	DisposeDialog(theDialog);
}

#endif /* !TARGET_API_MAC_OSX */
