/* appinit.c -- Tcl and Tk application initialization.

   The function Tcl_AppInit() below initializes various Tcl packages.
   It is called for each Tcl interpreter created by _tkinter.create().
   It needs to be compiled with -DWITH_<package> flags for each package
   that you are statically linking with.  You may have to add sections
   for packages not yet listed below.

   Note that those packages for which Tcl_StaticPackage() is called with
   a NULL first argument are known as "static loadable" packages to
   Tcl but not actually initialized.  To use these, you have to load
   it explicitly, e.g. tkapp.eval("load {} Blt").
 */

#include <tcl.h>
#include <tk.h>

int
Tcl_AppInit(Tcl_Interp *interp)
{
	Tk_Window main_window;

#ifdef TK_AQUA
#ifndef MAX_PATH_LEN
#define MAX_PATH_LEN 1024
#endif
	char tclLibPath[MAX_PATH_LEN], tkLibPath[MAX_PATH_LEN];
	Tcl_Obj*	pathPtr;

        /* pre- Tcl_Init code copied from tkMacOSXAppInit.c */
	Tk_MacOSXOpenBundleResources (interp, "com.tcltk.tcllibrary",
       	tclLibPath, MAX_PATH_LEN, 0);

	if (tclLibPath[0] != '\0') {
       	Tcl_SetVar(interp, "tcl_library", tclLibPath, TCL_GLOBAL_ONLY);
		Tcl_SetVar(interp, "tclDefaultLibrary", tclLibPath, TCL_GLOBAL_ONLY);
		Tcl_SetVar(interp, "tcl_pkgPath", tclLibPath, TCL_GLOBAL_ONLY);
	}
	
   	if (tclLibPath[0] != '\0') {
		Tcl_SetVar(interp, "tcl_library", tclLibPath, TCL_GLOBAL_ONLY);
		Tcl_SetVar(interp, "tclDefaultLibrary", tclLibPath, TCL_GLOBAL_ONLY);
		Tcl_SetVar(interp, "tcl_pkgPath", tclLibPath, TCL_GLOBAL_ONLY);
	}
#endif
	if (Tcl_Init (interp) == TCL_ERROR)
		return TCL_ERROR;

#ifdef TK_AQUA
        /* pre- Tk_Init code copied from tkMacOSXAppInit.c */
	Tk_MacOSXOpenBundleResources (interp, "com.tcltk.tklibrary",
            tkLibPath, MAX_PATH_LEN, 1);

	if (tclLibPath[0] != '\0') {
		pathPtr = Tcl_NewStringObj(tclLibPath, -1);
	} else {
		Tcl_Obj *pathPtr = TclGetLibraryPath();
	}

	if (tkLibPath[0] != '\0') {
		Tcl_Obj *objPtr;

		Tcl_SetVar(interp, "tk_library", tkLibPath, TCL_GLOBAL_ONLY);
		objPtr = Tcl_NewStringObj(tkLibPath, -1);
		Tcl_ListObjAppendElement(NULL, pathPtr, objPtr);
	}

	TclSetLibraryPath(pathPtr);
#endif

	if (Tk_Init (interp) == TCL_ERROR)
		return TCL_ERROR;

	main_window = Tk_MainWindow(interp);

#ifdef TK_AQUA
	TkMacOSXInitAppleEvents(interp);
	TkMacOSXInitMenus(interp);
#endif
    
#ifdef WITH_MOREBUTTONS
	{
		extern Tcl_CmdProc studButtonCmd;
		extern Tcl_CmdProc triButtonCmd;

		Tcl_CreateCommand(interp, "studbutton", studButtonCmd,
				  (ClientData) main_window, NULL);
		Tcl_CreateCommand(interp, "tributton", triButtonCmd,
				  (ClientData) main_window, NULL);
	}
#endif

#ifdef WITH_PIL /* 0.2b5 and later -- not yet released as of May 14 */
	{
		extern void TkImaging_Init(Tcl_Interp *);
		TkImaging_Init(interp);
		/* XXX TkImaging_Init() doesn't have the right return type */
		/*Tcl_StaticPackage(interp, "Imaging", TkImaging_Init, NULL);*/
	}
#endif

#ifdef WITH_PIL_OLD /* 0.2b4 and earlier */
	{
		extern void TkImaging_Init(void);
		/* XXX TkImaging_Init() doesn't have the right prototype */
		/*Tcl_StaticPackage(interp, "Imaging", TkImaging_Init, NULL);*/
	}
#endif

#ifdef WITH_TIX
        {
                extern int Tix_Init(Tcl_Interp *interp);
                extern int Tix_SafeInit(Tcl_Interp *interp);
                Tcl_StaticPackage(NULL, "Tix", Tix_Init, Tix_SafeInit);
        }
#endif

#ifdef WITH_BLT
	{
		extern int Blt_Init(Tcl_Interp *);
		extern int Blt_SafeInit(Tcl_Interp *);
		Tcl_StaticPackage(NULL, "Blt", Blt_Init, Blt_SafeInit);
	}
#endif

#ifdef WITH_TOGL
	{
		/* XXX I've heard rumors that this doesn't work */
		extern int Togl_Init(Tcl_Interp *);
		/* XXX Is there no Togl_SafeInit? */
		Tcl_StaticPackage(NULL, "Togl", Togl_Init, NULL);
	}
#endif

#ifdef WITH_XXX

#endif
	return TCL_OK;
}
