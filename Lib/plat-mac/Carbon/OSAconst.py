# Generated from 'OSA.h'

def FOUR_CHAR_CODE(x): return x
from Carbon.AppleEvents import *
kAEUseStandardDispatch = -1
kOSAComponentType = FOUR_CHAR_CODE('osa ')
kOSAGenericScriptingComponentSubtype = FOUR_CHAR_CODE('scpt')
kOSAFileType = FOUR_CHAR_CODE('osas')
kOSASuite = FOUR_CHAR_CODE('ascr')
kOSARecordedText = FOUR_CHAR_CODE('recd')
kOSAScriptIsModified = FOUR_CHAR_CODE('modi')
kOSAScriptIsTypeCompiledScript = FOUR_CHAR_CODE('cscr')
kOSAScriptIsTypeScriptValue = FOUR_CHAR_CODE('valu')
kOSAScriptIsTypeScriptContext = FOUR_CHAR_CODE('cntx')
kOSAScriptBestType = FOUR_CHAR_CODE('best')
kOSACanGetSource = FOUR_CHAR_CODE('gsrc')
typeOSADialectInfo = FOUR_CHAR_CODE('difo')
keyOSADialectName = FOUR_CHAR_CODE('dnam')
keyOSADialectCode = FOUR_CHAR_CODE('dcod')
keyOSADialectLangCode = FOUR_CHAR_CODE('dlcd')
keyOSADialectScriptCode = FOUR_CHAR_CODE('dscd')
kOSANullScript = 0
kOSANullMode = 0
kOSAModeNull = 0
kOSASupportsCompiling = 0x0002
kOSASupportsGetSource = 0x0004
kOSASupportsAECoercion = 0x0008
kOSASupportsAESending = 0x0010
kOSASupportsRecording = 0x0020
kOSASupportsConvenience = 0x0040
kOSASupportsDialects = 0x0080
kOSASupportsEventHandling = 0x0100
kOSASelectLoad = 0x0001
kOSASelectStore = 0x0002
kOSASelectExecute = 0x0003
kOSASelectDisplay = 0x0004
kOSASelectScriptError = 0x0005
kOSASelectDispose = 0x0006
kOSASelectSetScriptInfo = 0x0007
kOSASelectGetScriptInfo = 0x0008
kOSASelectSetActiveProc = 0x0009
kOSASelectGetActiveProc = 0x000A
kOSASelectScriptingComponentName = 0x0102
kOSASelectCompile = 0x0103
kOSASelectCopyID = 0x0104
kOSASelectCopyScript = 0x0105
kOSASelectGetSource = 0x0201
kOSASelectCoerceFromDesc = 0x0301
kOSASelectCoerceToDesc = 0x0302
kOSASelectSetSendProc = 0x0401
kOSASelectGetSendProc = 0x0402
kOSASelectSetCreateProc = 0x0403
kOSASelectGetCreateProc = 0x0404
kOSASelectSetDefaultTarget = 0x0405
kOSASelectStartRecording = 0x0501
kOSASelectStopRecording = 0x0502
kOSASelectLoadExecute = 0x0601
kOSASelectCompileExecute = 0x0602
kOSASelectDoScript = 0x0603
kOSASelectSetCurrentDialect = 0x0701
kOSASelectGetCurrentDialect = 0x0702
kOSASelectAvailableDialects = 0x0703
kOSASelectGetDialectInfo = 0x0704
kOSASelectAvailableDialectCodeList = 0x0705
kOSASelectSetResumeDispatchProc = 0x0801
kOSASelectGetResumeDispatchProc = 0x0802
kOSASelectExecuteEvent = 0x0803
kOSASelectDoEvent = 0x0804
kOSASelectMakeContext = 0x0805
kOSADebuggerCreateSession = 0x0901
kOSADebuggerGetSessionState = 0x0902
kOSADebuggerSessionStep = 0x0903
kOSADebuggerDisposeSession = 0x0904
kOSADebuggerGetStatementRanges = 0x0905
kOSADebuggerGetBreakpoint = 0x0910
kOSADebuggerSetBreakpoint = 0x0911
kOSADebuggerGetDefaultBreakpoint = 0x0912
kOSADebuggerGetCurrentCallFrame = 0x0906
kOSADebuggerGetCallFrameState = 0x0907
kOSADebuggerGetVariable = 0x0908
kOSADebuggerSetVariable = 0x0909
kOSADebuggerGetPreviousCallFrame = 0x090A
kOSADebuggerDisposeCallFrame = 0x090B
kOSADebuggerCountVariables = 0x090C
kOSASelectComponentSpecificStart = 0x1001
kOSAModePreventGetSource = 0x00000001
kOSAModeNeverInteract = kAENeverInteract
kOSAModeCanInteract = kAECanInteract
kOSAModeAlwaysInteract = kAEAlwaysInteract
kOSAModeDontReconnect = kAEDontReconnect
kOSAModeCantSwitchLayer = 0x00000040
kOSAModeDoRecord = 0x00001000
kOSAModeCompileIntoContext = 0x00000002
kOSAModeAugmentContext = 0x00000004
kOSAModeDisplayForHumans = 0x00000008
kOSAModeDontStoreParent = 0x00010000
kOSAModeDispatchToDirectObject = 0x00020000
kOSAModeDontGetDataForArguments = 0x00040000
kOSAScriptResourceType = kOSAGenericScriptingComponentSubtype
typeOSAGenericStorage = kOSAScriptResourceType
kOSAErrorNumber = keyErrorNumber
kOSAErrorMessage = keyErrorString
kOSAErrorBriefMessage = FOUR_CHAR_CODE('errb')
kOSAErrorApp = FOUR_CHAR_CODE('erap')
kOSAErrorPartialResult = FOUR_CHAR_CODE('ptlr')
kOSAErrorOffendingObject = FOUR_CHAR_CODE('erob')
kOSAErrorExpectedType = FOUR_CHAR_CODE('errt')
kOSAErrorRange = FOUR_CHAR_CODE('erng')
typeOSAErrorRange = FOUR_CHAR_CODE('erng')
keyOSASourceStart = FOUR_CHAR_CODE('srcs')
keyOSASourceEnd = FOUR_CHAR_CODE('srce')
kOSAUseStandardDispatch = kAEUseStandardDispatch
kOSANoDispatch = kAENoDispatch
kOSADontUsePhac = 0x0001
eNotStarted = 0
eRunnable = 1
eRunning = 2
eStopped = 3
eTerminated = 4
eStepOver = 0
eStepIn = 1
eStepOut = 2
eRun = 3
eLocal = 0
eGlobal = 1
eProperties = 2
keyProgramState = FOUR_CHAR_CODE('dsps')
typeStatementRange = FOUR_CHAR_CODE('srng')
keyProcedureName = FOUR_CHAR_CODE('dfnm')
keyStatementRange = FOUR_CHAR_CODE('dfsr')
keyLocalsNames = FOUR_CHAR_CODE('dfln')
keyGlobalsNames = FOUR_CHAR_CODE('dfgn')
keyParamsNames = FOUR_CHAR_CODE('dfpn')
