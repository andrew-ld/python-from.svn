# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

#error missing SetActionFilter

import string

# Declarations that change for each manager
MACHEADERFILE = 'Movies.h'		# The Apple header file
MODNAME = 'Qt'				# The name of the module
OBJECTNAME = 'Movie'			# The basic name of the objects used here

# The following is *usually* unchanged but may still require tuning
MODPREFIX = MODNAME			# The prefix for module-wide routines
OBJECTTYPE = "Movie"		# The C type used to represent them
OBJECTPREFIX = MODPREFIX + 'Obj'	# The prefix for object methods
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
OUTPUTFILE = MODNAME + "module.c"	# The file generated by this program

from macsupport import *

# Create the type objects

includestuff = includestuff + """
#include <%s>""" % MACHEADERFILE + """

/* Exported by Cmmodule.c: */
extern PyObject *CmpObj_New(Component);
extern int CmpObj_Convert(PyObject *, Component *);
extern PyObject *CmpInstObj_New(ComponentInstance);
extern int CmpInstObj_Convert(PyObject *, ComponentInstance *);

/* Exported by Qdmodule.c: */
extern PyObject *QdRGB_New(RGBColor *);
extern int QdRGB_Convert(PyObject *, RGBColor *);

/* Our own, used before defined: */
staticforward PyObject *TrackObj_New(Track);
staticforward int TrackObj_Convert(PyObject *, Track *);
staticforward PyObject *MovieObj_New(Movie);
staticforward int MovieObj_Convert(PyObject *, Movie *);
staticforward PyObject *MovieCtlObj_New(MovieController);
staticforward int MovieCtlObj_Convert(PyObject *, MovieController *);


"""

# Our (opaque) objects
Movie = OpaqueByValueType('Movie', 'MovieObj')
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
TEHandle = OpaqueByValueType("TEHandle", "ResObj")
# Silly Apple, passing an OStype by reference...
OSType_ptr = OpaqueType("OSType", "PyMac_BuildOSType", "PyMac_GetOSType")

RGBColor = OpaqueType("RGBColor", "QdRGB")
RGBColor_ptr = OpaqueType("RGBColor", "QdRGB")

# Non-opaque types, mostly integer-ish
TimeValue = Type("TimeValue", "l")
TimeScale = Type("TimeScale", "l")
TimeBaseFlags = Type("TimeBaseFlags", "l")
QTCallBackFlags = Type("QTCallBackFlags", "h")
TimeBaseStatus = Type("TimeBaseStatus", "l")
QTCallBackType = Type("QTCallBackType", "h")
nextTimeFlagsEnum = Type("nextTimeFlagsEnum", "h")
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

# Could-not-be-bothered-types (NewMovieFromFile)
dummyshortptr = FakeType('(short *)0')
dummyStringPtr = FakeType('(StringPtr)0')

class MovieObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Qt_Error,"Cannot create null Movie");
					return NULL;
				}""")
	def outputFreeIt(self, itselfname):
		Output("DisposeMovie(%s);", itselfname)

class TrackObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Qt_Error,"Cannot create null Track");
					return NULL;
				}""")
	def outputFreeIt(self, itselfname):
		Output("DisposeMovieTrack(%s);", itselfname)

class MediaObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Qt_Error,"Cannot create null Media");
					return NULL;
				}""")
	def outputFreeIt(self, itselfname):
		Output("DisposeTrackMedia(%s);", itselfname)

class UserDataObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Qt_Error,"Cannot create null UserData");
					return NULL;
				}""")
	def outputFreeIt(self, itselfname):
		Output("DisposeUserData(%s);", itselfname)

class TimeBaseObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Qt_Error,"Cannot create null TimeBase");
					return NULL;
				}""")
	def outputFreeIt(self, itselfname):
		Output("DisposeTimeBase(%s);", itselfname)

class MovieCtlObjectDefinition(GlobalObjectDefinition):
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
Function = OSErrFunctionGenerator
Method = OSErrMethodGenerator

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

