# Generated by h2py from /boot/develop/headers/be/net/socket.h

# Included from BeBuild.h
B_BEOS_VERSION_4 = 0x0400
B_BEOS_VERSION_4_5 = 0x0450
B_BEOS_VERSION_5 = 0x0500
B_BEOS_VERSION = B_BEOS_VERSION_5
B_BEOS_VERSION_MAUI = B_BEOS_VERSION_5
_PR2_COMPATIBLE_ = 1
_PR3_COMPATIBLE_ = 1
_R4_COMPATIBLE_ = 1
_R4_5_COMPATIBLE_ = 1
_PR2_COMPATIBLE_ = 0
_PR3_COMPATIBLE_ = 0
_R4_COMPATIBLE_ = 1
_R4_5_COMPATIBLE_ = 1
def _UNUSED(x): return x


# Included from sys/types.h

# Included from time.h

# Included from be_setup.h
def __std(ref): return ref

__be_os = 2
__dest_os = __be_os
__MSL__ = 0x4011
__GLIBC__ = -2
__GLIBC_MINOR__ = 1

# Included from null.h
NULL = (0)
NULL = 0L

# Included from size_t.h

# Included from stddef.h

# Included from wchar_t.h
CLOCKS_PER_SEC = 1000
CLK_TCK = CLOCKS_PER_SEC
MAX_TIMESTR = 70

# Included from sys/time.h

# Included from ByteOrder.h

# Included from endian.h
__LITTLE_ENDIAN = 1234
LITTLE_ENDIAN = __LITTLE_ENDIAN
__BYTE_ORDER = __LITTLE_ENDIAN
BYTE_ORDER = __BYTE_ORDER
__BIG_ENDIAN = 0
BIG_ENDIAN = 0
__BIG_ENDIAN = 4321
BIG_ENDIAN = __BIG_ENDIAN
__BYTE_ORDER = __BIG_ENDIAN
BYTE_ORDER = __BYTE_ORDER
__LITTLE_ENDIAN = 0
LITTLE_ENDIAN = 0
__PDP_ENDIAN = 3412
PDP_ENDIAN = __PDP_ENDIAN

# Included from SupportDefs.h

# Included from Errors.h

# Included from limits.h

# Included from float.h
FLT_ROUNDS = 1
FLT_RADIX = 2
FLT_MANT_DIG = 24
FLT_DIG = 6
FLT_MIN_EXP = (-125)
FLT_MIN_10_EXP = (-37)
FLT_MAX_EXP = 128
FLT_MAX_10_EXP = 38
DBL_MANT_DIG = 53
DBL_DIG = 15
DBL_MIN_EXP = (-1021)
DBL_MIN_10_EXP = (-308)
DBL_MAX_EXP = 1024
DBL_MAX_10_EXP = 308
LDBL_MANT_DIG = DBL_MANT_DIG
LDBL_DIG = DBL_DIG
LDBL_MIN_EXP = DBL_MIN_EXP
LDBL_MIN_10_EXP = DBL_MIN_10_EXP
LDBL_MAX_EXP = DBL_MAX_EXP
LDBL_MAX_10_EXP = DBL_MAX_10_EXP
CHAR_BIT = (8)
SCHAR_MIN = (-127-1)
SCHAR_MAX = (127)
CHAR_MIN = SCHAR_MIN
CHAR_MAX = SCHAR_MAX
MB_LEN_MAX = (1)
SHRT_MIN = (-32767-1)
SHRT_MAX = (32767)
LONG_MIN = (-2147483647L-1)
LONG_MAX = (2147483647L)
INT_MIN = LONG_MIN
INT_MAX = LONG_MAX
ARG_MAX = (32768)
ATEXIT_MAX = (32)
CHILD_MAX = (1024)
IOV_MAX = (256)
FILESIZEBITS = (64)
LINK_MAX = (1)
LOGIN_NAME_MAX = (32)
MAX_CANON = (255)
MAX_INPUT = (255)
NAME_MAX = (256)
NGROUPS_MAX = (32)
OPEN_MAX = (128)
PATH_MAX = (1024)
PIPE_MAX = (512)
SSIZE_MAX = (2147483647L)
TTY_NAME_MAX = (256)
TZNAME_MAX = (32)
SYMLINKS_MAX = (16)
_POSIX_ARG_MAX = (32768)
_POSIX_CHILD_MAX = (1024)
_POSIX_LINK_MAX = (1)
_POSIX_LOGIN_NAME_MAX = (9)
_POSIX_MAX_CANON = (255)
_POSIX_MAX_INPUT = (255)
_POSIX_NAME_MAX = (255)
_POSIX_NGROUPS_MAX = (0)
_POSIX_OPEN_MAX = (128)
_POSIX_PATH_MAX = (1024)
_POSIX_PIPE_BUF = (512)
_POSIX_SSIZE_MAX = (2147483647L)
_POSIX_STREAM_MAX = (8)
_POSIX_TTY_NAME_MAX = (256)
_POSIX_TZNAME_MAX = (3)
B_GENERAL_ERROR_BASE = LONG_MIN
B_OS_ERROR_BASE = B_GENERAL_ERROR_BASE + 0x1000
B_APP_ERROR_BASE = B_GENERAL_ERROR_BASE + 0x2000
B_INTERFACE_ERROR_BASE = B_GENERAL_ERROR_BASE + 0x3000
B_MEDIA_ERROR_BASE = B_GENERAL_ERROR_BASE + 0x4000
B_TRANSLATION_ERROR_BASE = B_GENERAL_ERROR_BASE + 0x4800
B_MIDI_ERROR_BASE = B_GENERAL_ERROR_BASE + 0x5000
B_STORAGE_ERROR_BASE = B_GENERAL_ERROR_BASE + 0x6000
B_POSIX_ERROR_BASE = B_GENERAL_ERROR_BASE + 0x7000
B_MAIL_ERROR_BASE = B_GENERAL_ERROR_BASE + 0x8000
B_PRINT_ERROR_BASE = B_GENERAL_ERROR_BASE + 0x9000
B_DEVICE_ERROR_BASE = B_GENERAL_ERROR_BASE + 0xa000
B_ERRORS_END = (B_GENERAL_ERROR_BASE + 0xffff)
E2BIG = (B_POSIX_ERROR_BASE + 1)
ECHILD = (B_POSIX_ERROR_BASE + 2)
EDEADLK = (B_POSIX_ERROR_BASE + 3)
EFBIG = (B_POSIX_ERROR_BASE + 4)
EMLINK = (B_POSIX_ERROR_BASE + 5)
ENFILE = (B_POSIX_ERROR_BASE + 6)
ENODEV = (B_POSIX_ERROR_BASE + 7)
ENOLCK = (B_POSIX_ERROR_BASE + 8)
ENOSYS = (B_POSIX_ERROR_BASE + 9)
ENOTTY = (B_POSIX_ERROR_BASE + 10)
ENXIO = (B_POSIX_ERROR_BASE + 11)
ESPIPE = (B_POSIX_ERROR_BASE + 12)
ESRCH = (B_POSIX_ERROR_BASE + 13)
EFPOS = (B_POSIX_ERROR_BASE + 14)
ESIGPARM = (B_POSIX_ERROR_BASE + 15)
EDOM = (B_POSIX_ERROR_BASE + 16)
ERANGE = (B_POSIX_ERROR_BASE + 17)
EPROTOTYPE = (B_POSIX_ERROR_BASE + 18)
EPROTONOSUPPORT = (B_POSIX_ERROR_BASE + 19)
EPFNOSUPPORT = (B_POSIX_ERROR_BASE + 20)
EAFNOSUPPORT = (B_POSIX_ERROR_BASE + 21)
EADDRINUSE = (B_POSIX_ERROR_BASE + 22)
EADDRNOTAVAIL = (B_POSIX_ERROR_BASE + 23)
ENETDOWN = (B_POSIX_ERROR_BASE + 24)
ENETUNREACH = (B_POSIX_ERROR_BASE + 25)
ENETRESET = (B_POSIX_ERROR_BASE + 26)
ECONNABORTED = (B_POSIX_ERROR_BASE + 27)
ECONNRESET = (B_POSIX_ERROR_BASE + 28)
EISCONN = (B_POSIX_ERROR_BASE + 29)
ENOTCONN = (B_POSIX_ERROR_BASE + 30)
ESHUTDOWN = (B_POSIX_ERROR_BASE + 31)
ECONNREFUSED = (B_POSIX_ERROR_BASE + 32)
EHOSTUNREACH = (B_POSIX_ERROR_BASE + 33)
ENOPROTOOPT = (B_POSIX_ERROR_BASE + 34)
ENOBUFS = (B_POSIX_ERROR_BASE + 35)
EINPROGRESS = (B_POSIX_ERROR_BASE + 36)
EALREADY = (B_POSIX_ERROR_BASE + 37)
EILSEQ = (B_POSIX_ERROR_BASE + 38)
ENOMSG = (B_POSIX_ERROR_BASE + 39)
ESTALE = (B_POSIX_ERROR_BASE + 40)
EOVERFLOW = (B_POSIX_ERROR_BASE + 41)
EMSGSIZE = (B_POSIX_ERROR_BASE + 42)
EOPNOTSUPP = (B_POSIX_ERROR_BASE + 43)
ENOTSOCK = (B_POSIX_ERROR_BASE + 44)
false = 0
true = 1
NULL = (0)
FALSE = 0
TRUE = 1

# Included from TypeConstants.h
B_HOST_IS_LENDIAN = 1
B_HOST_IS_BENDIAN = 0
def B_HOST_TO_LENDIAN_DOUBLE(arg): return (double)(arg)

def B_HOST_TO_LENDIAN_FLOAT(arg): return (float)(arg)

def B_HOST_TO_LENDIAN_INT64(arg): return (uint64)(arg)

def B_HOST_TO_LENDIAN_INT32(arg): return (uint32)(arg)

def B_HOST_TO_LENDIAN_INT16(arg): return (uint16)(arg)

def B_HOST_TO_BENDIAN_DOUBLE(arg): return __swap_double(arg)

def B_HOST_TO_BENDIAN_FLOAT(arg): return __swap_float(arg)

def B_HOST_TO_BENDIAN_INT64(arg): return __swap_int64(arg)

def B_HOST_TO_BENDIAN_INT32(arg): return __swap_int32(arg)

def B_HOST_TO_BENDIAN_INT16(arg): return __swap_int16(arg)

def B_LENDIAN_TO_HOST_DOUBLE(arg): return (double)(arg)

def B_LENDIAN_TO_HOST_FLOAT(arg): return (float)(arg)

def B_LENDIAN_TO_HOST_INT64(arg): return (uint64)(arg)

def B_LENDIAN_TO_HOST_INT32(arg): return (uint32)(arg)

def B_LENDIAN_TO_HOST_INT16(arg): return (uint16)(arg)

def B_BENDIAN_TO_HOST_DOUBLE(arg): return __swap_double(arg)

def B_BENDIAN_TO_HOST_FLOAT(arg): return __swap_float(arg)

def B_BENDIAN_TO_HOST_INT64(arg): return __swap_int64(arg)

def B_BENDIAN_TO_HOST_INT32(arg): return __swap_int32(arg)

def B_BENDIAN_TO_HOST_INT16(arg): return __swap_int16(arg)

B_HOST_IS_LENDIAN = 0
B_HOST_IS_BENDIAN = 1
def B_HOST_TO_LENDIAN_DOUBLE(arg): return __swap_double(arg)

def B_HOST_TO_LENDIAN_FLOAT(arg): return __swap_float(arg)

def B_HOST_TO_LENDIAN_INT64(arg): return __swap_int64(arg)

def B_HOST_TO_LENDIAN_INT32(arg): return __swap_int32(arg)

def B_HOST_TO_LENDIAN_INT16(arg): return __swap_int16(arg)

def B_HOST_TO_BENDIAN_DOUBLE(arg): return (double)(arg)

def B_HOST_TO_BENDIAN_FLOAT(arg): return (float)(arg)

def B_HOST_TO_BENDIAN_INT64(arg): return (uint64)(arg)

def B_HOST_TO_BENDIAN_INT32(arg): return (uint32)(arg)

def B_HOST_TO_BENDIAN_INT16(arg): return (uint16)(arg)

def B_LENDIAN_TO_HOST_DOUBLE(arg): return __swap_double(arg)

def B_LENDIAN_TO_HOST_FLOAT(arg): return __swap_float(arg)

def B_LENDIAN_TO_HOST_INT64(arg): return __swap_int64(arg)

def B_LENDIAN_TO_HOST_INT32(arg): return __swap_int32(arg)

def B_LENDIAN_TO_HOST_INT16(arg): return __swap_int16(arg)

def B_BENDIAN_TO_HOST_DOUBLE(arg): return (double)(arg)

def B_BENDIAN_TO_HOST_FLOAT(arg): return (float)(arg)

def B_BENDIAN_TO_HOST_INT64(arg): return (uint64)(arg)

def B_BENDIAN_TO_HOST_INT32(arg): return (uint32)(arg)

def B_BENDIAN_TO_HOST_INT16(arg): return (uint16)(arg)

def B_SWAP_DOUBLE(arg): return __swap_double(arg)

def B_SWAP_FLOAT(arg): return __swap_float(arg)

def B_SWAP_INT64(arg): return __swap_int64(arg)

def B_SWAP_INT32(arg): return __swap_int32(arg)

def B_SWAP_INT16(arg): return __swap_int16(arg)

def htonl(x): return B_HOST_TO_BENDIAN_INT32(x)

def ntohl(x): return B_BENDIAN_TO_HOST_INT32(x)

def htons(x): return B_HOST_TO_BENDIAN_INT16(x)

def ntohs(x): return B_BENDIAN_TO_HOST_INT16(x)

AF_INET = 1
INADDR_ANY = 0x00000000
INADDR_BROADCAST = 0xffffffff
INADDR_LOOPBACK = 0x7f000001
SOL_SOCKET = 1
SO_DEBUG = 1
SO_REUSEADDR = 2
SO_NONBLOCK = 3
SO_REUSEPORT = 4
MSG_OOB = 0x1
SOCK_DGRAM = 1
SOCK_STREAM = 2
IPPROTO_UDP = 1
IPPROTO_TCP = 2
IPPROTO_ICMP = 3
B_UDP_MAX_SIZE = (65536 - 1024)
FD_SETSIZE = 256
FDSETSIZE = FD_SETSIZE
NFDBITS = 32
def _FDMSKNO(fd): return ((fd) / NFDBITS)

def _FDBITNO(fd): return ((fd) % NFDBITS)
