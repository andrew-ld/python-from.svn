# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

#error missing SetActionFilter

import string

# Declarations that change for each manager
MACHEADERFILE = 'Movies.h'		# The Apple header file
MODNAME = '_Qt'				# The name of the module
OBJECTNAME = 'Movie'			# The basic name of the objects used here

# The following is *usually* unchanged but may still require tuning
MODPREFIX = 'Qt'			# The prefix for module-wide routines
OBJECTTYPE = "Movie"		# The C type used to represent them
OBJECTPREFIX = MODPREFIX + 'Obj'	# The prefix for object methods
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
OUTPUTFILE = MODNAME + "module.c"	# The file generated by this program

from macsupport import *

# Create the type objects

includestuff = includestuff + """
#ifdef WITHOUT_FRAMEWORKS
#include <Movies.h>
#else
/* #include <Carbon/Carbon.h> */
#include <QuickTime/QuickTime.h>
#endif


#ifdef USE_TOOLBOX_OBJECT_GLUE
extern PyObject *_TrackObj_New(Track);
extern int _TrackObj_Convert(PyObject *, Track *);
extern PyObject *_MovieObj_New(Movie);
extern int _MovieObj_Convert(PyObject *, Movie *);
extern PyObject *_MovieCtlObj_New(MovieController);
extern int _MovieCtlObj_Convert(PyObject *, MovieController *);
extern PyObject *_TimeBaseObj_New(TimeBase);
extern int _TimeBaseObj_Convert(PyObject *, TimeBase *);
extern PyObject *_UserDataObj_New(UserData);
extern int _UserDataObj_Convert(PyObject *, UserData *);
extern PyObject *_MediaObj_New(Media);
extern int _MediaObj_Convert(PyObject *, Media *);

#define TrackObj_New _TrackObj_New
#define TrackObj_Convert _TrackObj_Convert
#define MovieObj_New _MovieObj_New
#define MovieObj_Convert _MovieObj_Convert
#define MovieCtlObj_New _MovieCtlObj_New
#define MovieCtlObj_Convert _MovieCtlObj_Convert
#define TimeBaseObj_New _TimeBaseObj_New
#define TimeBaseObj_Convert _TimeBaseObj_Convert
#define UserDataObj_New _UserDataObj_New
#define UserDataObj_Convert _UserDataObj_Convert
#define MediaObj_New _MediaObj_New
#define MediaObj_Convert _MediaObj_Convert
#endif

/* Macro to allow us to GetNextInterestingTime without duration */
#define GetMediaNextInterestingTimeOnly(media, flags, time, rate, rv) \
			GetMediaNextInterestingTime(media, flags, time, rate, rv, NULL)
			
/*
** Parse/generate time records
*/
static PyObject *
QtTimeRecord_New(TimeRecord *itself)
{
	if (itself->base)
		return Py_BuildValue("O&lO&", PyMac_Buildwide, &itself->value, itself->scale, 
			TimeBaseObj_New, itself->base);
	else
		return  Py_BuildValue("O&lO", PyMac_Buildwide, &itself->value, itself->scale, 
			Py_None);
}

static int
QtTimeRecord_Convert(PyObject *v, TimeRecord *p_itself)
{
	PyObject *base = NULL;
	if( !PyArg_ParseTuple(v, "O&l|O", PyMac_Getwide, &p_itself->value, &p_itself->scale,
			&base) )
		return 0;
	if ( base == NULL || base == Py_None )
		p_itself->base = NULL;
	else
		if ( !TimeBaseObj_Convert(base, &p_itself->base) )
			return 0;
	return 1;
}



"""

initstuff = initstuff + """
	PyMac_INIT_TOOLBOX_OBJECT_NEW(Track, TrackObj_New);
	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(Track, TrackObj_Convert);
	PyMac_INIT_TOOLBOX_OBJECT_NEW(Movie, MovieObj_New);
	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(Movie, MovieObj_Convert);
	PyMac_INIT_TOOLBOX_OBJECT_NEW(MovieController, MovieCtlObj_New);
	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(MovieController, MovieCtlObj_Convert);
	PyMac_INIT_TOOLBOX_OBJECT_NEW(TimeBase, TimeBaseObj_New);
	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(TimeBase, TimeBaseObj_Convert);
	PyMac_INIT_TOOLBOX_OBJECT_NEW(UserData, UserDataObj_New);
	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(UserData, UserDataObj_Convert);
	PyMac_INIT_TOOLBOX_OBJECT_NEW(Media, MediaObj_New);
	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(Media, MediaObj_Convert);
"""

# Our (opaque) objects
Movie = OpaqueByValueType('Movie', 'MovieObj')
NullMovie = FakeType("(Movie)0")
Track = OpaqueByValueType('Track', 'TrackObj')
Media = OpaqueByValueType('Media', 'MediaObj')
UserData = OpaqueByValueType('UserData', 'UserDataObj')
TimeBase = OpaqueByValueType('TimeBase', 'TimeBaseObj')
MovieController = OpaqueByValueType('MovieController', 'MovieCtlObj')

# Other opaque objects
Component = OpaqueByValueType('Component', 'CmpObj')
MediaHandlerComponent = OpaqueByValueType('MediaHandlerComponent', 'CmpObj')
DataHandlerComponent = OpaqueByValueType('DataHandlerComponent', 'CmpObj')

ComponentInstance = OpaqueByValueType('ComponentInstance', 'CmpInstObj')
MediaHandler = OpaqueByValueType('MediaHandler', 'CmpInstObj')
DataHandler = OpaqueByValueType('DataHandler', 'CmpInstObj')

RgnHandle = OpaqueByValueType("RgnHandle", "ResObj")
PicHandle = OpaqueByValueType("PicHandle", "ResObj")
CTabHandle = OpaqueByValueType("CTabHandle", "ResObj")
PixMapHandle = OpaqueByValueType("PixMapHandle", "ResObj")
SampleDescriptionHandle = OpaqueByValueType("SampleDescriptionHandle", "ResObj")
ImageDescriptionHandle = OpaqueByValueType("ImageDescriptionHandle", "ResObj")
TextDescriptionHandle = OpaqueByValueType("TextDescriptionHandle", "ResObj")
TEHandle = OpaqueByValueType("TEHandle", "ResObj")
CGrafPtr = OpaqueByValueType("CGrafPtr", "GrafObj")
GDHandle = OpaqueByValueType("GDHandle", "OptResObj")
AliasHandle = OpaqueByValueType("AliasHandle", "ResObj")
SoundDescriptionHandle = OpaqueByValueType("SoundDescriptionHandle", "ResObj")
# Silly Apple, passing an OStype by reference...
OSType_ptr = OpaqueType("OSType", "PyMac_BuildOSType", "PyMac_GetOSType")
# And even sillier: passing floats by address
float_ptr = ByAddressType("float", "f")

RGBColor = OpaqueType("RGBColor", "QdRGB")
RGBColor_ptr = RGBColor
TimeRecord = OpaqueType("TimeRecord", "QtTimeRecord")
TimeRecord_ptr = TimeRecord

# Non-opaque types, mostly integer-ish
TimeValue = Type("TimeValue", "l")
TimeScale = Type("TimeScale", "l")
TimeBaseFlags = Type("TimeBaseFlags", "l")
QTCallBackFlags = Type("QTCallBackFlags", "H")
TimeBaseStatus = Type("TimeBaseStatus", "l")
QTCallBackType = Type("QTCallBackType", "H")
nextTimeFlagsEnum = Type("nextTimeFlagsEnum", "H")
createMovieFileFlagsEnum = Type("createMovieFileFlagsEnum", "l")
movieFlattenFlagsEnum = Type("movieFlattenFlagsEnum", "l")
dataRefAttributesFlags = Type("dataRefAttributesFlags", "l")
playHintsEnum = Type("playHintsEnum", "l")
mediaHandlerFlagsEnum = Type("mediaHandlerFlagsEnum", "l")
ComponentResult = Type("ComponentResult", "l")
HandlerError = Type("HandlerError", "l")
Ptr = InputOnlyType("Ptr", "s")
StringPtr = Type("StringPtr", "s")
mcactionparams = InputOnlyType("void *", "s")
QTParameterDialog = Type("QTParameterDialog", "l")
QTAtomID = Type("QTAtomID", "l")
MCInterfaceElement = Type("MCInterfaceElement", "l")
CodecType = OSTypeType("CodecType")
GWorldPtr = OpaqueByValueType("GWorldPtr", "GWorldObj")
QTFloatSingle = Type("QTFloatSingle", "f")

# Could-not-be-bothered-types (NewMovieFromFile)
dummyshortptr = FakeType('(short *)0')
dummyStringPtr = FakeType('(StringPtr)0')

class MovieObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Qt_Error,"Cannot create null Movie");
					return NULL;
				}""")
	def outputFreeIt(self, itselfname):
		Output("DisposeMovie(%s);", itselfname)

class TrackObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Qt_Error,"Cannot create null Track");
					return NULL;
				}""")
	def outputFreeIt(self, itselfname):
		Output("DisposeMovieTrack(%s);", itselfname)

class MediaObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Qt_Error,"Cannot create null Media");
					return NULL;
				}""")
	def outputFreeIt(self, itselfname):
		Output("DisposeTrackMedia(%s);", itselfname)

class UserDataObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Qt_Error,"Cannot create null UserData");
					return NULL;
				}""")
	def outputFreeIt(self, itselfname):
		Output("DisposeUserData(%s);", itselfname)

class TimeBaseObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Qt_Error,"Cannot create null TimeBase");
					return NULL;
				}""")
##	def outputFreeIt(self, itselfname):
##		Output("DisposeTimeBase(%s);", itselfname)

class MovieCtlObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Qt_Error,"Cannot create null MovieController");
					return NULL;
				}""")
	def outputFreeIt(self, itselfname):
		Output("DisposeMovieController(%s);", itselfname)

# From here on it's basically all boiler plate...

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff)
Movie_object = MovieObjectDefinition('Movie', 'MovieObj', 'Movie')
Track_object = TrackObjectDefinition('Track', 'TrackObj', 'Track')
Media_object = MediaObjectDefinition('Media', 'MediaObj', 'Media')
UserData_object = UserDataObjectDefinition('UserData', 'UserDataObj', 'UserData')
TimeBase_object = TimeBaseObjectDefinition('TimeBase', 'TimeBaseObj', 'TimeBase')
MovieController_object = MovieCtlObjectDefinition('MovieController', 'MovieCtlObj', 'MovieController')

module.addobject(MovieController_object)
module.addobject(TimeBase_object)
module.addobject(UserData_object)
module.addobject(Media_object)
module.addobject(Track_object)
module.addobject(Movie_object)

# Create the generator classes used to populate the lists
Function = OSErrWeakLinkFunctionGenerator
Method = OSErrWeakLinkMethodGenerator

# Create and populate the lists
functions = []
MovieController_methods = []
TimeBase_methods = []
UserData_methods = []
Media_methods = []
Track_methods = []
Movie_methods = []
execfile(INPUTFILE)

#
# Some functions from ImageCompression.h that we need:
ICMAlignmentProcRecordPtr = FakeType('(ICMAlignmentProcRecordPtr)0')
dummyRect = FakeType('(Rect *)0')

f = Function(void, 'AlignWindow',
	(WindowPtr, 'wp', InMode),
	(Boolean, 'front', InMode),
	(dummyRect, 'alignmentRect', InMode),
	(ICMAlignmentProcRecordPtr, 'alignmentProc', InMode),
)
functions.append(f)

f = Function(void, 'DragAlignedWindow',
	(WindowPtr, 'wp', InMode),
	(Point, 'startPt', InMode),
	(Rect_ptr, 'boundsRect', InMode),
	(dummyRect, 'alignmentRect', InMode),
	(ICMAlignmentProcRecordPtr, 'alignmentProc', InMode),
)
functions.append(f)

# And we want the version of MoviesTask without a movie argument
f = Function(void, 'MoviesTask',
    (NullMovie, 'theMovie', InMode),
    (long, 'maxMilliSecToUse', InMode),
)
functions.append(f)

# And we want a GetMediaNextInterestingTime without duration
f = Method(void, 'GetMediaNextInterestingTimeOnly',
    (Media, 'theMedia', InMode),
    (short, 'interestingTimeFlags', InMode),
    (TimeValue, 'time', InMode),
    (Fixed, 'rate', InMode),
    (TimeValue, 'interestingTime', OutMode),
)
Media_methods.append(f)

# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
for f in MovieController_methods: MovieController_object.add(f)
for f in TimeBase_methods: TimeBase_object.add(f)
for f in UserData_methods: UserData_object.add(f)
for f in Media_methods: Media_object.add(f)
for f in Track_methods: Track_object.add(f)
for f in Movie_methods: Movie_object.add(f)

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()

