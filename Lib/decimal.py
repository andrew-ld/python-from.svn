# Copyright (c) 2004 Python Software Foundation.
# All rights reserved.

# Written by Eric Price <eprice at tjhsst.edu>
#    and Facundo Batista <facundo at taniquetil.com.ar>
#    and Raymond Hettinger <python at rcn.com>
#    and Aahz <aahz at pobox.com>
#    and Tim Peters

# This module is currently Py2.3 compatible and should be kept that way
# unless a major compelling advantage arises.  IOW, 2.3 compatibility is
# strongly preferred, but not guaranteed.

# Also, this module should be kept in sync with the latest updates of
# the IBM specification as it evolves.  Those updates will be treated
# as bug fixes (deviation from the spec is a compatibility, usability
# bug) and will be backported.  At this point the spec is stabilizing
# and the updates are becoming fewer, smaller, and less significant.

"""
This is a Py2.3 implementation of decimal floating point arithmetic based on
the General Decimal Arithmetic Specification:

    www2.hursley.ibm.com/decimal/decarith.html

and IEEE standard 854-1987:

    www.cs.berkeley.edu/~ejr/projects/754/private/drafts/854-1987/dir.html

Decimal floating point has finite precision with arbitrarily large bounds.

The purpose of this module is to support arithmetic using familiar
"schoolhouse" rules and to avoid some of the tricky representation
issues associated with binary floating point.  The package is especially
useful for financial applications or for contexts where users have
expectations that are at odds with binary floating point (for instance,
in binary floating point, 1.00 % 0.1 gives 0.09999999999999995 instead
of the expected Decimal("0.00") returned by decimal floating point).

Here are some examples of using the decimal module:

>>> from decimal import *
>>> setcontext(ExtendedContext)
>>> Decimal(0)
Decimal("0")
>>> Decimal("1")
Decimal("1")
>>> Decimal("-.0123")
Decimal("-0.0123")
>>> Decimal(123456)
Decimal("123456")
>>> Decimal("123.45e12345678901234567890")
Decimal("1.2345E+12345678901234567892")
>>> Decimal("1.33") + Decimal("1.27")
Decimal("2.60")
>>> Decimal("12.34") + Decimal("3.87") - Decimal("18.41")
Decimal("-2.20")
>>> dig = Decimal(1)
>>> print dig / Decimal(3)
0.333333333
>>> getcontext().prec = 18
>>> print dig / Decimal(3)
0.333333333333333333
>>> print dig.sqrt()
1
>>> print Decimal(3).sqrt()
1.73205080756887729
>>> print Decimal(3) ** 123
4.85192780976896427E+58
>>> inf = Decimal(1) / Decimal(0)
>>> print inf
Infinity
>>> neginf = Decimal(-1) / Decimal(0)
>>> print neginf
-Infinity
>>> print neginf + inf
NaN
>>> print neginf * inf
-Infinity
>>> print dig / 0
Infinity
>>> getcontext().traps[DivisionByZero] = 1
>>> print dig / 0
Traceback (most recent call last):
  ...
  ...
  ...
DivisionByZero: x / 0
>>> c = Context()
>>> c.traps[InvalidOperation] = 0
>>> print c.flags[InvalidOperation]
0
>>> c.divide(Decimal(0), Decimal(0))
Decimal("NaN")
>>> c.traps[InvalidOperation] = 1
>>> print c.flags[InvalidOperation]
1
>>> c.flags[InvalidOperation] = 0
>>> print c.flags[InvalidOperation]
0
>>> print c.divide(Decimal(0), Decimal(0))
Traceback (most recent call last):
  ...
  ...
  ...
InvalidOperation: 0 / 0
>>> print c.flags[InvalidOperation]
1
>>> c.flags[InvalidOperation] = 0
>>> c.traps[InvalidOperation] = 0
>>> print c.divide(Decimal(0), Decimal(0))
NaN
>>> print c.flags[InvalidOperation]
1
>>>
"""

__all__ = [
    # Two major classes
    'Decimal', 'Context',

    # Contexts
    'DefaultContext', 'BasicContext', 'ExtendedContext',

    # Exceptions
    'DecimalException', 'Clamped', 'InvalidOperation', 'DivisionByZero',
    'Inexact', 'Rounded', 'Subnormal', 'Overflow', 'Underflow',

    # Constants for use in setting up contexts
    'ROUND_DOWN', 'ROUND_HALF_UP', 'ROUND_HALF_EVEN', 'ROUND_CEILING',
    'ROUND_FLOOR', 'ROUND_UP', 'ROUND_HALF_DOWN',

    # Functions for manipulating contexts
    'setcontext', 'getcontext', 'localcontext'
]

import copy as _copy

# Rounding
ROUND_DOWN = 'ROUND_DOWN'
ROUND_HALF_UP = 'ROUND_HALF_UP'
ROUND_HALF_EVEN = 'ROUND_HALF_EVEN'
ROUND_CEILING = 'ROUND_CEILING'
ROUND_FLOOR = 'ROUND_FLOOR'
ROUND_UP = 'ROUND_UP'
ROUND_HALF_DOWN = 'ROUND_HALF_DOWN'

# Rounding decision (not part of the public API)
NEVER_ROUND = 'NEVER_ROUND'    # Round in division (non-divmod), sqrt ONLY
ALWAYS_ROUND = 'ALWAYS_ROUND'  # Every operation rounds at end.

# Errors

class DecimalException(ArithmeticError):
    """Base exception class.

    Used exceptions derive from this.
    If an exception derives from another exception besides this (such as
    Underflow (Inexact, Rounded, Subnormal) that indicates that it is only
    called if the others are present.  This isn't actually used for
    anything, though.

    handle  -- Called when context._raise_error is called and the
               trap_enabler is set.  First argument is self, second is the
               context.  More arguments can be given, those being after
               the explanation in _raise_error (For example,
               context._raise_error(NewError, '(-x)!', self._sign) would
               call NewError().handle(context, self._sign).)

    To define a new exception, it should be sufficient to have it derive
    from DecimalException.
    """
    def handle(self, context, *args):
        pass


class Clamped(DecimalException):
    """Exponent of a 0 changed to fit bounds.

    This occurs and signals clamped if the exponent of a result has been
    altered in order to fit the constraints of a specific concrete
    representation.  This may occur when the exponent of a zero result would
    be outside the bounds of a representation, or when a large normal
    number would have an encoded exponent that cannot be represented.  In
    this latter case, the exponent is reduced to fit and the corresponding
    number of zero digits are appended to the coefficient ("fold-down").
    """


class InvalidOperation(DecimalException):
    """An invalid operation was performed.

    Various bad things cause this:

    Something creates a signaling NaN
    -INF + INF
    0 * (+-)INF
    (+-)INF / (+-)INF
    x % 0
    (+-)INF % x
    x._rescale( non-integer )
    sqrt(-x) , x > 0
    0 ** 0
    x ** (non-integer)
    x ** (+-)INF
    An operand is invalid

    The result of the operation after these is a quiet positive NaN,
    except when the cause is a signaling NaN, in which case the result is
    also a quiet NaN, but with the original sign, and an optional
    diagnostic information.
    """
    def handle(self, context, *args):
        if args:
            if args[0] == 1:  # sNaN, must drop 's' but keep diagnostics
                return Decimal( (args[1]._sign, args[1]._int, 'n') )
            elif args[0] == 2:
                return Decimal( (args[1], args[2], 'P') )
        return NaN


class ConversionSyntax(InvalidOperation):
    """Trying to convert badly formed string.

    This occurs and signals invalid-operation if an string is being
    converted to a number and it does not conform to the numeric string
    syntax.  The result is [0,qNaN].
    """
    def handle(self, context, *args):
        return NaN

class DivisionByZero(DecimalException, ZeroDivisionError):
    """Division by 0.

    This occurs and signals division-by-zero if division of a finite number
    by zero was attempted (during a divide-integer or divide operation, or a
    power operation with negative right-hand operand), and the dividend was
    not zero.

    The result of the operation is [sign,inf], where sign is the exclusive
    or of the signs of the operands for divide, or is 1 for an odd power of
    -0, for power.
    """

    def handle(self, context, sign, double = None, *args):
        if double is not None:
            return (Infsign[sign],)*2
        return Infsign[sign]

class DivisionImpossible(InvalidOperation):
    """Cannot perform the division adequately.

    This occurs and signals invalid-operation if the integer result of a
    divide-integer or remainder operation had too many digits (would be
    longer than precision).  The result is [0,qNaN].
    """

    def handle(self, context, *args):
        return (NaN, NaN)

class DivisionUndefined(InvalidOperation, ZeroDivisionError):
    """Undefined result of division.

    This occurs and signals invalid-operation if division by zero was
    attempted (during a divide-integer, divide, or remainder operation), and
    the dividend is also zero.  The result is [0,qNaN].
    """

    def handle(self, context, tup=None, *args):
        if tup is not None:
            return (NaN, NaN)  # for 0 %0, 0 // 0
        return NaN

class Inexact(DecimalException):
    """Had to round, losing information.

    This occurs and signals inexact whenever the result of an operation is
    not exact (that is, it needed to be rounded and any discarded digits
    were non-zero), or if an overflow or underflow condition occurs.  The
    result in all cases is unchanged.

    The inexact signal may be tested (or trapped) to determine if a given
    operation (or sequence of operations) was inexact.
    """
    pass

class InvalidContext(InvalidOperation):
    """Invalid context.  Unknown rounding, for example.

    This occurs and signals invalid-operation if an invalid context was
    detected during an operation.  This can occur if contexts are not checked
    on creation and either the precision exceeds the capability of the
    underlying concrete representation or an unknown or unsupported rounding
    was specified.  These aspects of the context need only be checked when
    the values are required to be used.  The result is [0,qNaN].
    """

    def handle(self, context, *args):
        return NaN

class Rounded(DecimalException):
    """Number got rounded (not  necessarily changed during rounding).

    This occurs and signals rounded whenever the result of an operation is
    rounded (that is, some zero or non-zero digits were discarded from the
    coefficient), or if an overflow or underflow condition occurs.  The
    result in all cases is unchanged.

    The rounded signal may be tested (or trapped) to determine if a given
    operation (or sequence of operations) caused a loss of precision.
    """
    pass

class Subnormal(DecimalException):
    """Exponent < Emin before rounding.

    This occurs and signals subnormal whenever the result of a conversion or
    operation is subnormal (that is, its adjusted exponent is less than
    Emin, before any rounding).  The result in all cases is unchanged.

    The subnormal signal may be tested (or trapped) to determine if a given
    or operation (or sequence of operations) yielded a subnormal result.
    """
    pass

class Overflow(Inexact, Rounded):
    """Numerical overflow.

    This occurs and signals overflow if the adjusted exponent of a result
    (from a conversion or from an operation that is not an attempt to divide
    by zero), after rounding, would be greater than the largest value that
    can be handled by the implementation (the value Emax).

    The result depends on the rounding mode:

    For round-half-up and round-half-even (and for round-half-down and
    round-up, if implemented), the result of the operation is [sign,inf],
    where sign is the sign of the intermediate result.  For round-down, the
    result is the largest finite number that can be represented in the
    current precision, with the sign of the intermediate result.  For
    round-ceiling, the result is the same as for round-down if the sign of
    the intermediate result is 1, or is [0,inf] otherwise.  For round-floor,
    the result is the same as for round-down if the sign of the intermediate
    result is 0, or is [1,inf] otherwise.  In all cases, Inexact and Rounded
    will also be raised.
   """

    def handle(self, context, sign, *args):
        if context.rounding in (ROUND_HALF_UP, ROUND_HALF_EVEN,
                                     ROUND_HALF_DOWN, ROUND_UP):
            return Infsign[sign]
        if sign == 0:
            if context.rounding == ROUND_CEILING:
                return Infsign[sign]
            return Decimal((sign, (9,)*context.prec,
                            context.Emax-context.prec+1))
        if sign == 1:
            if context.rounding == ROUND_FLOOR:
                return Infsign[sign]
            return Decimal( (sign, (9,)*context.prec,
                             context.Emax-context.prec+1))


class Underflow(Inexact, Rounded, Subnormal):
    """Numerical underflow with result rounded to 0.

    This occurs and signals underflow if a result is inexact and the
    adjusted exponent of the result would be smaller (more negative) than
    the smallest value that can be handled by the implementation (the value
    Emin).  That is, the result is both inexact and subnormal.

    The result after an underflow will be a subnormal number rounded, if
    necessary, so that its exponent is not less than Etiny.  This may result
    in 0 with the sign of the intermediate result and an exponent of Etiny.

    In all cases, Inexact, Rounded, and Subnormal will also be raised.
    """

# List of public traps and flags
_signals = [Clamped, DivisionByZero, Inexact, Overflow, Rounded,
           Underflow, InvalidOperation, Subnormal]

# Map conditions (per the spec) to signals
_condition_map = {ConversionSyntax:InvalidOperation,
                  DivisionImpossible:InvalidOperation,
                  DivisionUndefined:InvalidOperation,
                  InvalidContext:InvalidOperation}

##### Context Functions ##################################################

# The getcontext() and setcontext() function manage access to a thread-local
# current context.  Py2.4 offers direct support for thread locals.  If that
# is not available, use threading.currentThread() which is slower but will
# work for older Pythons.  If threads are not part of the build, create a
# mock threading object with threading.local() returning the module namespace.

try:
    import threading
except ImportError:
    # Python was compiled without threads; create a mock object instead
    import sys
    class MockThreading(object):
        def local(self, sys=sys):
            return sys.modules[__name__]
    threading = MockThreading()
    del sys, MockThreading

try:
    threading.local

except AttributeError:

    # To fix reloading, force it to create a new context
    # Old contexts have different exceptions in their dicts, making problems.
    if hasattr(threading.currentThread(), '__decimal_context__'):
        del threading.currentThread().__decimal_context__

    def setcontext(context):
        """Set this thread's context to context."""
        if context in (DefaultContext, BasicContext, ExtendedContext):
            context = context.copy()
            context.clear_flags()
        threading.currentThread().__decimal_context__ = context

    def getcontext():
        """Returns this thread's context.

        If this thread does not yet have a context, returns
        a new context and sets this thread's context.
        New contexts are copies of DefaultContext.
        """
        try:
            return threading.currentThread().__decimal_context__
        except AttributeError:
            context = Context()
            threading.currentThread().__decimal_context__ = context
            return context

else:

    local = threading.local()
    if hasattr(local, '__decimal_context__'):
        del local.__decimal_context__

    def getcontext(_local=local):
        """Returns this thread's context.

        If this thread does not yet have a context, returns
        a new context and sets this thread's context.
        New contexts are copies of DefaultContext.
        """
        try:
            return _local.__decimal_context__
        except AttributeError:
            context = Context()
            _local.__decimal_context__ = context
            return context

    def setcontext(context, _local=local):
        """Set this thread's context to context."""
        if context in (DefaultContext, BasicContext, ExtendedContext):
            context = context.copy()
            context.clear_flags()
        _local.__decimal_context__ = context

    del threading, local        # Don't contaminate the namespace

def localcontext(ctx=None):
    """Return a context manager for a copy of the supplied context

    Uses a copy of the current context if no context is specified
    The returned context manager creates a local decimal context
    in a with statement:
        def sin(x):
             with localcontext() as ctx:
                 ctx.prec += 2
                 # Rest of sin calculation algorithm
                 # uses a precision 2 greater than normal
             return +s  # Convert result to normal precision

         def sin(x):
             with localcontext(ExtendedContext):
                 # Rest of sin calculation algorithm
                 # uses the Extended Context from the
                 # General Decimal Arithmetic Specification
             return +s  # Convert result to normal context

    """
    # The string below can't be included in the docstring until Python 2.6
    # as the doctest module doesn't understand __future__ statements
    """
    >>> from __future__ import with_statement
    >>> print getcontext().prec
    28
    >>> with localcontext():
    ...     ctx = getcontext()
    ...     ctx.prec += 2
    ...     print ctx.prec
    ...
    30
    >>> with localcontext(ExtendedContext):
    ...     print getcontext().prec
    ...
    9
    >>> print getcontext().prec
    28
    """
    if ctx is None: ctx = getcontext()
    return _ContextManager(ctx)


##### Decimal class #######################################################

class Decimal(object):
    """Floating point class for decimal arithmetic."""

    __slots__ = ('_exp','_int','_sign', '_is_special')
    # Generally, the value of the Decimal instance is given by
    #  (-1)**_sign * _int * 10**_exp
    # Special values are signified by _is_special == True

    # We're immutable, so use __new__ not __init__
    def __new__(cls, value="0", context=None):
        """Create a decimal point instance.

        >>> Decimal('3.14')              # string input
        Decimal("3.14")
        >>> Decimal((0, (3, 1, 4), -2))  # tuple (sign, digit_tuple, exponent)
        Decimal("3.14")
        >>> Decimal(314)                 # int or long
        Decimal("314")
        >>> Decimal(Decimal(314))        # another decimal instance
        Decimal("314")
        """

        self = object.__new__(cls)
        self._is_special = False

        # From an internal working value
        if isinstance(value, _WorkRep):
            self._sign = value.sign
            self._int = tuple(map(int, str(value.int)))
            self._exp = int(value.exp)
            return self

        # From another decimal
        if isinstance(value, Decimal):
            self._exp  = value._exp
            self._sign = value._sign
            self._int  = value._int
            self._is_special  = value._is_special
            return self

        # From an integer
        if isinstance(value, (int,long)):
            if value >= 0:
                self._sign = 0
            else:
                self._sign = 1
            self._exp = 0
            self._int = tuple(map(int, str(abs(value))))
            return self

        # tuple/list conversion (possibly from as_tuple())
        if isinstance(value, (list,tuple)):
            if len(value) != 3:
                raise ValueError('Invalid arguments')
            if value[0] not in (0,1):
                raise ValueError('Invalid sign')
            for digit in value[1]:
                if not isinstance(digit, (int,long)) or digit < 0:
                    raise ValueError("The second value in the tuple must be "
                                "composed of non negative integer elements.")
            self._sign = value[0]
            self._int  = tuple(value[1])
            if value[2] in ('F','n','N', 'P'):
                self._exp = value[2]
                self._is_special = True
            else:
                self._exp  = int(value[2])
            return self

        if isinstance(value, float):
            raise TypeError("Cannot convert float to Decimal.  " +
                            "First convert the float to a string")

        # Other argument types may require the context during interpretation
        if context is None:
            context = getcontext()

        # From a string
        # REs insist on real strings, so we can too.
        if isinstance(value, basestring):
            if _isinfinity(value):
                self._exp = 'F'
                self._int = (0,)
                self._is_special = True
                if _isinfinity(value) == 1:
                    self._sign = 0
                else:
                    self._sign = 1
                return self
            if _isnan(value):
                sig, sign, diag = _isnan(value)
                self._is_special = True
                if len(diag) > context.prec:  # Diagnostic info too long
                    # sig=1, qNaN -> ConversionSyntax
                    # sig=2, sNaN -> InvalidOperation
                    digits = tuple(int(x) for x in diag[-context.prec:])
                    if sig == 1:
                        self._exp = 'P'  # qNaN
                        self._sign = sign
                        self._int = digits
                        return self

                    return context._raise_error(InvalidOperation,
                                                'diagnostic info too long',
                                                2, sign, digits)
                if sig == 1:
                    self._exp = 'n'  # qNaN
                else:  # sig == 2
                    self._exp = 'N'  # sNaN
                self._sign = sign
                self._int = tuple(map(int, diag))  # Diagnostic info
                return self
            try:
                self._sign, self._int, self._exp = _string2exact(value)
            except ValueError:
                self._is_special = True
                return context._raise_error(ConversionSyntax,
                                                "non parseable string")
            return self

        raise TypeError("Cannot convert %r to Decimal" % value)

    def _isnan(self):
        """Returns whether the number is not actually one.

        0 if a number
        1 if NaN  (it could be a normal quiet NaN or a phantom one)
        2 if sNaN
        """
        if self._is_special:
            exp = self._exp
            if exp == 'n' or exp == 'P':
                return 1
            elif exp == 'N':
                return 2
        return 0

    def _isinfinity(self):
        """Returns whether the number is infinite

        0 if finite or not a number
        1 if +INF
        -1 if -INF
        """
        if self._exp == 'F':
            if self._sign:
                return -1
            return 1
        return 0

    def _check_nans(self, other=None, context=None):
        """Returns whether the number is not actually one.

        if self, other are sNaN, signal
        if self, other are NaN return nan
        return 0

        Done before operations.
        """

        self_is_nan = self._isnan()
        if other is None:
            other_is_nan = False
        else:
            other_is_nan = other._isnan()

        if self_is_nan or other_is_nan:
            if context is None:
                context = getcontext()

            if self_is_nan == 2:
                return context._raise_error(InvalidOperation, 'sNaN',
                                        1, self)
            if other_is_nan == 2:
                return context._raise_error(InvalidOperation, 'sNaN',
                                        1, other)
            if self_is_nan:
                return self

            return other
        return 0

    def __nonzero__(self):
        """Is the number non-zero?

        0 if self == 0
        1 if self != 0
        """
        if self._is_special:
            return 1
        return sum(self._int) != 0

    def __cmp__(self, other, context=None):
        other = _convert_other(other)
        if other is NotImplemented:
            # Never return NotImplemented
            return 1

        if self._is_special or other._is_special:
            ans = self._check_nans(other, context)
            if ans:
                return 1  # Comparison involving NaN's always reports self > other

            # INF = INF
            return cmp(self._isinfinity(), other._isinfinity())

        if not self and not other:
            return 0  # If both 0, sign comparison isn't certain.

        # If different signs, neg one is less
        if other._sign < self._sign:
            return -1
        if self._sign < other._sign:
            return 1

        self_adjusted = self.adjusted()
        other_adjusted = other.adjusted()
        if self_adjusted == other_adjusted and \
           self._int + (0,)*(self._exp - other._exp) == \
           other._int + (0,)*(other._exp - self._exp):
            return 0  # equal, except in precision. ([0]*(-x) = [])
        elif self_adjusted > other_adjusted and self._int[0] != 0:
            return (-1)**self._sign
        elif self_adjusted < other_adjusted and other._int[0] != 0:
            return -((-1)**self._sign)

        # Need to round, so make sure we have a valid context
        if context is None:
            context = getcontext()

        context = context._shallow_copy()
        rounding = context._set_rounding(ROUND_UP)  # round away from 0

        flags = context._ignore_all_flags()
        res = self.__sub__(other, context=context)

        context._regard_flags(*flags)

        context.rounding = rounding

        if not res:
            return 0
        elif res._sign:
            return -1
        return 1

    def __eq__(self, other):
        if not isinstance(other, (Decimal, int, long)):
            return NotImplemented
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        if not isinstance(other, (Decimal, int, long)):
            return NotImplemented
        return self.__cmp__(other) != 0

    def compare(self, other, context=None):
        """Compares one to another.

        -1 => a < b
        0  => a = b
        1  => a > b
        NaN => one is NaN
        Like __cmp__, but returns Decimal instances.
        """
        other = _convert_other(other)
        if other is NotImplemented:
            return other

        # Compare(NaN, NaN) = NaN
        if (self._is_special or other and other._is_special):
            ans = self._check_nans(other, context)
            if ans:
                return ans

        return Decimal(self.__cmp__(other, context))

    def __hash__(self):
        """x.__hash__() <==> hash(x)"""
        # Decimal integers must hash the same as the ints
        # Non-integer decimals are normalized and hashed as strings
        # Normalization assures that hash(100E-1) == hash(10)
        if self._is_special:
            if self._isnan():
                raise TypeError('Cannot hash a NaN value.')
            return hash(str(self))
        i = int(self)
        if self == Decimal(i):
            return hash(i)
        assert self.__nonzero__()   # '-0' handled by integer case
        return hash(str(self.normalize()))

    def as_tuple(self):
        """Represents the number as a triple tuple.

        To show the internals exactly as they are.
        """
        return (self._sign, self._int, self._exp)

    def __repr__(self):
        """Represents the number as an instance of Decimal."""
        # Invariant:  eval(repr(d)) == d
        return 'Decimal("%s")' % str(self)

    def __str__(self, eng = 0, context=None):
        """Return string representation of the number in scientific notation.

        Captures all of the information in the underlying representation.
        """

        if self._is_special:
            if self._isnan():
                minus = '-'*self._sign
                if self._int == (0,):
                    info = ''
                else:
                    info = ''.join(map(str, self._int))
                if self._isnan() == 2:
                    return minus + 'sNaN' + info
                return minus + 'NaN' + info
            if self._isinfinity():
                minus = '-'*self._sign
                return minus + 'Infinity'

        if context is None:
            context = getcontext()

        tmp = map(str, self._int)
        numdigits = len(self._int)
        leftdigits = self._exp + numdigits
        if eng and not self:  # self = 0eX wants 0[.0[0]]eY, not [[0]0]0eY
            if self._exp < 0 and self._exp >= -6:  # short, no need for e/E
                s = '-'*self._sign + '0.' + '0'*(abs(self._exp))
                return s
            # exp is closest mult. of 3 >= self._exp
            exp = ((self._exp - 1)// 3 + 1) * 3
            if exp != self._exp:
                s = '0.'+'0'*(exp - self._exp)
            else:
                s = '0'
            if exp != 0:
                if context.capitals:
                    s += 'E'
                else:
                    s += 'e'
                if exp > 0:
                    s += '+'  # 0.0e+3, not 0.0e3
                s += str(exp)
            s = '-'*self._sign + s
            return s
        if eng:
            dotplace = (leftdigits-1)%3+1
            adjexp = leftdigits -1 - (leftdigits-1)%3
        else:
            adjexp = leftdigits-1
            dotplace = 1
        if self._exp == 0:
            pass
        elif self._exp < 0 and adjexp >= 0:
            tmp.insert(leftdigits, '.')
        elif self._exp < 0 and adjexp >= -6:
            tmp[0:0] = ['0'] * int(-leftdigits)
            tmp.insert(0, '0.')
        else:
            if numdigits > dotplace:
                tmp.insert(dotplace, '.')
            elif numdigits < dotplace:
                tmp.extend(['0']*(dotplace-numdigits))
            if adjexp:
                if not context.capitals:
                    tmp.append('e')
                else:
                    tmp.append('E')
                    if adjexp > 0:
                        tmp.append('+')
                tmp.append(str(adjexp))
        if eng:
            while tmp[0:1] == ['0']:
                tmp[0:1] = []
            if len(tmp) == 0 or tmp[0] == '.' or tmp[0].lower() == 'e':
                tmp[0:0] = ['0']
        if self._sign:
            tmp.insert(0, '-')

        return ''.join(tmp)

    def to_eng_string(self, context=None):
        """Convert to engineering-type string.

        Engineering notation has an exponent which is a multiple of 3, so there
        are up to 3 digits left of the decimal place.

        Same rules for when in exponential and when as a value as in __str__.
        """
        return self.__str__(eng=1, context=context)

    def __neg__(self, context=None):
        """Returns a copy with the sign switched.

        Rounds, if it has reason.
        """
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans

        if not self:
            # -Decimal('0') is Decimal('0'), not Decimal('-0')
            sign = 0
        elif self._sign:
            sign = 0
        else:
            sign = 1

        if context is None:
            context = getcontext()
        if context._rounding_decision == ALWAYS_ROUND:
            return Decimal((sign, self._int, self._exp))._fix(context)
        return Decimal( (sign, self._int, self._exp))

    def __pos__(self, context=None):
        """Returns a copy, unless it is a sNaN.

        Rounds the number (if more then precision digits)
        """
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans

        sign = self._sign
        if not self:
            # + (-0) = 0
            sign = 0

        if context is None:
            context = getcontext()

        if context._rounding_decision == ALWAYS_ROUND:
            ans = self._fix(context)
        else:
            ans = Decimal(self)
        ans._sign = sign
        return ans

    def __abs__(self, round=1, context=None):
        """Returns the absolute value of self.

        If the second argument is 0, do not round.
        """
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans

        if not round:
            if context is None:
                context = getcontext()
            context = context._shallow_copy()
            context._set_rounding_decision(NEVER_ROUND)

        if self._sign:
            ans = self.__neg__(context=context)
        else:
            ans = self.__pos__(context=context)

        return ans

    def __add__(self, other, context=None):
        """Returns self + other.

        -INF + INF (or the reverse) cause InvalidOperation errors.
        """
        other = _convert_other(other)
        if other is NotImplemented:
            return other

        if context is None:
            context = getcontext()

        if self._is_special or other._is_special:
            ans = self._check_nans(other, context)
            if ans:
                return ans

            if self._isinfinity():
                # If both INF, same sign => same as both, opposite => error.
                if self._sign != other._sign and other._isinfinity():
                    return context._raise_error(InvalidOperation, '-INF + INF')
                return Decimal(self)
            if other._isinfinity():
                return Decimal(other)  # Can't both be infinity here

        shouldround = context._rounding_decision == ALWAYS_ROUND

        exp = min(self._exp, other._exp)
        negativezero = 0
        if context.rounding == ROUND_FLOOR and self._sign != other._sign:
            # If the answer is 0, the sign should be negative, in this case.
            negativezero = 1

        if not self and not other:
            sign = min(self._sign, other._sign)
            if negativezero:
                sign = 1
            ans = Decimal( (sign, (0,), exp))
            if shouldround:
                ans = ans._fix(context)
            return ans
        if not self:
            exp = max(exp, other._exp - context.prec-1)
            ans = other._rescale(exp, watchexp=0, context=context)
            if shouldround:
                ans = ans._fix(context)
            return ans
        if not other:
            exp = max(exp, self._exp - context.prec-1)
            ans = self._rescale(exp, watchexp=0, context=context)
            if shouldround:
                ans = ans._fix(context)
            return ans

        op1 = _WorkRep(self)
        op2 = _WorkRep(other)
        op1, op2 = _normalize(op1, op2, shouldround, context.prec)

        result = _WorkRep()
        if op1.sign != op2.sign:
            # Equal and opposite
            if op1.int == op2.int:
                if exp < context.Etiny():
                    exp = context.Etiny()
                    context._raise_error(Clamped)
                return Decimal((negativezero, (0,), exp))
            if op1.int < op2.int:
                op1, op2 = op2, op1
                # OK, now abs(op1) > abs(op2)
            if op1.sign == 1:
                result.sign = 1
                op1.sign, op2.sign = op2.sign, op1.sign
            else:
                result.sign = 0
                # So we know the sign, and op1 > 0.
        elif op1.sign == 1:
            result.sign = 1
            op1.sign, op2.sign = (0, 0)
        else:
            result.sign = 0
        # Now, op1 > abs(op2) > 0

        if op2.sign == 0:
            result.int = op1.int + op2.int
        else:
            result.int = op1.int - op2.int

        result.exp = op1.exp
        ans = Decimal(result)
        if shouldround:
            ans = ans._fix(context)
        return ans

    __radd__ = __add__

    def __sub__(self, other, context=None):
        """Return self + (-other)"""
        other = _convert_other(other)
        if other is NotImplemented:
            return other

        if self._is_special or other._is_special:
            ans = self._check_nans(other, context=context)
            if ans:
                return ans

        # -Decimal(0) = Decimal(0), which we don't want since
        # (-0 - 0 = -0 + (-0) = -0, but -0 + 0 = 0.)
        # so we change the sign directly to a copy
        tmp = Decimal(other)
        tmp._sign = 1-tmp._sign

        return self.__add__(tmp, context=context)

    def __rsub__(self, other, context=None):
        """Return other + (-self)"""
        other = _convert_other(other)
        if other is NotImplemented:
            return other

        tmp = Decimal(self)
        tmp._sign = 1 - tmp._sign
        return other.__add__(tmp, context=context)

    def _increment(self, round=1, context=None):
        """Special case of add, adding 1eExponent

        Since it is common, (rounding, for example) this adds
        (sign)*one E self._exp to the number more efficiently than add.

        For example:
        Decimal('5.624e10')._increment() == Decimal('5.625e10')
        """
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans

            # Must be infinite, and incrementing makes no difference
            return Decimal(self)

        L = list(self._int)
        L[-1] += 1
        spot = len(L)-1
        while L[spot] == 10:
            L[spot] = 0
            if spot == 0:
                L[0:0] = [1]
                break
            L[spot-1] += 1
            spot -= 1
        ans = Decimal((self._sign, L, self._exp))

        if context is None:
            context = getcontext()
        if round and context._rounding_decision == ALWAYS_ROUND:
            ans = ans._fix(context)
        return ans

    def __mul__(self, other, context=None):
        """Return self * other.

        (+-) INF * 0 (or its reverse) raise InvalidOperation.
        """
        other = _convert_other(other)
        if other is NotImplemented:
            return other

        if context is None:
            context = getcontext()

        resultsign = self._sign ^ other._sign

        if self._is_special or other._is_special:
            ans = self._check_nans(other, context)
            if ans:
                return ans

            if self._isinfinity():
                if not other:
                    return context._raise_error(InvalidOperation, '(+-)INF * 0')
                return Infsign[resultsign]

            if other._isinfinity():
                if not self:
                    return context._raise_error(InvalidOperation, '0 * (+-)INF')
                return Infsign[resultsign]

        resultexp = self._exp + other._exp
        shouldround = context._rounding_decision == ALWAYS_ROUND

        # Special case for multiplying by zero
        if not self or not other:
            ans = Decimal((resultsign, (0,), resultexp))
            if shouldround:
                # Fixing in case the exponent is out of bounds
                ans = ans._fix(context)
            return ans

        # Special case for multiplying by power of 10
        if self._int == (1,):
            ans = Decimal((resultsign, other._int, resultexp))
            if shouldround:
                ans = ans._fix(context)
            return ans
        if other._int == (1,):
            ans = Decimal((resultsign, self._int, resultexp))
            if shouldround:
                ans = ans._fix(context)
            return ans

        op1 = _WorkRep(self)
        op2 = _WorkRep(other)

        ans = Decimal((resultsign, map(int, str(op1.int * op2.int)), resultexp))
        if shouldround:
            ans = ans._fix(context)

        return ans
    __rmul__ = __mul__

    def __div__(self, other, context=None):
        """Return self / other."""
        return self._divide(other, context=context)
    __truediv__ = __div__

    def _divide(self, other, divmod = 0, context=None):
        """Return a / b, to context.prec precision.

        divmod:
        0 => true division
        1 => (a //b, a%b)
        2 => a //b
        3 => a%b

        Actually, if divmod is 2 or 3 a tuple is returned, but errors for
        computing the other value are not raised.
        """
        other = _convert_other(other)
        if other is NotImplemented:
            if divmod in (0, 1):
                return NotImplemented
            return (NotImplemented, NotImplemented)

        if context is None:
            context = getcontext()

        sign = self._sign ^ other._sign

        if self._is_special or other._is_special:
            ans = self._check_nans(other, context)
            if ans:
                if divmod:
                    return (ans, ans)
                return ans

            if self._isinfinity() and other._isinfinity():
                if divmod:
                    reloco = (context._raise_error(InvalidOperation,
                                            '(+-)INF // (+-)INF'),
                            context._raise_error(InvalidOperation,
                                            '(+-)INF % (+-)INF'))
                    return reloco
                return context._raise_error(InvalidOperation, '(+-)INF/(+-)INF')

            if self._isinfinity():
                if divmod == 1:
                    return (Infsign[sign],
                            context._raise_error(InvalidOperation, 'INF % x'))
                elif divmod == 2:
                    return (Infsign[sign], NaN)
                elif divmod == 3:
                    return (Infsign[sign],
                            context._raise_error(InvalidOperation, 'INF % x'))
                return Infsign[sign]

            if other._isinfinity():
                if divmod:
                    return (Decimal((sign, (0,), 0)), Decimal(self))
                context._raise_error(Clamped, 'Division by infinity')
                return Decimal((sign, (0,), context.Etiny()))

        # Special cases for zeroes
        if not self and not other:
            if divmod:
                return context._raise_error(DivisionUndefined, '0 / 0', 1)
            return context._raise_error(DivisionUndefined, '0 / 0')

        if not self:
            if divmod:
                otherside = Decimal(self)
                otherside._exp = min(self._exp, other._exp)
                return (Decimal((sign, (0,), 0)),  otherside)
            exp = self._exp - other._exp
            if exp < context.Etiny():
                exp = context.Etiny()
                context._raise_error(Clamped, '0e-x / y')
            if exp > context.Emax:
                exp = context.Emax
                context._raise_error(Clamped, '0e+x / y')
            return Decimal( (sign, (0,), exp) )

        if not other:
            if divmod:
                return context._raise_error(DivisionByZero, 'divmod(x,0)',
                                           sign, 1)
            return context._raise_error(DivisionByZero, 'x / 0', sign)

        # OK, so neither = 0, INF or NaN
        shouldround = context._rounding_decision == ALWAYS_ROUND

        # If we're dividing into ints, and self < other, stop.
        # self.__abs__(0) does not round.
        if divmod and (self.__abs__(0, context) < other.__abs__(0, context)):

            if divmod == 1 or divmod == 3:
                exp = min(self._exp, other._exp)
                ans2 = self._rescale(exp, context=context, watchexp=0)
                if shouldround:
                    ans2 = ans2._fix(context)
                return (Decimal( (sign, (0,), 0) ),
                        ans2)

            elif divmod == 2:
                # Don't round the mod part, if we don't need it.
                return (Decimal( (sign, (0,), 0) ), Decimal(self))

        op1 = _WorkRep(self)
        op2 = _WorkRep(other)
        op1, op2, adjust = _adjust_coefficients(op1, op2)
        res = _WorkRep( (sign, 0, (op1.exp - op2.exp)) )
        if divmod and res.exp > context.prec + 1:
            return context._raise_error(DivisionImpossible)

        prec_limit = 10 ** context.prec
        while 1:
            while op2.int <= op1.int:
                res.int += 1
                op1.int -= op2.int
            if res.exp == 0 and divmod:
                if res.int >= prec_limit and shouldround:
                    return context._raise_error(DivisionImpossible)
                otherside = Decimal(op1)
                frozen = context._ignore_all_flags()

                exp = min(self._exp, other._exp)
                otherside = otherside._rescale(exp, context=context, watchexp=0)
                context._regard_flags(*frozen)
                if shouldround:
                    otherside = otherside._fix(context)
                return (Decimal(res), otherside)

            if op1.int == 0 and adjust >= 0 and not divmod:
                break
            if res.int >= prec_limit and shouldround:
                if divmod:
                    return context._raise_error(DivisionImpossible)
                shouldround=1
                # Really, the answer is a bit higher, so adding a one to
                # the end will make sure the rounding is right.
                if op1.int != 0:
                    res.int *= 10
                    res.int += 1
                    res.exp -= 1

                break
            res.int *= 10
            res.exp -= 1
            adjust += 1
            op1.int *= 10
            op1.exp -= 1

            if res.exp == 0 and divmod and op2.int > op1.int:
                # Solves an error in precision.  Same as a previous block.

                if res.int >= prec_limit and shouldround:
                    return context._raise_error(DivisionImpossible)
                otherside = Decimal(op1)
                frozen = context._ignore_all_flags()

                exp = min(self._exp, other._exp)
                otherside = otherside._rescale(exp, context=context)

                context._regard_flags(*frozen)

                return (Decimal(res), otherside)

        ans = Decimal(res)
        if shouldround:
            ans = ans._fix(context)
        return ans

    def __rdiv__(self, other, context=None):
        """Swaps self/other and returns __div__."""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        return other.__div__(self, context=context)
    __rtruediv__ = __rdiv__

    def __divmod__(self, other, context=None):
        """
        (self // other, self % other)
        """
        return self._divide(other, 1, context)

    def __rdivmod__(self, other, context=None):
        """Swaps self/other and returns __divmod__."""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        return other.__divmod__(self, context=context)

    def __mod__(self, other, context=None):
        """
        self % other
        """
        other = _convert_other(other)
        if other is NotImplemented:
            return other

        if self._is_special or other._is_special:
            ans = self._check_nans(other, context)
            if ans:
                return ans

        if self and not other:
            return context._raise_error(InvalidOperation, 'x % 0')

        return self._divide(other, 3, context)[1]

    def __rmod__(self, other, context=None):
        """Swaps self/other and returns __mod__."""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        return other.__mod__(self, context=context)

    def remainder_near(self, other, context=None):
        """
        Remainder nearest to 0-  abs(remainder-near) <= other/2
        """
        other = _convert_other(other)
        if other is NotImplemented:
            return other

        if self._is_special or other._is_special:
            ans = self._check_nans(other, context)
            if ans:
                return ans
        if self and not other:
            return context._raise_error(InvalidOperation, 'x % 0')

        if context is None:
            context = getcontext()
        # If DivisionImpossible causes an error, do not leave Rounded/Inexact
        # ignored in the calling function.
        context = context._shallow_copy()
        flags = context._ignore_flags(Rounded, Inexact)
        # Keep DivisionImpossible flags
        (side, r) = self.__divmod__(other, context=context)

        if r._isnan():
            context._regard_flags(*flags)
            return r

        context = context._shallow_copy()
        rounding = context._set_rounding_decision(NEVER_ROUND)

        if other._sign:
            comparison = other.__div__(Decimal(-2), context=context)
        else:
            comparison = other.__div__(Decimal(2), context=context)

        context._set_rounding_decision(rounding)
        context._regard_flags(*flags)

        s1, s2 = r._sign, comparison._sign
        r._sign, comparison._sign = 0, 0

        if r < comparison:
            r._sign, comparison._sign = s1, s2
            # Get flags now
            self.__divmod__(other, context=context)
            return r._fix(context)
        r._sign, comparison._sign = s1, s2

        rounding = context._set_rounding_decision(NEVER_ROUND)

        (side, r) = self.__divmod__(other, context=context)
        context._set_rounding_decision(rounding)
        if r._isnan():
            return r

        decrease = not side._iseven()
        rounding = context._set_rounding_decision(NEVER_ROUND)
        side = side.__abs__(context=context)
        context._set_rounding_decision(rounding)

        s1, s2 = r._sign, comparison._sign
        r._sign, comparison._sign = 0, 0
        if r > comparison or decrease and r == comparison:
            r._sign, comparison._sign = s1, s2
            context.prec += 1
            numbsquant = len(side.__add__(Decimal(1), context=context)._int)
            if numbsquant >= context.prec:
                context.prec -= 1
                return context._raise_error(DivisionImpossible)[1]
            context.prec -= 1
            if self._sign == other._sign:
                r = r.__sub__(other, context=context)
            else:
                r = r.__add__(other, context=context)
        else:
            r._sign, comparison._sign = s1, s2

        return r._fix(context)

    def __floordiv__(self, other, context=None):
        """self // other"""
        return self._divide(other, 2, context)[0]

    def __rfloordiv__(self, other, context=None):
        """Swaps self/other and returns __floordiv__."""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        return other.__floordiv__(self, context=context)

    def __float__(self):
        """Float representation."""
        return float(str(self))

    def __int__(self):
        """Converts self to an int, truncating if necessary."""
        if self._is_special:
            if self._isnan():
                context = getcontext()
                return context._raise_error(InvalidContext)
            elif self._isinfinity():
                raise OverflowError("Cannot convert infinity to long")
        if self._exp >= 0:
            s = ''.join(map(str, self._int)) + '0'*self._exp
        else:
            s = ''.join(map(str, self._int))[:self._exp]
        if s == '':
            s = '0'
        sign = '-'*self._sign
        return int(sign + s)

    def __long__(self):
        """Converts to a long.

        Equivalent to long(int(self))
        """
        return long(self.__int__())

    def _fix(self, context):
        """Round if it is necessary to keep self within prec precision.

        Rounds and fixes the exponent.  Does not raise on a sNaN.

        Arguments:
        self - Decimal instance
        context - context used.
        """
        if self._is_special:
            return self
        if context is None:
            context = getcontext()
        prec = context.prec
        ans = self._fixexponents(context)
        if len(ans._int) > prec:
            ans = ans._round(prec, context=context)
            ans = ans._fixexponents(context)
        return ans

    def _fixexponents(self, context):
        """Fix the exponents and return a copy with the exponent in bounds.
        Only call if known to not be a special value.
        """

        ans = self
        # deal with zeros first
        if not ans:
            Etiny = context.Etiny()
            if ans._exp < Etiny:
                ans = Decimal(self)
                ans._exp = Etiny
                context._raise_error(Clamped)
            else:
                if context._clamp:
                    exp_max = context.Etop()
                else:
                    exp_max = context.Emax
                if ans._exp > exp_max:
                    ans = Decimal(self)
                    ans._exp = exp_max
                    context._raise_error(Clamped)
            return ans

        # self is nonzero; if adjusted exponent is > Emax, overflow
        ans_adjusted = ans.adjusted()
        if ans_adjusted > context.Emax:
            context._raise_error(Inexact)
            context._raise_error(Rounded)
            c = context._raise_error(Overflow, 'above Emax', ans._sign)
            return c

        # Now check for subnormal results, and for the need to fold
        # down.  These two conditions are *not* mutually
        # exclusive---when the precision is large and Emin and Emax
        # are small it's quite possible to have Emin > Etop.
        # (Actually, the specification requires Emin and Emax to be at
        # least 5*precision, so this shouldn't happen, but it never
        # hurts to be careful.)
        if context._clamp:
            Etop = context.Etop()
            if ans._exp > Etop:
                context._raise_error(Clamped)
                ans = ans._rescale(Etop, context=context)

        if ans_adjusted < context.Emin:
            context._raise_error(Subnormal)
            Etiny = context.Etiny()
            if ans._exp < Etiny:
                ans_before_rescale = ans
                ans = ans._rescale(Etiny, context=context)
                if ans != ans_before_rescale:
                    context._raise_error(Underflow)
                    if not ans:
                        context._raise_error(Clamped)

        return ans

    def _round(self, prec=None, rounding=None, context=None, forceExp=None, fromQuantize=False):
        """Returns a rounded version of self.

        You can specify the precision or rounding method.  Otherwise, the
        context determines it.
        """

        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans

            if self._isinfinity():
                return Decimal(self)

        if context is None:
            context = getcontext()

        if rounding is None:
            rounding = context.rounding
        if prec is None:
            prec = context.prec

        if not self:
            if prec <= 0:
                dig = (0,)
                exp = len(self._int) - prec + self._exp
            else:
                dig = (0,) * prec
                exp = len(self._int) + self._exp - prec
            ans = Decimal((self._sign, dig, exp))
            context._raise_error(Rounded)
            return ans

        if prec == 0:
            temp = Decimal(self)
            temp._int = (0,)+temp._int
            prec = 1
        elif prec < 0:
            exp = self._exp + len(self._int) - prec - 1
            temp = Decimal( (self._sign, (0, 1), exp))
            prec = 1
        else:
            temp = Decimal(self)

        numdigits = len(temp._int)

#        # See if we need to extend precision
        expdiff = prec - numdigits

        # not allowing subnormal for quantize
        if fromQuantize and (forceExp - context.Emax) > context.prec:
            context._raise_error(InvalidOperation, "Quantize doesn't allow subnormal")
            return NaN

        if expdiff >= 0:
            if fromQuantize and len(temp._int)+expdiff > context.prec:
                context._raise_error(InvalidOperation, 'Beyond guarded precision')
                return NaN
            tmp = list(temp._int)
            tmp.extend([0] * expdiff)
            ans =  Decimal( (temp._sign, tmp, temp._exp - expdiff))
            return ans

        # OK, but maybe all the lost digits are 0.
        lostdigits = self._int[expdiff:]
        if lostdigits == (0,) * len(lostdigits):
            ans = Decimal( (temp._sign, temp._int[:prec], temp._exp - expdiff))
            # Rounded, but not Inexact
            context._raise_error(Rounded)
            return ans

        # Okay, let's round and lose data, let's get the correct rounding function
        this_function = getattr(temp, self._pick_rounding_function[rounding])

        # Now we've got the rounding function
        origprec = context.prec
        if prec != context.prec:
            context = context._shallow_copy()
            context.prec = prec
        ans = this_function(prec, expdiff, context)

        if forceExp is not None:
            exp = forceExp
            if fromQuantize and not (context.Emin <= exp <= context.Emax):
                if (context.Emin <= ans._exp) and ans._int == (0,):
                    context._raise_error(InvalidOperation)
                    return NaN

            if context.Emin < exp < context.Emax:
                newdiff = ans._exp - exp
                if newdiff >= 0:
                    ans._int = ans._int + tuple([0]*newdiff)
                else:
                    ans._int = (0,)
                ans._exp = exp
            else:
                if not context.flags[Underflow]:
                    newdiff = ans._exp - exp
                    if newdiff >= 0:
                        ans._int = ans._int + tuple([0]*newdiff)
                    else:
                        ans._int = (0,)

                ans._exp = exp
                context._raise_error(Rounded)
                context._raise_error(Inexact, 'Changed in rounding')
                return ans

            if len(ans._int) > origprec:
                context._raise_error(InvalidOperation, 'Beyond guarded precision')
                return NaN

        context._raise_error(Rounded)
        context._raise_error(Inexact, 'Changed in rounding')
        return ans

    _pick_rounding_function = {}

    def _round_down(self, prec, expdiff, context):
        """Also known as round-towards-0, truncate."""
        return Decimal( (self._sign, self._int[:prec], self._exp - expdiff) )

    def _round_half_up(self, prec, expdiff, context, tmp = None):
        """Rounds 5 up (away from 0)"""

        if tmp is None:
            tmp = Decimal( (self._sign,self._int[:prec], self._exp - expdiff))
        if self._int[prec] >= 5:
            tmp = tmp._increment(round=0, context=context)
            if len(tmp._int) > prec:
                return Decimal( (tmp._sign, tmp._int[:-1], tmp._exp + 1))
        return tmp

    def _round_half_even(self, prec, expdiff, context):
        """Round 5 to even, rest to nearest."""

        tmp = Decimal( (self._sign, self._int[:prec], self._exp - expdiff))
        half = (self._int[prec] == 5)
        if half:
            for digit in self._int[prec+1:]:
                if digit != 0:
                    half = 0
                    break
        if half:
            if self._int[prec-1] & 1 == 0:
                return tmp
        return self._round_half_up(prec, expdiff, context, tmp)

    def _round_half_down(self, prec, expdiff, context):
        """Round 5 down"""

        tmp = Decimal( (self._sign, self._int[:prec], self._exp - expdiff))
        half = (self._int[prec] == 5)
        if half:
            for digit in self._int[prec+1:]:
                if digit != 0:
                    half = 0
                    break
        if half:
            return tmp
        return self._round_half_up(prec, expdiff, context, tmp)

    def _round_up(self, prec, expdiff, context):
        """Rounds away from 0."""
        tmp = Decimal( (self._sign, self._int[:prec], self._exp - expdiff) )
        for digit in self._int[prec:]:
            if digit != 0:
                tmp = tmp._increment(round=1, context=context)
                if len(tmp._int) > prec:
                    return Decimal( (tmp._sign, tmp._int[:-1], tmp._exp + 1))
                else:
                    return tmp
        return tmp

    def _round_ceiling(self, prec, expdiff, context):
        """Rounds up (not away from 0 if negative.)"""
        if self._sign:
            return self._round_down(prec, expdiff, context)
        else:
            return self._round_up(prec, expdiff, context)

    def _round_floor(self, prec, expdiff, context):
        """Rounds down (not towards 0 if negative)"""
        if not self._sign:
            return self._round_down(prec, expdiff, context)
        else:
            return self._round_up(prec, expdiff, context)

    def fma(self, other, third, context=None):
        """Fused multiply-add.

        Returns self*other+third with no rounding of the intermediate
        product self*other.

        self and other are multiplied together, with no rounding of
        the result.  The third operand is then added to the result,
        and a single final rounding is performed.
        """

        if context is None:
            context = getcontext()

        other = _convert_other(other)
        if other is NotImplemented:
            return other

        third = _convert_other(third)
        if third is NotImplemented:
            return third

        # deal correctly with NaNs:
        self_is_nan = self._isnan()
        other_is_nan = other._isnan()
        third_is_nan = third._isnan()
        if self_is_nan or other_is_nan or third_is_nan:
            if self_is_nan == 2:
                return context._raise_error(InvalidOperation, 'sNaN',
                                        1, self)
            if other_is_nan == 2:
                return context._raise_error(InvalidOperation, 'sNaN',
                                        1, other)
            if third_is_nan == 2:
                return context._raise_error(InvalidOperation, 'sNaN',
                                        1, third)
            if self_is_nan:
                return self
            if other_is_nan:
                return other
            return third

        context = context._shallow_copy()
        rounding_decision = context._set_rounding_decision(NEVER_ROUND)
        product = self.__mul__(other, context)
        context._set_rounding_decision(rounding_decision)
        return product.__add__(third, context)

    def __pow__(self, n, modulo=None, context=None):
        """Return self ** n (mod modulo)

        If modulo is None (default), don't take it mod modulo.
        """
        n = _convert_other(n)
        if n is NotImplemented:
            return n

        if context is None:
            context = getcontext()
        if n._exp == 0 and n._sign == 0 and len(n._int) > context.prec:
            return context._raise_error(InvalidContext)

#        # FIXME: this block code was against the new handling of Infinities
#        # I think we could remove them safely, do not know what the "n.adjusted()>8"
#        # actually means, so I won't be sure until all the tests passes ok.
#        #         . Facundo
#        if self._is_special or n._is_special:# or n.adjusted() > 8:
#            # Because the spot << doesn't work with really big exponents
#            if n._isinfinity() or n.adjusted() > 8:
#                return context._raise_error(InvalidOperation, 'x ** INF')

        ans = self._check_nans(n, context)
        if ans:
            return ans

        if not n:
            if self:
                return Decimal(1)  # something ** 0
            else:
                return context._raise_error(InvalidOperation, '0 ** 0')

        if not self:
            if n._sign == 0:
                zero = Decimal(0)
                if n._iseven():
                    return zero
                zero._sign = self._sign
                return zero
            # n is negative
            if self._sign == 0:
                return Inf
            # also self is negative
            if n._iseven():
                return Inf
            else:
                return negInf

        self_inf = self._isinfinity()
        n_inf = n._isinfinity()
        if self == Decimal(1):
            if n_inf:
                context._raise_error(Inexact)
                context._raise_error(Rounded)
                digits = (1,)+(0,)*(context.prec-1)
                return Decimal((0, digits, -context.prec+1))
            return Decimal(1)

        if self_inf == -1 and n_inf:
            return context._raise_error(InvalidOperation, '-Inf ** +-Inf')

        if self_inf:
            if modulo:
                return context._raise_error(InvalidOperation, 'INF % x')
            if not n:
                return Decimal(1)
        if self_inf == 1:
            if n._sign == 1:
                return Decimal(0)
            return Inf
        if self_inf == -1:
            if abs(n) < 1:
                return context._raise_error(InvalidOperation, '-INF ** -1<n<1')
            if n._sign == 0:
                if n._iseven():
                    return Inf
                else:
                    return negInf
            if n._iseven():
                return Decimal(0)
            else:
                return Decimal((1, (0,), 0))

        if n_inf and self._sign == 1:
            return context._raise_error(InvalidOperation, '-num ** Inf')
        if n_inf == 1:
            if self < 1:
                return Decimal(0)
            else:
                return Inf
        if n_inf == -1:
            if self > 1:
                return Decimal(0)
            else:
                return Inf

        sign = self._sign and not n._iseven()
        n = int(n)
        # With ludicrously large exponent, just raise an overflow
        # and return inf.
        if not modulo and n > 0 and \
           (self._exp + len(self._int) - 1) * n > context.Emax and self:

            tmp = Decimal('inf')
            tmp._sign = sign
            context._raise_error(Rounded)
            context._raise_error(Inexact)
            context._raise_error(Overflow, 'Big power', sign)
            return tmp

        elength = len(str(abs(n)))
        firstprec = context.prec

        if not modulo and firstprec + elength + 1 > DefaultContext.Emax:
            return context._raise_error(Overflow, 'Too much precision.', sign)

        mul = Decimal(self)
        val = Decimal(1)
        context = context._shallow_copy()
        context.prec = firstprec + elength + 1
        if n < 0:
            # n is a long now, not Decimal instance
            n = -n
            mul = Decimal(1).__div__(mul, context=context)

        spot = 1
        while spot <= n:
            spot <<= 1

        spot >>= 1
        # spot is the highest power of 2 less than n
        while spot:
            val = val.__mul__(val, context=context)
            if val._isinfinity():
                val = Infsign[sign]
                break
            if spot & n:
                val = val.__mul__(mul, context=context)
            if modulo is not None:
                val = val.__mod__(modulo, context=context)
            spot >>= 1
        context.prec = firstprec

        if context._rounding_decision == ALWAYS_ROUND:
            return val._fix(context)
        return val

    def __rpow__(self, other, context=None):
        """Swaps self/other and returns __pow__."""
        other = _convert_other(other)
        if other is NotImplemented:
            return other
        return other.__pow__(self, context=context)

    def normalize(self, context=None):
        """Normalize- strip trailing 0s, change anything equal to 0 to 0e0"""

        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans

        dup = self._fix(context)
        if dup._isinfinity():
            return dup

        if not dup:
            return Decimal( (dup._sign, (0,), 0) )
        end = len(dup._int)
        exp = dup._exp
        while dup._int[end-1] == 0:
            exp += 1
            end -= 1
        return Decimal( (dup._sign, dup._int[:end], exp) )


    def quantize(self, exp, rounding=None, context=None, watchexp=1):
        """Quantize self so its exponent is the same as that of exp.

        Similar to self._rescale(exp._exp) but with error checking.
        """
        if self._is_special or exp._is_special:
            ans = self._check_nans(exp, context)
            if ans:
                return ans

            if exp._isinfinity() or self._isinfinity():
                if exp._isinfinity() and self._isinfinity():
                    return self  # if both are inf, it is OK
                if context is None:
                    context = getcontext()
                return context._raise_error(InvalidOperation,
                                        'quantize with one INF')
        return self._rescale(exp._exp, rounding, context, watchexp=0, fromQuantize=True)

    def same_quantum(self, other):
        """Test whether self and other have the same exponent.

        same as self._exp == other._exp, except NaN == sNaN
        """
        if self._is_special or other._is_special:
            if self._isnan() or other._isnan():
                return self._isnan() and other._isnan() and True
            if self._isinfinity() or other._isinfinity():
                return self._isinfinity() and other._isinfinity() and True
        return self._exp == other._exp

    def _rescale(self, exp, rounding=None, context=None, watchexp=1, fromQuantize=False):
        """Rescales so that the exponent is exp.

        exp = exp to scale to (an integer)
        rounding = rounding version
        watchexp: if set (default) an error is returned if exp is greater
        than Emax or less than Etiny.
        """
        if context is None:
            context = getcontext()

        if self._is_special:
            if self._isinfinity():
                return context._raise_error(InvalidOperation, 'rescale with an INF')

            ans = self._check_nans(context=context)
            if ans:
                return ans

        if fromQuantize and (context.Emax  < exp or context.Etiny() > exp):
            return context._raise_error(InvalidOperation, 'rescale(a, INF)')
        if fromQuantize and exp < context.Etiny():
            return context._raise_error(InvalidOperation, '"rhs" must be no less than Etiny')

        if not self:
            ans = Decimal(self)
            ans._int = (0,)
            ans._exp = exp
            return ans

        diff = self._exp - exp
        digits = len(self._int) + diff

        if watchexp and digits > context.prec:
            return context._raise_error(InvalidOperation, 'Rescale > prec')

        tmp = Decimal(self)

        if digits < 0:
            tmp._exp = -digits + tmp._exp
            tmp._int = (0,1)
            digits = 1
        tmp = tmp._round(digits, rounding, context=context, forceExp=exp, fromQuantize=fromQuantize)

        if watchexp or fromQuantize:
            tmp_adjusted = tmp.adjusted()
            if tmp and tmp_adjusted < context.Emin:
                context._raise_error(Subnormal)
            elif tmp and tmp_adjusted > context.Emax:
                return context._raise_error(InvalidOperation, 'rescale(a, INF)')
        return tmp

    def to_integral_value(self, rounding=None, context=None):
        """Rounds to the nearest integer, without raising inexact, rounded."""
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans
        if self._exp >= 0:
            return self
        if context is None:
            context = getcontext()
        flags = context._ignore_flags(Rounded, Inexact)
        ans = self._rescale(0, rounding, context=context)
        context._regard_flags(flags)
        return ans

    # the method name changed, but we provide also the old one, for compatibility
    to_integral = to_integral_value

    def sqrt(self, context=None):
        """Return the square root of self."""
        if self._is_special:
            ans = self._check_nans(context=context)
            if ans:
                return ans

            if self._isinfinity() and self._sign == 0:
                return Decimal(self)

        if not self:
            # exponent = self._exp // 2.  sqrt(-0) = -0
            ans = Decimal((self._sign, (0,), self._exp // 2))
            return ans._fix(context)

        if context is None:
            context = getcontext()

        if self._sign == 1:
            return context._raise_error(InvalidOperation, 'sqrt(-x), x > 0')

        # At this point self represents a positive number.  Let p be
        # the desired precision and express self in the form c*100**e
        # with c a positive real number and e an integer, c and e
        # being chosen so that 100**(p-1) <= c < 100**p.  Then the
        # (exact) square root of self is sqrt(c)*10**e, and 10**(p-1)
        # <= sqrt(c) < 10**p, so the closest representable Decimal at
        # precision p is n*10**e where n = round_half_even(sqrt(c)),
        # the closest integer to sqrt(c) with the even integer chosen
        # in the case of a tie.
        #
        # To ensure correct rounding in all cases, we use the
        # following trick: we compute the square root to an extra
        # place (precision p+1 instead of precision p), rounding down.
        # Then, if the result is inexact and its last digit is 0 or 5,
        # we increase the last digit to 1 or 6 respectively; if it's
        # exact we leave the last digit alone.  Now the final round to
        # p places (or fewer in the case of underflow) will round
        # correctly and raise the appropriate flags.

        # use an extra digit of precision
        prec = context.prec+1

        # write argument in the form c*100**e where e = self._exp//2
        # is the 'ideal' exponent, to be used if the square root is
        # exactly representable.  l is the number of 'digits' of c in
        # base 100, so that 100**(l-1) <= c < 100**l.
        op = _WorkRep(self)
        e = op.exp >> 1
        if op.exp & 1:
            c = op.int * 10
            l = (len(self._int) >> 1) + 1
        else:
            c = op.int
            l = len(self._int)+1 >> 1

        # rescale so that c has exactly prec base 100 'digits'
        shift = prec-l
        if shift >= 0:
            c *= 100**shift
            exact = True
        else:
            c, remainder = divmod(c, 100**-shift)
            exact = not remainder
        e -= shift

        # find n = floor(sqrt(c)) using Newton's method
        n = 10**prec
        while True:
            q = c//n
            if n <= q:
                break
            else:
                n = n + q >> 1
        exact = exact and n*n == c

        if exact:
            # result is exact; rescale to use ideal exponent e
            if shift >= 0:
                # assert n % 10**shift == 0
                n //= 10**shift
            else:
                n *= 10**-shift
            e += shift
        else:
            # result is not exact; fix last digit as described above
            if n % 5 == 0:
                n += 1

        ans = Decimal((0, map(int, str(n)), e))

        # round, and fit to current context
        context = context._shallow_copy()
        rounding = context._set_rounding(ROUND_HALF_EVEN)
        ans = ans._fix(context)
        context.rounding = rounding

        return ans

    def max(self, other, context=None):
        """Returns the larger value.

        Like max(self, other) except if one is not a number, returns
        NaN (and signals if one is sNaN).  Also rounds.
        """
        other = _convert_other(other)
        if other is NotImplemented:
            return other

        if self._is_special or other._is_special:
            # If one operand is a quiet NaN and the other is number, then the
            # number is always returned
            if other._exp == 'P':
                return other
            sn = self._isnan()
            on = other._isnan()
            if sn or on:
                if on == 1 and sn != 2:
                    return self
                if sn == 1 and on != 2:
                    return other
                return self._check_nans(other, context)

        ans = self
        c = self.__cmp__(other)
        if c == 0:
            # If both operands are finite and equal in numerical value
            # then an ordering is applied:
            #
            # If the signs differ then max returns the operand with the
            # positive sign and min returns the operand with the negative sign
            #
            # If the signs are the same then the exponent is used to select
            # the result.
            if self._sign != other._sign:
                if self._sign:
                    ans = other
            elif self._exp < other._exp and not self._sign:
                ans = other
            elif self._exp > other._exp and self._sign:
                ans = other
        elif c == -1:
            ans = other

        if context is None:
            context = getcontext()
        if context._rounding_decision == ALWAYS_ROUND:
            return ans._fix(context)
        return ans

    def min(self, other, context=None):
        """Returns the smaller value.

        Like min(self, other) except if one is not a number, returns
        NaN (and signals if one is sNaN).  Also rounds.
        """
        other = _convert_other(other)
        if other is NotImplemented:
            return other

        if self._is_special or other._is_special:
            # If one operand is a quiet NaN and the other is number, then the
            # number is always returned
            sn = self._isnan()
            on = other._isnan()
            if sn or on:
                if on == 1 and sn != 2:
                    return self
                if sn == 1 and on != 2:
                    return other
                return self._check_nans(other, context)

        ans = self
        c = self.__cmp__(other)
        if c == 0:
            # If both operands are finite and equal in numerical value
            # then an ordering is applied:
            #
            # If the signs differ then max returns the operand with the
            # positive sign and min returns the operand with the negative sign
            #
            # If the signs are the same then the exponent is used to select
            # the result.
            if self._sign != other._sign:
                if other._sign:
                    ans = other
            elif self._exp > other._exp and not self._sign:
                ans = other
            elif self._exp < other._exp and self._sign:
                ans = other
        elif c == 1:
            ans = other

        if context is None:
            context = getcontext()
        if context._rounding_decision == ALWAYS_ROUND:
            return ans._fix(context)
        return ans

    def _isinteger(self):
        """Returns whether self is an integer"""
        if self._exp >= 0:
            return True
        rest = self._int[self._exp:]
        return rest == (0,)*len(rest)

    def _iseven(self):
        """Returns 1 if self is even.  Assumes self is an integer."""
        if self._exp > 0:
            return 1
        return self._int[-1+self._exp] & 1 == 0

    def adjusted(self):
        """Return the adjusted exponent of self"""
        try:
            return self._exp + len(self._int) - 1
        # If NaN or Infinity, self._exp is string
        except TypeError:
            return 0

    def canonical(self, context=None):
        """Returns the same Decimal object.

        As we do not have different encodings for the same number, the
        received object already is in its canonical form.
        """
        return self

    def compare_signal(self, other, context=None):
        """Compares self to the other operand numerically.

        It's pretty much like compare(), but all NaNs signal, with signaling
        NaNs taking precedence over quiet NaNs.
        """

    def compare_total(self, other, context=None):
        """Compares self to other using the abstract representations.

        This is not like the standard compare, which use their numerical
        value. Note that a total ordering is defined for all possible abstract
        representations.
        """
        # if one is negative and the other is positive, it's easy
        if self._sign and not other._sign:
            return Decimal(-1)
        if not self._sign and other._sign:
            return Decimal(1)
        sign = self._sign

        # let's handle both NaN types
        self_nan = self._isnan()
        other_nan = other._isnan()
        if self_nan or other_nan:
            if self_nan == other_nan:
                if self._int < other._int:
                    if sign:
                        return Decimal(1)
                    else:
                        return Decimal(-1)
                if self._int > other._int:
                    if sign:
                        return Decimal(-1)
                    else:
                        return Decimal(1)
                return Decimal(0)

            if sign:
                if self_nan == 1:
                    return Decimal(-1)
                if other_nan == 1:
                    return Decimal(1)
                if self_nan == 2:
                    return Decimal(-1)
                if other_nan == 2:
                    return Decimal(1)
            else:
                if self_nan == 1:
                    return Decimal(1)
                if other_nan == 1:
                    return Decimal(-1)
                if self_nan == 2:
                    return Decimal(1)
                if other_nan == 2:
                    return Decimal(-1)

        if self < other:
            return Decimal(-1)
        if self > other:
            return Decimal(1)

        if self._exp < other._exp:
            if sign:
                return Decimal(1)
            else:
                return Decimal(-1)
        if self._exp > other._exp:
            if sign:
                return Decimal(-1)
            else:
                return Decimal(1)
        return Decimal(0)


    def compare_total_mag(self, other):
        """Compares self to other using abstract repr., ignoring sign.

        Like compare_total, but with operand's sign ignored and assumed to be 0.
        """
        s = self.copy_abs()
        o = other.copy_abs()
        return s.compare_total(o)

    def copy_abs(self):
        """Returns a copy with the sign set to 0. """
        return Decimal((0, self._int, self._exp))

    def copy_negate(self, context=None):
        """Returns a copy with the sign inverted."""
        if self._sign:
            return Decimal((0, self._int, self._exp))
        else:
            return Decimal((1, self._int, self._exp))

    def copy_sign(self, other, context=None):
        """Returns self with the sign of other."""
        return Decimal((other._sign, self._int, self._exp))

    def exp(self, context=None):
        """Returns e ** self."""

    def is_canonical(self, context=None):
        """Returns 1 if self is canonical; otherwise returns 0."""
        return Decimal(1)

    def is_finite(self, context=None):
        """Returns 1 if self is finite, otherwise returns 0.

        For it to be finite, it must be neither infinite nor a NaN.
        """
        if self._is_special:
            return Decimal(0)
        else:
            return Decimal(1)

    def is_infinite(self, context=None):
        """Returns 1 if self is an Infinite, otherwise returns 0."""
        if self._isinfinity():
            return Decimal(1)
        else:
            return Decimal(0)

    def is_nan(self, context=None):
        """Returns 1 if self is qNaN or sNaN, otherwise returns 0."""
        if self._isnan():
            return Decimal(1)
        else:
            return Decimal(0)

    def is_normal(self, context=None):
        """Returns 1 if self is a normal number, otherwise returns 0."""

    def is_qnan(self, context=None):
        """Returns 1 if self is a quiet NaN, otherwise returns 0."""
        if self._isnan() == 1:
            return Decimal(1)
        else:
            return Decimal(0)

    def is_signed(self, context=None):
        """Returns 1 if self is negative, otherwise returns 0."""
        return Decimal(self._sign)

    def is_snan(self, context=None):
        """Returns 1 if self is a signaling NaN, otherwise returns 0."""
        if self._isnan() == 2:
            return Decimal(1)
        else:
            return Decimal(0)

    def is_subnormal(self, context=None):
        """Returns 1 if self is subnormal, otherwise returns 0."""
        if context is None:
            context = getcontext()

        r = self._exp + len(self._int)
        if r <= context.Emin:
            return Decimal(1)
        return Decimal(0)

    def is_zero(self, context=None):
        """Returns 1 if self is a zero, otherwise returns 0."""
        if self:
            return Decimal(0)
        else:
            return Decimal(1)

    def ln(self, context=None):
        """Returns the natural (base e) logarithm of self."""

    def log10(self, context=None):
        """Returns the base 10 logarithm of self."""

    def logb(self, context=None):
        """ Returns the exponent of the magnitude of self's MSD.

        The result is the integer which is the exponent of the magnitude
        of the most significant digit of self (as though it were truncated
        to a single digit while maintaining the value of that digit and
        without limiting the resulting exponent).
        """

    def _islogical(self):
        """Return 1 is self is a logical operand.

        For being logical, it must be a finite numbers with a sign of 0,
        an exponent of 0, and a coefficient whose digits must all be
        either 0 or 1.
        """
        if self._sign != 0 or self._exp != 0:
            return 0
        for dig in self._int:
            if dig not in (0, 1):
                return 0
        return 1

    def _fill_logical(self, context, opa, opb):
        dif = context.prec - len(opa)
        if dif > 0:
            opa = (0,)*dif + opa
        elif dif < 0:
            opa = opa[-context.prec:]
        dif = context.prec - len(opb)
        if dif > 0:
            opb = (0,)*dif + opb
        elif dif < 0:
            opb = opb[-context.prec:]
        return opa, opb

    def logical_and(self, other, context=None):
        """Applies an 'and' operation between self and other's digits."""
        if context is None:
            context = getcontext()
        if not self._islogical() or not other._islogical():
            return context._raise_error(InvalidOperation)

        # fill to context.prec
        (opa, opb) = self._fill_logical(context, self._int, other._int)

        # make the operation, and clean starting zeroes
        result = [a&b for a,b in zip(opa,opb)]
        for i,d in enumerate(result):
            if d == 1:
                break
        result = tuple(result[i:])

        # if empty, we must have at least a zero
        if not result:
            result = (0,)
        return Decimal((0, result, 0))

    def logical_invert(self, context=None):
        """Invert all its digits."""
        if context is None:
            context = getcontext()
        return self.logical_xor(Decimal((0,(1,)*context.prec,0)), context)

    def logical_or(self, other, context=None):
        """Applies an 'or' operation between self and other's digits."""
        if context is None:
            context = getcontext()
        if not self._islogical() or not other._islogical():
            return context._raise_error(InvalidOperation)

        # fill to context.prec
        (opa, opb) = self._fill_logical(context, self._int, other._int)

        # make the operation, and clean starting zeroes
        result = [a|b for a,b in zip(opa,opb)]
        for i,d in enumerate(result):
            if d == 1:
                break
        result = tuple(result[i:])

        # if empty, we must have at least a zero
        if not result:
            result = (0,)
        return Decimal((0, result, 0))

    def logical_xor(self, other, context=None):
        """Applies an 'xor' operation between self and other's digits."""
        if context is None:
            context = getcontext()
        if not self._islogical() or not other._islogical():
            return context._raise_error(InvalidOperation)

        # fill to context.prec
        (opa, opb) = self._fill_logical(context, self._int, other._int)

        # make the operation, and clean starting zeroes
        result = [a^b for a,b in zip(opa,opb)]
        for i,d in enumerate(result):
            if d == 1:
                break
        result = tuple(result[i:])

        # if empty, we must have at least a zero
        if not result:
            result = (0,)
        return Decimal((0, result, 0))

    def max_mag(self, other, context=None):
        """Compares the values numerically with their sign ignored."""
        if context is None:
            context = getcontext()
        if self._isnan() == 2:
            return context._raise_error(InvalidOperation, 'Magnitude max with sNaN', 1, self)
        if other._isnan() == 2:
            return context._raise_error(InvalidOperation, 'Magnitude max with sNaN', 1, other)
        abs_self = abs(self)
        abs_other = abs(other)
        if abs_self == abs_other:
            if self._sign == other._sign:
                if self._sign == 0:
                    if self._exp >= other._exp:
                        return self
                    else:
                        return other
                else:
                    if self._exp < other._exp:
                        return self
                    else:
                        return other
            elif self._sign == 0:
                return self
            else:
                return other
        ans = abs_self.max(abs_other)
        if abs_self is ans:
            d = self._fix(context)
        else:
            d = other._fix(context)
        return d

    def min_mag(self, other, context=None):
        """Compares the values numerically with their sign ignored."""
        if context is None:
            context = getcontext()
        if self._isnan() == 2:
            return context._raise_error(InvalidOperation, 'Magnitude max with sNaN', 1, self)
        if other._isnan() == 2:
            return context._raise_error(InvalidOperation, 'Magnitude max with sNaN', 1, other)
        abs_self = abs(self)
        abs_other = abs(other)
        if abs_self == abs_other:
            if self._sign == other._sign:
                if self._sign == 0:
                    if self._exp >= other._exp:
                        return other
                    else:
                        return self
                else:
                    if self._exp < other._exp:
                        return other
                    else:
                        return self
            elif self._sign == 0:
                return other
            else:
                return self
        ans = abs_self.min(abs_other)
        if abs_self is ans:
            d = self._fix(context)
        else:
            d = other._fix(context)
        return d

    def next_minus(self, context=None):
        """Returns the largest representable number smaller than itself."""
        if context is None:
            context = getcontext()

        ans = self._check_nans(self, context)
        if ans:
            return ans

        minime = context.Emin-context.prec+1
        if self._isinfinity() == 1:
            return Decimal((0, (9,)*context.prec, context.Emax-context.prec+1))
        if self._isinfinity() == -1:
            return self

        if self._exp < minime:
            newself = Decimal((self._sign, self._int, minime))
            if newself._sign == 1:
                return newself
        else:
            newself = Decimal(self)

        if not newself:
            return Decimal((1, (1,), minime))

        expdif = context.prec - len(newself._int)
        if expdif < 0:
            # negative difference
            resto = newself._int[context.prec:]
            if resto != (0,)*(-expdif):
                # the rest is not all zeroes
                d = newself._round_floor(context.prec, expdif, context)
                return d
            # negative expdif, but all zeroes
            d = Decimal((newself._sign, newself._int[:expdif], newself._exp-expdif))
        else:
            # positive expdif
            if  newself._exp-expdif < minime:
                expdif = newself._exp - minime
            d = Decimal((newself._sign, newself._int+(0,)*expdif, newself._exp-expdif))
        dif = Decimal((0, (0,)*(len(d._int)-1)+(1,), d._exp))
        d = d - dif

        digdif = context.prec - len(d._int)
        if digdif > 0 and d._exp-digdif > context.Emin:
            d = Decimal((d._sign, d._int + (9,)*digdif, d._exp-digdif))
        if d.adjusted() > context.Emax:
            return negInf
        return d

    def next_plus(self, context=None):
        """Returns the smallest representable number larger than itself."""
        if context is None:
            context = getcontext()

        ans = self._check_nans(self, context)
        if ans:
            return ans

        if self._isinfinity() == 1:
            return self
        if self._isinfinity() == -1:
            return Decimal((1, (9,)*context.prec, context.Emax-context.prec+1))

        minime = context.Emin-context.prec+1
        if self._exp < minime:
            newself = Decimal((self._sign, self._int, minime))
            if newself._sign == 0:
                return newself
        else:
            newself = Decimal(self)

        if not newself:
            return Decimal((0, (1,), minime))
        expdif = context.prec - len(newself._int)

        if expdif < 0:
            resto = newself._int[context.prec:]
            if resto != (0,)*(-expdif):
                # the rest is not all zeroes
                d = newself._round_ceiling(context.prec, expdif, context)
                return d
            # negative expdif, but all zeroes
            d = Decimal((newself._sign, newself._int[:expdif], newself._exp-expdif))
        else:
            # positive expdif
            if newself._exp-expdif < minime:
                expdif = newself._exp - minime
            d = Decimal((newself._sign, newself._int+(0,)*expdif, newself._exp-expdif))

        dif = Decimal((0, (0,)*(len(d._int)-1)+(1,), d._exp))
        d = d + dif
        if not d:
            # restablish previos sign
            d._sign = newself._sign
            return d

        digdif = context.prec - len(d._int)
        if digdif > 0 and d._exp-digdif > context.Emin:
            d = Decimal((d._sign, d._int + (9,)*digdif, d._exp-digdif))
        if d.adjusted() > context.Emax:
            return Inf
        return d


    def next_toward(self, other, context=None):
        """Returns the number closest to itself, in direction towards other.

        The result is the closest to self representable number (but not
        self) that is in the direction towards other, unless the both have
        the same value.
        """

    def number_class(self, context=None):
        """Returns an indication of the class of self.

        The class is one of the following strings:
          -sNaN
          -NaN
          -Infinity
          -Normal
          -Subnormal
          -Zero
          +Zero
          +Subnormal
          +Normal
          +Infinity
        """
        if self.is_snan():
            return "sNaN"
        if self.is_qnan():
            return "NaN"
        inf = self._isinfinity()
        if inf == 1:
            return "+Infinity"
        if inf == -1:
            return "-Infinity"
        if self.is_zero():
            if self._sign:
                return "-Zero"
            else:
                return "+Zero"
        if context is None:
            context = getcontext()
        if self.is_subnormal(context=context):
            if self._sign:
                return "-Subnormal"
            else:
                return "+Subnormal"
        # just a normal, regular, boring number, :)
        if self._sign:
            return "-Normal"
        else:
            return "+Normal"

    def radix(self, context=None):
        """Just returns 10, as this is Decimal, :)"""
        return Decimal(10)

    def rotate(self, other, context=None):
        """Returns a rotated copy of self, value-of-other times."""
        if context is None:
            context = getcontext()

        ans = self._check_nans(other, context)
        if ans:
            return ans

        if other._exp != 0:
            return context._raise_error(InvalidOperation)
        if not (-context.prec <= int(other) <= context.prec):
            return context._raise_error(InvalidOperation)

        if self._isinfinity():
            return self

        # get values, pad if necessary
        torot = int(other)
        rotdig = self._int
        topad = context.prec - len(rotdig)
        if topad:
            rotdig = ((0,)*topad) + rotdig

        # let's rotate!
        rotated = rotdig[torot:] + rotdig[:torot]

        # clean starting zeroes
        for i,d in enumerate(rotated):
            if d != 0:
                break
        rotated = rotated[i:]

        return Decimal((self._sign, rotated, self._exp))


    def scaleb (self, other, context=None):
        """Returns self operand after adding the second value to its exp."""
        if context is None:
            context = getcontext()

        ans = self._check_nans(other, context)
        if ans:
            return ans

        if other._exp != 0:
            return context._raise_error(InvalidOperation)
        liminf = -2 * (context.Emax + context.prec)
        limsup =  2 * (context.Emax + context.prec)
        if not (liminf <= int(other) <= limsup):
            return context._raise_error(InvalidOperation)

        if self._isinfinity():
            return self

        d = Decimal((self._sign, self._int, self._exp + int(other)))
        d = d._fixexponents(context)
        return d

    def shift(self, other, context=None):
        """Returns a shifted copy of self, value-of-other times."""
        if context is None:
            context = getcontext()

        ans = self._check_nans(other, context)
        if ans:
            return ans

        if other._exp != 0:
            return context._raise_error(InvalidOperation)
        if not (-context.prec <= int(other) <= context.prec):
            return context._raise_error(InvalidOperation)

        if self._isinfinity():
            return self

        # get values, pad if necessary
        torot = int(other)
        if not torot:
            return self
        rotdig = self._int
        topad = context.prec - len(rotdig)
        if topad:
            rotdig = ((0,)*topad) + rotdig

        # let's shift!
        if torot < 0:
            rotated = rotdig[:torot]
        else:
            rotated = (rotdig + ((0,) * torot))
            rotated = rotated[-context.prec:]

        # clean starting zeroes
        if rotated:
            for i,d in enumerate(rotated):
                if d != 0:
                    break
            rotated = rotated[i:]
        else:
            rotated = (0,)

        return Decimal((self._sign, rotated, self._exp))


    # Support for pickling, copy, and deepcopy
    def __reduce__(self):
        return (self.__class__, (str(self),))

    def __copy__(self):
        if type(self) == Decimal:
            return self     # I'm immutable; therefore I am my own clone
        return self.__class__(str(self))

    def __deepcopy__(self, memo):
        if type(self) == Decimal:
            return self     # My components are also immutable
        return self.__class__(str(self))

##### Context class #######################################################


# get rounding method function:
rounding_functions = [name for name in Decimal.__dict__.keys()
                                    if name.startswith('_round_')]
for name in rounding_functions:
    # name is like _round_half_even, goes to the global ROUND_HALF_EVEN value.
    globalname = name[1:].upper()
    val = globals()[globalname]
    Decimal._pick_rounding_function[val] = name

del name, val, globalname, rounding_functions

class _ContextManager(object):
    """Context manager class to support localcontext().

      Sets a copy of the supplied context in __enter__() and restores
      the previous decimal context in __exit__()
    """
    def __init__(self, new_context):
        self.new_context = new_context.copy()
    def __enter__(self):
        self.saved_context = getcontext()
        setcontext(self.new_context)
        return self.new_context
    def __exit__(self, t, v, tb):
        setcontext(self.saved_context)

class Context(object):
    """Contains the context for a Decimal instance.

    Contains:
    prec - precision (for use in rounding, division, square roots..)
    rounding - rounding type (how you round)
    _rounding_decision - ALWAYS_ROUND, NEVER_ROUND -- do you round?
    traps - If traps[exception] = 1, then the exception is
                    raised when it is caused.  Otherwise, a value is
                    substituted in.
    flags  - When an exception is caused, flags[exception] is incremented.
             (Whether or not the trap_enabler is set)
             Should be reset by user of Decimal instance.
    Emin -   Minimum exponent
    Emax -   Maximum exponent
    capitals -      If 1, 1*10^1 is printed as 1E+1.
                    If 0, printed as 1e1
    _clamp - If 1, change exponents if too high (Default 0)
    """

    def __init__(self, prec=None, rounding=None,
                 traps=None, flags=None,
                 _rounding_decision=None,
                 Emin=None, Emax=None,
                 capitals=None, _clamp=0,
                 _ignored_flags=None):
        if flags is None:
            flags = []
        if _ignored_flags is None:
            _ignored_flags = []
        if not isinstance(flags, dict):
            flags = dict([(s,s in flags) for s in _signals])
            del s
        if traps is not None and not isinstance(traps, dict):
            traps = dict([(s,s in traps) for s in _signals])
            del s
        for name, val in locals().items():
            if val is None:
                setattr(self, name, _copy.copy(getattr(DefaultContext, name)))
            else:
                setattr(self, name, val)
        del self.self

    def __repr__(self):
        """Show the current context."""
        s = []
        s.append('Context(prec=%(prec)d, rounding=%(rounding)s, '
                 'Emin=%(Emin)d, Emax=%(Emax)d, capitals=%(capitals)d'
                 % vars(self))
        names = [f.__name__ for f, v in self.flags.items() if v]
        s.append('flags=[' + ', '.join(names) + ']')
        names = [t.__name__ for t, v in self.traps.items() if v]
        s.append('traps=[' + ', '.join(names) + ']')
        return ', '.join(s) + ')'

    def clear_flags(self):
        """Reset all flags to zero"""
        for flag in self.flags:
            self.flags[flag] = 0

    def _shallow_copy(self):
        """Returns a shallow copy from self."""
        nc = Context(self.prec, self.rounding, self.traps, self.flags,
                         self._rounding_decision, self.Emin, self.Emax,
                         self.capitals, self._clamp, self._ignored_flags)
        return nc

    def copy(self):
        """Returns a deep copy from self."""
        nc = Context(self.prec, self.rounding, self.traps.copy(),
                self.flags.copy(), self._rounding_decision, self.Emin,
                self.Emax, self.capitals, self._clamp, self._ignored_flags)
        return nc
    __copy__ = copy

    def _raise_error(self, condition, explanation = None, *args):
        """Handles an error

        If the flag is in _ignored_flags, returns the default response.
        Otherwise, it increments the flag, then, if the corresponding
        trap_enabler is set, it reaises the exception.  Otherwise, it returns
        the default value after incrementing the flag.
        """
        error = _condition_map.get(condition, condition)
        if error in self._ignored_flags:
            # Don't touch the flag
            return error().handle(self, *args)

        self.flags[error] += 1
        if not self.traps[error]:
            # The errors define how to handle themselves.
            return condition().handle(self, *args)

        # Errors should only be risked on copies of the context
        # self._ignored_flags = []
        raise error, explanation

    def _ignore_all_flags(self):
        """Ignore all flags, if they are raised"""
        return self._ignore_flags(*_signals)

    def _ignore_flags(self, *flags):
        """Ignore the flags, if they are raised"""
        # Do not mutate-- This way, copies of a context leave the original
        # alone.
        self._ignored_flags = (self._ignored_flags + list(flags))
        return list(flags)

    def _regard_flags(self, *flags):
        """Stop ignoring the flags, if they are raised"""
        if flags and isinstance(flags[0], (tuple,list)):
            flags = flags[0]
        for flag in flags:
            self._ignored_flags.remove(flag)

    def __hash__(self):
        """A Context cannot be hashed."""
        # We inherit object.__hash__, so we must deny this explicitly
        raise TypeError("Cannot hash a Context.")

    def Etiny(self):
        """Returns Etiny (= Emin - prec + 1)"""
        return int(self.Emin - self.prec + 1)

    def Etop(self):
        """Returns maximum exponent (= Emax - prec + 1)"""
        return int(self.Emax - self.prec + 1)

    def _set_rounding_decision(self, type):
        """Sets the rounding decision.

        Sets the rounding decision, and returns the current (previous)
        rounding decision.  Often used like:

        context = context._shallow_copy()
        # That so you don't change the calling context
        # if an error occurs in the middle (say DivisionImpossible is raised).

        rounding = context._set_rounding_decision(NEVER_ROUND)
        instance = instance / Decimal(2)
        context._set_rounding_decision(rounding)

        This will make it not round for that operation.
        """

        rounding = self._rounding_decision
        self._rounding_decision = type
        return rounding

    def _set_rounding(self, type):
        """Sets the rounding type.

        Sets the rounding type, and returns the current (previous)
        rounding type.  Often used like:

        context = context.copy()
        # so you don't change the calling context
        # if an error occurs in the middle.
        rounding = context._set_rounding(ROUND_UP)
        val = self.__sub__(other, context=context)
        context._set_rounding(rounding)

        This will make it round up for that operation.
        """
        rounding = self.rounding
        self.rounding= type
        return rounding

    def create_decimal(self, num='0'):
        """Creates a new Decimal instance but using self as context."""
        d = Decimal(num, context=self)
        return d._fix(self)

    # Methods
    def abs(self, a):
        """Returns the absolute value of the operand.

        If the operand is negative, the result is the same as using the minus
        operation on the operand.  Otherwise, the result is the same as using
        the plus operation on the operand.

        >>> ExtendedContext.abs(Decimal('2.1'))
        Decimal("2.1")
        >>> ExtendedContext.abs(Decimal('-100'))
        Decimal("100")
        >>> ExtendedContext.abs(Decimal('101.5'))
        Decimal("101.5")
        >>> ExtendedContext.abs(Decimal('-101.5'))
        Decimal("101.5")
        """
        return a.__abs__(context=self)

    def add(self, a, b):
        """Return the sum of the two operands.

        >>> ExtendedContext.add(Decimal('12'), Decimal('7.00'))
        Decimal("19.00")
        >>> ExtendedContext.add(Decimal('1E+2'), Decimal('1.01E+4'))
        Decimal("1.02E+4")
        """
        return a.__add__(b, context=self)

    def _apply(self, a):
        return str(a._fix(self))

    def canonical(self, a):
        """Returns the same Decimal object.

        As we do not have different encodings for the same number, the
        received object already is in its canonical form.

        >>> ExtendedContext.canonical(Decimal('2.50'))
        Decimal("2.50")
        """
        return a.canonical(context=self)

    def compare(self, a, b):
        """Compares values numerically.

        If the signs of the operands differ, a value representing each operand
        ('-1' if the operand is less than zero, '0' if the operand is zero or
        negative zero, or '1' if the operand is greater than zero) is used in
        place of that operand for the comparison instead of the actual
        operand.

        The comparison is then effected by subtracting the second operand from
        the first and then returning a value according to the result of the
        subtraction: '-1' if the result is less than zero, '0' if the result is
        zero or negative zero, or '1' if the result is greater than zero.

        >>> ExtendedContext.compare(Decimal('2.1'), Decimal('3'))
        Decimal("-1")
        >>> ExtendedContext.compare(Decimal('2.1'), Decimal('2.1'))
        Decimal("0")
        >>> ExtendedContext.compare(Decimal('2.1'), Decimal('2.10'))
        Decimal("0")
        >>> ExtendedContext.compare(Decimal('3'), Decimal('2.1'))
        Decimal("1")
        >>> ExtendedContext.compare(Decimal('2.1'), Decimal('-3'))
        Decimal("1")
        >>> ExtendedContext.compare(Decimal('-3'), Decimal('2.1'))
        Decimal("-1")
        """
        return a.compare(b, context=self)

    def compare_signal(self, a, b):
        """Compares the values of the two operands numerically.

        It's pretty much like compare(), but all NaNs signal, with signaling
        NaNs taking precedence over quiet NaNs.
        """
        return a.compare_signal(b, context=self)

    def compare_total(self, a, b):
        """Compares two operands using their abstract representation.

        This is not like the standard compare, which use their numerical
        value. Note that a total ordering is defined for all possible abstract
        representations.

        >>> ExtendedContext.compare_total(Decimal('12.73'), Decimal('127.9'))
        Decimal("-1")
        >>> ExtendedContext.compare_total(Decimal('-127'),  Decimal('12'))
        Decimal("-1")
        >>> ExtendedContext.compare_total(Decimal('12.30'), Decimal('12.3'))
        Decimal("-1")
        >>> ExtendedContext.compare_total(Decimal('12.30'), Decimal('12.30'))
        Decimal("0")
        >>> ExtendedContext.compare_total(Decimal('12.3'),  Decimal('12.300'))
        Decimal("1")
        >>> ExtendedContext.compare_total(Decimal('12.3'),  Decimal('NaN'))
        Decimal("-1")
        """
        return a.compare_total(b, context=self)

    def compare_total_mag(self, a, b):
        """Compares two operands using their abstract representation ignoring sign.

        Like compare_total, but with operand's sign ignored and assumed to be 0.
        """
        return a.compare_total_mag(b)

    def copy_abs(self, a):
        """Returns a copy of the operand with the sign set to 0.

        >>> ExtendedContext.copy_abs(Decimal('2.1'))
        Decimal("2.1")
        >>> ExtendedContext.copy_abs(Decimal('-100'))
        Decimal("100")
        """
        return a.copy_abs()

    def copy_decimal(self, a):
        """Returns a copy of the decimal objet.

        >>> ExtendedContext.copy_decimal(Decimal('2.1'))
        Decimal("2.1")
        >>> ExtendedContext.copy_decimal(Decimal('-1.00'))
        Decimal("-1.00")
        """
        return a

    def copy_negate(self, a):
        """Returns a copy of the operand with the sign inverted.

        >>> ExtendedContext.copy_negate(Decimal('101.5'))
        Decimal("-101.5")
        >>> ExtendedContext.copy_negate(Decimal('-101.5'))
        Decimal("101.5")
        """
        return a.copy_negate(context=self)

    def copy_sign(self, a, b):
        """Copies the second operand's sign to the first one.

        In detail, it returns a copy of the first operand with the sign
        equal to the sign of the second operand.

        >>> ExtendedContext.copy_sign(Decimal( '1.50'), Decimal('7.33'))
        Decimal("1.50")
        >>> ExtendedContext.copy_sign(Decimal('-1.50'), Decimal('7.33'))
        Decimal("1.50")
        >>> ExtendedContext.copy_sign(Decimal( '1.50'), Decimal('-7.33'))
        Decimal("-1.50")
        >>> ExtendedContext.copy_sign(Decimal('-1.50'), Decimal('-7.33'))
        Decimal("-1.50")
        """
        return a.copy_sign(b, context=self)

    def divide(self, a, b):
        """Decimal division in a specified context.

        >>> ExtendedContext.divide(Decimal('1'), Decimal('3'))
        Decimal("0.333333333")
        >>> ExtendedContext.divide(Decimal('2'), Decimal('3'))
        Decimal("0.666666667")
        >>> ExtendedContext.divide(Decimal('5'), Decimal('2'))
        Decimal("2.5")
        >>> ExtendedContext.divide(Decimal('1'), Decimal('10'))
        Decimal("0.1")
        >>> ExtendedContext.divide(Decimal('12'), Decimal('12'))
        Decimal("1")
        >>> ExtendedContext.divide(Decimal('8.00'), Decimal('2'))
        Decimal("4.00")
        >>> ExtendedContext.divide(Decimal('2.400'), Decimal('2.0'))
        Decimal("1.20")
        >>> ExtendedContext.divide(Decimal('1000'), Decimal('100'))
        Decimal("10")
        >>> ExtendedContext.divide(Decimal('1000'), Decimal('1'))
        Decimal("1000")
        >>> ExtendedContext.divide(Decimal('2.40E+6'), Decimal('2'))
        Decimal("1.20E+6")
        """
        return a.__div__(b, context=self)

    def divide_int(self, a, b):
        """Divides two numbers and returns the integer part of the result.

        >>> ExtendedContext.divide_int(Decimal('2'), Decimal('3'))
        Decimal("0")
        >>> ExtendedContext.divide_int(Decimal('10'), Decimal('3'))
        Decimal("3")
        >>> ExtendedContext.divide_int(Decimal('1'), Decimal('0.3'))
        Decimal("3")
        """
        return a.__floordiv__(b, context=self)

    def divmod(self, a, b):
        return a.__divmod__(b, context=self)

    def exp(self, a):
        """Returns e ** a.

        >>> ExtendedContext.exp(Decimal('-Infinity'))
        Decimal("0")
        >>> ExtendedContext.exp(Decimal('-1'))
        Decimal("0.367879441")
        >>> ExtendedContext.exp(Decimal('0'))
        Decimal("1")
        >>> ExtendedContext.exp(Decimal('1'))
        Decimal("2.71828183")
        >>> ExtendedContext.exp(Decimal('0.693147181'))
        Decimal("2.00000000")
        >>> ExtendedContext.exp(Decimal('+Infinity'))
        Decimal("Inf")
        """
        return a.exp(context=self)

    def fma(self, a, b, c):
        """Returns a multiplied by b, plus c.

        The first two operands are multiplied together, using multiply,
        the third operand is then added to the result of that
        multiplication, using add, all with only one final rounding.

        >>> ExtendedContext.fma(Decimal('3'), Decimal('5'), Decimal('7'))
        Decimal("22")
        >>> ExtendedContext.fma(Decimal('3'), Decimal('-5'), Decimal('7'))
        Decimal("-8")
        >>> ExtendedContext.fma(Decimal('888565290'), Decimal('1557.96930'), Decimal('-86087.7578'))
        Decimal("1.38435736E+12")
        """
        return a.fma(b, c, context=self)

    def is_canonical(self, a):
        """Returns 1 if the operand is canonical; otherwise returns 0.

        >>> ExtendedContext.is_canonical(Decimal('2.50'))
        Decimal("1")
        """
        return Decimal(1)

    def is_finite(self, a):
        """Returns 1 if the operand is finite, otherwise returns 0.

        For it to be finite, it must be neither infinite nor a NaN.

        >>> ExtendedContext.is_finite(Decimal('2.50'))
        Decimal("1")
        >>> ExtendedContext.is_finite(Decimal('-0.3'))
        Decimal("1")
        >>> ExtendedContext.is_finite(Decimal('0'))
        Decimal("1")
        >>> ExtendedContext.is_finite(Decimal('Inf'))
        Decimal("0")
        >>> ExtendedContext.is_finite(Decimal('NaN'))
        Decimal("0")
        """
        return a.is_finite(context=self)

    def is_infinite(self, a):
        """Returns 1 if the operand is an Infinite, otherwise returns 0.

        >>> ExtendedContext.is_infinite(Decimal('2.50'))
        Decimal("0")
        >>> ExtendedContext.is_infinite(Decimal('-Inf'))
        Decimal("1")
        >>> ExtendedContext.is_infinite(Decimal('NaN'))
        Decimal("0")
        """
        return a.is_infinite(context=self)

    def is_nan(self, a):
        """Returns 1 if the operand is qNaN or sNaN, otherwise returns 0.

        >>> ExtendedContext.is_nan(Decimal('2.50'))
        Decimal("0")
        >>> ExtendedContext.is_nan(Decimal('NaN'))
        Decimal("1")
        >>> ExtendedContext.is_nan(Decimal('-sNaN'))
        Decimal("1")
        """
        return a.is_nan(context=self)

    def is_normal(self, a):
        """Returns 1 if the operand is a normal number, otherwise returns 0.

        >>> ExtendedContext.is_normal(Decimal('2.50'))
        Decimal("1")
        >>> ExtendedContext.is_normal(Decimal('0.1E-999'))
        Decimal("0")
        >>> ExtendedContext.is_normal(Decimal('0.00'))
        Decimal("0")
        >>> ExtendedContext.is_normal(Decimal('-Inf'))
        Decimal("0")
        >>> ExtendedContext.is_normal(Decimal('NaN'))
        Decimal("0")
        """
        return a.is_normal(context=self)

    def is_qnan(self, a):
        """Returns 1 if the operand is a quiet NaN, otherwise returns 0.

        >>> ExtendedContext.is_qnan(Decimal('2.50'))
        Decimal("0")
        >>> ExtendedContext.is_qnan(Decimal('NaN'))
        Decimal("1")
        >>> ExtendedContext.is_qnan(Decimal('sNaN'))
        Decimal("0")
        """
        return a.is_qnan(context=self)

    def is_signed(self, a):
        """Returns 1 if the operand is negative, otherwise returns 0.

        >>> ExtendedContext.is_signed(Decimal('2.50'))
        Decimal("0")
        >>> ExtendedContext.is_signed(Decimal('-12'))
        Decimal("1")
        >>> ExtendedContext.is_signed(Decimal('-0'))
        Decimal("1")
        """
        return a.is_signed(context=self)

    def is_snan(self, a):
        """Returns 1 if the operand is a signaling NaN, otherwise returns 0.

        >>> ExtendedContext.is_snan(Decimal('2.50'))
        Decimal("0")
        >>> ExtendedContext.is_snan(Decimal('NaN'))
        Decimal("0")
        >>> ExtendedContext.is_snan(Decimal('sNaN'))
        Decimal("1")
        """
        return a.is_snan(context=self)

    def is_subnormal(self, a):
        """Returns 1 if the operand is subnormal, otherwise returns 0.

        >>> ExtendedContext.is_subnormal(Decimal('2.50'))
        Decimal("0")
        >>> ExtendedContext.is_subnormal(Decimal('0.1E-999'))
        Decimal("1")
        >>> ExtendedContext.is_subnormal(Decimal('0.00'))
        Decimal("0")
        >>> ExtendedContext.is_subnormal(Decimal('-Inf'))
        Decimal("0")
        >>> ExtendedContext.is_subnormal(Decimal('NaN'))
        Decimal("0")
        """
        return a.is_subnormal(context=self)

    def is_zero(self, a):
        """Returns 1 if the operand is a zero, otherwise returns 0.

        >>> ExtendedContext.is_zero(Decimal('0'))
        Decimal("1")
        >>> ExtendedContext.is_zero(Decimal('2.50'))
        Decimal("0")
        >>> ExtendedContext.is_zero(Decimal('-0E+2'))
        Decimal("1")
        """
        return a.is_zero(context=self)

    def ln(self, a):
        """Returns the natural (base e) logarithm of the operand.

        >>> ExtendedContext.ln(Decimal('0'))
        Decimal("-Inf")
        >>> ExtendedContext.ln(Decimal('1.000'))
        Decimal("0")
        >>> ExtendedContext.ln(Decimal('2.71828183'))
        Decimal("1.00000000")
        >>> ExtendedContext.ln(Decimal('10'))
        Decimal("2.30258509")
        >>> ExtendedContext.ln(Decimal('+Infinity'))
        Decimal("Inf")
        """
        return a.ln(context=self)

    def log10(self, a):
        """Returns the base 10 logarithm of the operand.

        >>> ExtendedContext.log10(Decimal('0'))
        Decimal("-In")
        >>> ExtendedContext.log10(Decimal('0.001'))
        Decimal("-3")
        >>> ExtendedContext.log10(Decimal('1.000'))
        Decimal("0")
        >>> ExtendedContext.log10(Decimal('2'))
        Decimal("0.301029996")
        >>> ExtendedContext.log10(Decimal('10'))
        Decimal("1")
        >>> ExtendedContext.log10(Decimal('70'))
        Decimal("1.84509804")
        >>> ExtendedContext.log10(Decimal('+Infinity'))
        Decimal("Inf")
        """
        return a.log10(context=self)

    def logb(self, a):
        """ Returns the exponent of the magnitude of the operand's MSD.

        The result is the integer which is the exponent of the magnitude
        of the most significant digit of the operand (as though the
        operand were truncated to a single digit while maintaining the
        value of that digit and without limiting the resulting exponent).

        >>> ExtendedContext.logb(Decimal('250'))
        Decimal("2")
        >>> ExtendedContext.logb(Decimal('2.50'))
        Decimal("0")
        >>> ExtendedContext.logb(Decimal('0.03'))
        Decimal("-2")
        >>> ExtendedContext.logb(Decimal('0'))
        Decimal("-Inf")
        """
        return a.logb(context=self)

    def logical_and(self, a, b):
        """Applies the logical operation 'and' between each operand's digits.

        The operands must be both logical numbers.

        >>> ExtendedContext.logical_and(Decimal('0'), Decimal('0'))
        Decimal("0")
        >>> ExtendedContext.logical_and(Decimal('0'), Decimal('1'))
        Decimal("0")
        >>> ExtendedContext.logical_and(Decimal('1'), Decimal('0'))
        Decimal("0")
        >>> ExtendedContext.logical_and(Decimal('1'), Decimal('1'))
        Decimal("1")
        >>> ExtendedContext.logical_and(Decimal('1100'), Decimal('1010'))
        Decimal("1000")
        >>> ExtendedContext.logical_and(Decimal('1111'), Decimal('10'))
        Decimal("10")
        """
        return a.logical_and(b, context=self)

    def logical_invert(self, a):
        """Invert all the digits in the operand.

        The operand must be a logical number.

        >>> ExtendedContext.logical_invert(Decimal('0'))
        Decimal("111111111")
        >>> ExtendedContext.logical_invert(Decimal('1'))
        Decimal("111111110")
        >>> ExtendedContext.logical_invert(Decimal('111111111'))
        Decimal("0")
        >>> ExtendedContext.logical_invert(Decimal('101010101'))
        Decimal("10101010")
        """
        return a.logical_invert(context=self)

    def logical_or(self, a, b):
        """Applies the logical operation 'or' between each operand's digits.

        The operands must be both logical numbers.

        >>> ExtendedContext.logical_or(Decimal('0'), Decimal('0'))
        Decimal("0")
        >>> ExtendedContext.logical_or(Decimal('0'), Decimal('1'))
        Decimal("1")
        >>> ExtendedContext.logical_or(Decimal('1'), Decimal('0'))
        Decimal("1")
        >>> ExtendedContext.logical_or(Decimal('1'), Decimal('1'))
        Decimal("1")
        >>> ExtendedContext.logical_or(Decimal('1100'), Decimal('1010'))
        Decimal("1110")
        >>> ExtendedContext.logical_or(Decimal('1110'), Decimal('10'))
        Decimal("1110")
        """
        return a.logical_or(b, context=self)

    def logical_xor(self, a, b):
        """Applies the logical operation 'xor' between each operand's digits.

        The operands must be both logical numbers.

        >>> ExtendedContext.logical_xor(Decimal('0'), Decimal('0'))
        Decimal("0")
        >>> ExtendedContext.logical_xor(Decimal('0'), Decimal('1'))
        Decimal("1")
        >>> ExtendedContext.logical_xor(Decimal('1'), Decimal('0'))
        Decimal("1")
        >>> ExtendedContext.logical_xor(Decimal('1'), Decimal('1'))
        Decimal("0")
        >>> ExtendedContext.logical_xor(Decimal('1100'), Decimal('1010'))
        Decimal("110")
        >>> ExtendedContext.logical_xor(Decimal('1111'), Decimal('10'))
        Decimal("1101")
        """
        return a.logical_xor(b, context=self)

    def max(self, a,b):
        """max compares two values numerically and returns the maximum.

        If either operand is a NaN then the general rules apply.
        Otherwise, the operands are compared as as though by the compare
        operation.  If they are numerically equal then the left-hand operand
        is chosen as the result.  Otherwise the maximum (closer to positive
        infinity) of the two operands is chosen as the result.

        >>> ExtendedContext.max(Decimal('3'), Decimal('2'))
        Decimal("3")
        >>> ExtendedContext.max(Decimal('-10'), Decimal('3'))
        Decimal("3")
        >>> ExtendedContext.max(Decimal('1.0'), Decimal('1'))
        Decimal("1")
        >>> ExtendedContext.max(Decimal('7'), Decimal('NaN'))
        Decimal("7")
        """
        return a.max(b, context=self)

    def max_mag(self, a, b):
        """Compares the values numerically with their sign ignored."""
        return a.max_mag(b, context=self)

    def min(self, a,b):
        """min compares two values numerically and returns the minimum.

        If either operand is a NaN then the general rules apply.
        Otherwise, the operands are compared as as though by the compare
        operation.  If they are numerically equal then the left-hand operand
        is chosen as the result.  Otherwise the minimum (closer to negative
        infinity) of the two operands is chosen as the result.

        >>> ExtendedContext.min(Decimal('3'), Decimal('2'))
        Decimal("2")
        >>> ExtendedContext.min(Decimal('-10'), Decimal('3'))
        Decimal("-10")
        >>> ExtendedContext.min(Decimal('1.0'), Decimal('1'))
        Decimal("1.0")
        >>> ExtendedContext.min(Decimal('7'), Decimal('NaN'))
        Decimal("7")
        """
        return a.min(b, context=self)

    def min_mag(self, a, b):
        """Compares the values numerically with their sign ignored."""
        return a.min_mag(b, context=self)

    def minus(self, a):
        """Minus corresponds to unary prefix minus in Python.

        The operation is evaluated using the same rules as subtract; the
        operation minus(a) is calculated as subtract('0', a) where the '0'
        has the same exponent as the operand.

        >>> ExtendedContext.minus(Decimal('1.3'))
        Decimal("-1.3")
        >>> ExtendedContext.minus(Decimal('-1.3'))
        Decimal("1.3")
        """
        return a.__neg__(context=self)

    def multiply(self, a, b):
        """multiply multiplies two operands.

        If either operand is a special value then the general rules apply.
        Otherwise, the operands are multiplied together ('long multiplication'),
        resulting in a number which may be as long as the sum of the lengths
        of the two operands.

        >>> ExtendedContext.multiply(Decimal('1.20'), Decimal('3'))
        Decimal("3.60")
        >>> ExtendedContext.multiply(Decimal('7'), Decimal('3'))
        Decimal("21")
        >>> ExtendedContext.multiply(Decimal('0.9'), Decimal('0.8'))
        Decimal("0.72")
        >>> ExtendedContext.multiply(Decimal('0.9'), Decimal('-0'))
        Decimal("-0.0")
        >>> ExtendedContext.multiply(Decimal('654321'), Decimal('654321'))
        Decimal("4.28135971E+11")
        """
        return a.__mul__(b, context=self)

    def next_minus(self, a):
        """Returns the largest representable number smaller than a.

        >>> c = ExtendedContext.copy()
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> ExtendedContext.next_minus(Decimal('1'))
        Decimal("0.999999999")
        >>> c.next_minus(Decimal('1E-1007'))
        Decimal("0E-1007")
        >>> ExtendedContext.next_minus(Decimal('-1.00000003'))
        Decimal("-1.00000004")
        >>> c.next_minus(Decimal('Infinity'))
        Decimal("9.99999999E+999")
        """
        return a.next_minus(context=self)

    def next_plus(self, a):
        """Returns the smallest representable number larger than a.

        >>> c = ExtendedContext.copy()
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> ExtendedContext.next_plus(Decimal('1'))
        Decimal("1.00000001")
        >>> c.next_plus(Decimal('-1E-1007'))
        Decimal("-0E-1007")
        >>> ExtendedContext.next_plus(Decimal('-1.00000003'))
        Decimal("-1.00000002")
        >>> c.next_plus(Decimal('-Infinity'))
        Decimal("-9.99999999E+999")
        """
        return a.next_plus(context=self)

    def next_toward(self, a, b):
        """Returns the number closest to a, in direction towards b.

        The result is the closest representable number from the first
        operand (but not the first operand) that is in the direction
        towards the second operand, unless the operands have the same
        value.

        >>> ExtendedContext.next_toward(Decimal('1'), Decimal('2'))
        Decimal("1.00000001")
        >>> ExtendedContext.next_toward(Decimal('-1E-1007'), Decimal('1'))
        Decimal("-0E-1007")
        >>> ExtendedContext.next_toward(Decimal('-1.00000003'), Decimal('0'))
        Decimal("-1.00000002")
        >>> ExtendedContext.next_toward(Decimal('1'), Decimal('0'))
        Decimal("0.999999999")
        >>> ExtendedContext.next_toward(Decimal('1E-1007'), Decimal('-100'))
        Decimal("0E-1007")
        >>> ExtendedContext.next_toward(Decimal('-1.00000003'), Decimal('-10'))
        Decimal("-1.00000004")
        >>> ExtendedContext.next_toward(Decimal('0.00'), Decimal('-0.0000'))
        Decimal("-0.00")
        """
        return a.next_toward(b, context=self)

    def normalize(self, a):
        """normalize reduces an operand to its simplest form.

        Essentially a plus operation with all trailing zeros removed from the
        result.

        >>> ExtendedContext.normalize(Decimal('2.1'))
        Decimal("2.1")
        >>> ExtendedContext.normalize(Decimal('-2.0'))
        Decimal("-2")
        >>> ExtendedContext.normalize(Decimal('1.200'))
        Decimal("1.2")
        >>> ExtendedContext.normalize(Decimal('-120'))
        Decimal("-1.2E+2")
        >>> ExtendedContext.normalize(Decimal('120.00'))
        Decimal("1.2E+2")
        >>> ExtendedContext.normalize(Decimal('0.00'))
        Decimal("0")
        """
        return a.normalize(context=self)

    def number_class(self, a):
        """Returns an indication of the class of the operand.

        The class is one of the following strings:
          -sNaN
          -NaN
          -Infinity
          -Normal
          -Subnormal
          -Zero
          +Zero
          +Subnormal
          +Normal
          +Infinity

        >>> c = Context(ExtendedContext)
        >>> c.Emin = -999
        >>> c.Emax = 999
        >>> c.number_class(Decimal('Infinity'))
        '+Infinity'
        >>> c.number_class(Decimal('1E-10'))
        '+Normal'
        >>> c.number_class(Decimal('2.50'))
        '+Normal'
        >>> c.number_class(Decimal('0.1E-999'))
        '+Subnormal'
        >>> c.number_class(Decimal('0'))
        '+Zero'
        >>> c.number_class(Decimal('-0'))
        '-Zero'
        >>> c.number_class(Decimal('-0.1E-999'))
        '-Subnormal'
        >>> c.number_class(Decimal('-1E-10'))
        '-Normal'
        >>> c.number_class(Decimal('-2.50'))
        '-Normal'
        >>> c.number_class(Decimal('-Infinity'))
        '-Infinity'
        >>> c.number_class(Decimal('NaN'))
        'NaN'
        >>> c.number_class(Decimal('-NaN'))
        'NaN'
        >>> c.number_class(Decimal('sNaN'))
        'sNaN'
        """
        return a.number_class(context=self)

    def plus(self, a):
        """Plus corresponds to unary prefix plus in Python.

        The operation is evaluated using the same rules as add; the
        operation plus(a) is calculated as add('0', a) where the '0'
        has the same exponent as the operand.

        >>> ExtendedContext.plus(Decimal('1.3'))
        Decimal("1.3")
        >>> ExtendedContext.plus(Decimal('-1.3'))
        Decimal("-1.3")
        """
        return a.__pos__(context=self)

    def power(self, a, b, modulo=None):
        """Raises a to the power of b, to modulo if given.

        The right-hand operand must be a whole number whose integer part (after
        any exponent has been applied) has no more than 9 digits and whose
        fractional part (if any) is all zeros before any rounding.  The operand
        may be positive, negative, or zero; if negative, the absolute value of
        the power is used, and the left-hand operand is inverted (divided into
        1) before use.

        If the increased precision needed for the intermediate calculations
        exceeds the capabilities of the implementation then an Invalid
        operation condition is raised.

        If, when raising to a negative power, an underflow occurs during the
        division into 1, the operation is not halted at that point but
        continues.

        >>> ExtendedContext.power(Decimal('2'), Decimal('3'))
        Decimal("8")
        >>> ExtendedContext.power(Decimal('2'), Decimal('-3'))
        Decimal("0.125")
        >>> ExtendedContext.power(Decimal('1.7'), Decimal('8'))
        Decimal("69.7575744")
        >>> ExtendedContext.power(Decimal('Infinity'), Decimal('-2'))
        Decimal("0")
        >>> ExtendedContext.power(Decimal('Infinity'), Decimal('-1'))
        Decimal("0")
        >>> ExtendedContext.power(Decimal('Infinity'), Decimal('0'))
        Decimal("1")
        >>> ExtendedContext.power(Decimal('Infinity'), Decimal('1'))
        Decimal("Infinity")
        >>> ExtendedContext.power(Decimal('Infinity'), Decimal('2'))
        Decimal("Infinity")
        >>> ExtendedContext.power(Decimal('-Infinity'), Decimal('-2'))
        Decimal("0")
        >>> ExtendedContext.power(Decimal('-Infinity'), Decimal('-1'))
        Decimal("-0")
        >>> ExtendedContext.power(Decimal('-Infinity'), Decimal('0'))
        Decimal("1")
        >>> ExtendedContext.power(Decimal('-Infinity'), Decimal('1'))
        Decimal("-Infinity")
        >>> ExtendedContext.power(Decimal('-Infinity'), Decimal('2'))
        Decimal("Infinity")
        >>> ExtendedContext.power(Decimal('0'), Decimal('0'))
        Decimal("NaN")
        """
        return a.__pow__(b, modulo, context=self)

    def quantize(self, a, b):
        """Returns a value equal to 'a' (rounded), having the exponent of 'b'.

        The coefficient of the result is derived from that of the left-hand
        operand.  It may be rounded using the current rounding setting (if the
        exponent is being increased), multiplied by a positive power of ten (if
        the exponent is being decreased), or is unchanged (if the exponent is
        already equal to that of the right-hand operand).

        Unlike other operations, if the length of the coefficient after the
        quantize operation would be greater than precision then an Invalid
        operation condition is raised.  This guarantees that, unless there is
        an error condition, the exponent of the result of a quantize is always
        equal to that of the right-hand operand.

        Also unlike other operations, quantize will never raise Underflow, even
        if the result is subnormal and inexact.

        >>> ExtendedContext.quantize(Decimal('2.17'), Decimal('0.001'))
        Decimal("2.170")
        >>> ExtendedContext.quantize(Decimal('2.17'), Decimal('0.01'))
        Decimal("2.17")
        >>> ExtendedContext.quantize(Decimal('2.17'), Decimal('0.1'))
        Decimal("2.2")
        >>> ExtendedContext.quantize(Decimal('2.17'), Decimal('1e+0'))
        Decimal("2")
        >>> ExtendedContext.quantize(Decimal('2.17'), Decimal('1e+1'))
        Decimal("0E+1")
        >>> ExtendedContext.quantize(Decimal('-Inf'), Decimal('Infinity'))
        Decimal("-Infinity")
        >>> ExtendedContext.quantize(Decimal('2'), Decimal('Infinity'))
        Decimal("NaN")
        >>> ExtendedContext.quantize(Decimal('-0.1'), Decimal('1'))
        Decimal("-0")
        >>> ExtendedContext.quantize(Decimal('-0'), Decimal('1e+5'))
        Decimal("-0E+5")
        >>> ExtendedContext.quantize(Decimal('+35236450.6'), Decimal('1e-2'))
        Decimal("NaN")
        >>> ExtendedContext.quantize(Decimal('-35236450.6'), Decimal('1e-2'))
        Decimal("NaN")
        >>> ExtendedContext.quantize(Decimal('217'), Decimal('1e-1'))
        Decimal("217.0")
        >>> ExtendedContext.quantize(Decimal('217'), Decimal('1e-0'))
        Decimal("217")
        >>> ExtendedContext.quantize(Decimal('217'), Decimal('1e+1'))
        Decimal("2.2E+2")
        >>> ExtendedContext.quantize(Decimal('217'), Decimal('1e+2'))
        Decimal("2E+2")
        """
        return a.quantize(b, context=self)

    def radix(self):
        """Just returns 10, as this is Decimal, :)

        >>> ExtendedContext.radix()
        Decimal("10")
        """
        return Decimal(10)

    def remainder(self, a, b):
        """Returns the remainder from integer division.

        The result is the residue of the dividend after the operation of
        calculating integer division as described for divide-integer, rounded
        to precision digits if necessary.  The sign of the result, if
        non-zero, is the same as that of the original dividend.

        This operation will fail under the same conditions as integer division
        (that is, if integer division on the same two operands would fail, the
        remainder cannot be calculated).

        >>> ExtendedContext.remainder(Decimal('2.1'), Decimal('3'))
        Decimal("2.1")
        >>> ExtendedContext.remainder(Decimal('10'), Decimal('3'))
        Decimal("1")
        >>> ExtendedContext.remainder(Decimal('-10'), Decimal('3'))
        Decimal("-1")
        >>> ExtendedContext.remainder(Decimal('10.2'), Decimal('1'))
        Decimal("0.2")
        >>> ExtendedContext.remainder(Decimal('10'), Decimal('0.3'))
        Decimal("0.1")
        >>> ExtendedContext.remainder(Decimal('3.6'), Decimal('1.3'))
        Decimal("1.0")
        """
        return a.__mod__(b, context=self)

    def remainder_near(self, a, b):
        """Returns to be "a - b * n", where n is the integer nearest the exact
        value of "x / b" (if two integers are equally near then the even one
        is chosen).  If the result is equal to 0 then its sign will be the
        sign of a.

        This operation will fail under the same conditions as integer division
        (that is, if integer division on the same two operands would fail, the
        remainder cannot be calculated).

        >>> ExtendedContext.remainder_near(Decimal('2.1'), Decimal('3'))
        Decimal("-0.9")
        >>> ExtendedContext.remainder_near(Decimal('10'), Decimal('6'))
        Decimal("-2")
        >>> ExtendedContext.remainder_near(Decimal('10'), Decimal('3'))
        Decimal("1")
        >>> ExtendedContext.remainder_near(Decimal('-10'), Decimal('3'))
        Decimal("-1")
        >>> ExtendedContext.remainder_near(Decimal('10.2'), Decimal('1'))
        Decimal("0.2")
        >>> ExtendedContext.remainder_near(Decimal('10'), Decimal('0.3'))
        Decimal("0.1")
        >>> ExtendedContext.remainder_near(Decimal('3.6'), Decimal('1.3'))
        Decimal("-0.3")
        """
        return a.remainder_near(b, context=self)

    def rotate(self, a, b):
        """Returns a rotated copy of a, b times.

        The coefficient of the result is a rotated copy of the digits in
        the coefficient of the first operand.  The number of places of
        rotation is taken from the absolute value of the second operand,
        with the rotation being to the left if the second operand is
        positive or to the right otherwise.

        >>> ExtendedContext.rotate(Decimal('34'), Decimal('8'))
        Decimal("400000003")
        >>> ExtendedContext.rotate(Decimal('12'), Decimal('9'))
        Decimal("12")
        >>> ExtendedContext.rotate(Decimal('123456789'), Decimal('-2'))
        Decimal("891234567")
        >>> ExtendedContext.rotate(Decimal('123456789'), Decimal('0'))
        Decimal("123456789")
        >>> ExtendedContext.rotate(Decimal('123456789'), Decimal('+2'))
        Decimal("345678912")
        """
        return a.rotate(b, context=self)

    def same_quantum(self, a, b):
        """Returns True if the two operands have the same exponent.

        The result is never affected by either the sign or the coefficient of
        either operand.

        >>> ExtendedContext.same_quantum(Decimal('2.17'), Decimal('0.001'))
        False
        >>> ExtendedContext.same_quantum(Decimal('2.17'), Decimal('0.01'))
        True
        >>> ExtendedContext.same_quantum(Decimal('2.17'), Decimal('1'))
        False
        >>> ExtendedContext.same_quantum(Decimal('Inf'), Decimal('-Inf'))
        True
        """
        return a.same_quantum(b)

    def scaleb (self, a, b):
        """Returns the first operand after adding the second value its exp.

        >>> ExtendedContext.scaleb(Decimal('7.50'), Decimal('-2'))
        Decimal("0.0750")
        >>> ExtendedContext.scaleb(Decimal('7.50'), Decimal('0'))
        Decimal("7.50")
        >>> ExtendedContext.scaleb(Decimal('7.50'), Decimal('3'))
        Decimal("7.50E+3")
        """
        return a.scaleb (b, context=self)

    def shift(self, a, b):
        """Returns a shifted copy of a, b times.

        The coefficient of the result is a shifted copy of the digits
        in the coefficient of the first operand.  The number of places
        to shift is taken from the absolute value of the second operand,
        with the shift being to the left if the second operand is
        positive or to the right otherwise.  Digits shifted into the
        coefficient are zeros.

        >>> ExtendedContext.shift(Decimal('34'), Decimal('8'))
        Decimal("400000000")
        >>> ExtendedContext.shift(Decimal('12'), Decimal('9'))
        Decimal("0")
        >>> ExtendedContext.shift(Decimal('123456789'), Decimal('-2'))
        Decimal("1234567")
        >>> ExtendedContext.shift(Decimal('123456789'), Decimal('0'))
        Decimal("123456789")
        >>> ExtendedContext.shift(Decimal('123456789'), Decimal('+2'))
        Decimal("345678900")
        """
        return a.shift(b, context=self)

    def sqrt(self, a):
        """Square root of a non-negative number to context precision.

        If the result must be inexact, it is rounded using the round-half-even
        algorithm.

        >>> ExtendedContext.sqrt(Decimal('0'))
        Decimal("0")
        >>> ExtendedContext.sqrt(Decimal('-0'))
        Decimal("-0")
        >>> ExtendedContext.sqrt(Decimal('0.39'))
        Decimal("0.624499800")
        >>> ExtendedContext.sqrt(Decimal('100'))
        Decimal("10")
        >>> ExtendedContext.sqrt(Decimal('1'))
        Decimal("1")
        >>> ExtendedContext.sqrt(Decimal('1.0'))
        Decimal("1.0")
        >>> ExtendedContext.sqrt(Decimal('1.00'))
        Decimal("1.0")
        >>> ExtendedContext.sqrt(Decimal('7'))
        Decimal("2.64575131")
        >>> ExtendedContext.sqrt(Decimal('10'))
        Decimal("3.16227766")
        >>> ExtendedContext.prec
        9
        """
        return a.sqrt(context=self)

    def subtract(self, a, b):
        """Return the difference between the two operands.

        >>> ExtendedContext.subtract(Decimal('1.3'), Decimal('1.07'))
        Decimal("0.23")
        >>> ExtendedContext.subtract(Decimal('1.3'), Decimal('1.30'))
        Decimal("0.00")
        >>> ExtendedContext.subtract(Decimal('1.3'), Decimal('2.07'))
        Decimal("-0.77")
        """
        return a.__sub__(b, context=self)

    def to_eng_string(self, a):
        """Converts a number to a string, using scientific notation.

        The operation is not affected by the context.
        """
        return a.to_eng_string(context=self)

    def to_sci_string(self, a):
        """Converts a number to a string, using scientific notation.

        The operation is not affected by the context.
        """
        if a._exp == 'P':
            a = self._raise_error(ConversionSyntax)
        return a.__str__(context=self)

    def to_integral_exact(self, a):
        """Rounds to an integer.

        When the operand has a negative exponent, the result is the same
        as using the quantize() operation using the given operand as the
        left-hand-operand, 1E+0 as the right-hand-operand, and the precision
        of the operand as the precision setting; Inexact and Rounded flags
        are allowed in this operation.  The rounding mode is taken from the
        context.

        >>> ExtendedContext.to_integral_exact(Decimal('2.1'))
        Decimal("2")
        >>> ExtendedContext.to_integral_exact(Decimal('100'))
        Decimal("100")
        >>> ExtendedContext.to_integral_exact(Decimal('100.0'))
        Decimal("100")
        >>> ExtendedContext.to_integral_exact(Decimal('101.5'))
        Decimal("102")
        >>> ExtendedContext.to_integral_exact(Decimal('-101.5'))
        Decimal("-102")
        >>> ExtendedContext.to_integral_exact(Decimal('10E+5'))
        Decimal("1.0E+6")
        >>> ExtendedContext.to_integral_exact(Decimal('7.89E+77'))
        Decimal("7.89E+77")
        >>> ExtendedContext.to_integral_exact(Decimal('-Inf'))
        Decimal("-Infinity")
        """

    def to_integral_value(self, a):
        """Rounds to an integer.

        When the operand has a negative exponent, the result is the same
        as using the quantize() operation using the given operand as the
        left-hand-operand, 1E+0 as the right-hand-operand, and the precision
        of the operand as the precision setting, except that no flags will
        be set.  The rounding mode is taken from the context.

        >>> ExtendedContext.to_integral_value(Decimal('2.1'))
        Decimal("2")
        >>> ExtendedContext.to_integral_value(Decimal('100'))
        Decimal("100")
        >>> ExtendedContext.to_integral_value(Decimal('100.0'))
        Decimal("100")
        >>> ExtendedContext.to_integral_value(Decimal('101.5'))
        Decimal("102")
        >>> ExtendedContext.to_integral_value(Decimal('-101.5'))
        Decimal("-102")
        >>> ExtendedContext.to_integral_value(Decimal('10E+5'))
        Decimal("1.0E+6")
        >>> ExtendedContext.to_integral_value(Decimal('7.89E+77'))
        Decimal("7.89E+77")
        >>> ExtendedContext.to_integral_value(Decimal('-Inf'))
        Decimal("-Infinity")
        """
        return a.to_integral_value(context=self)

    # the method name changed, but we provide also the old one, for compatibility
    to_integral = to_integral_value

class _WorkRep(object):
    __slots__ = ('sign','int','exp')
    # sign: 0 or 1
    # int:  int or long
    # exp:  None, int, or string

    def __init__(self, value=None):
        if value is None:
            self.sign = None
            self.int = 0
            self.exp = None
        elif isinstance(value, Decimal):
            self.sign = value._sign
            cum = 0
            for digit  in value._int:
                cum = cum * 10 + digit
            self.int = cum
            self.exp = value._exp
        else:
            # assert isinstance(value, tuple)
            self.sign = value[0]
            self.int = value[1]
            self.exp = value[2]

    def __repr__(self):
        return "(%r, %r, %r)" % (self.sign, self.int, self.exp)

    __str__ = __repr__



def _normalize(op1, op2, shouldround = 0, prec = 0):
    """Normalizes op1, op2 to have the same exp and length of coefficient.

    Done during addition.
    """
    # Yes, the exponent is a long, but the difference between exponents
    # must be an int-- otherwise you'd get a big memory problem.
    numdigits = int(op1.exp - op2.exp)
    if numdigits < 0:
        numdigits = -numdigits
        tmp = op2
        other = op1
    else:
        tmp = op1
        other = op2


    if shouldround and numdigits > prec + 1:
        # Big difference in exponents - check the adjusted exponents
        tmp_len = len(str(tmp.int))
        other_len = len(str(other.int))
        if numdigits > (other_len + prec + 1 - tmp_len):
            # If the difference in adjusted exps is > prec+1, we know
            # other is insignificant, so might as well put a 1 after the
            # precision (since this is only for addition).  Also stops
            # use of massive longs.

            extend = prec + 2 - tmp_len
            if extend <= 0:
                extend = 1
            tmp.int *= 10 ** extend
            tmp.exp -= extend
            other.int = 1
            other.exp = tmp.exp
            return op1, op2

    tmp.int *= 10 ** numdigits
    tmp.exp -= numdigits
    return op1, op2

def _adjust_coefficients(op1, op2):
    """Adjust op1, op2 so that op2.int * 10 > op1.int >= op2.int.

    Returns the adjusted op1, op2 as well as the change in op1.exp-op2.exp.

    Used on _WorkRep instances during division.
    """
    adjust = 0
    # If op1 is smaller, make it larger
    while op2.int > op1.int:
        op1.int *= 10
        op1.exp -= 1
        adjust += 1

    # If op2 is too small, make it larger
    while op1.int >= (10 * op2.int):
        op2.int *= 10
        op2.exp -= 1
        adjust -= 1

    return op1, op2, adjust

##### Helper Functions ####################################################

def _convert_other(other):
    """Convert other to Decimal.

    Verifies that it's ok to use in an implicit construction.
    """
    if isinstance(other, Decimal):
        return other
    if isinstance(other, (int, long)):
        return Decimal(other)
    return NotImplemented

_infinity_map = {
    'inf' : 1,
    'infinity' : 1,
    '+inf' : 1,
    '+infinity' : 1,
    '-inf' : -1,
    '-infinity' : -1
}

def _isinfinity(num):
    """Determines whether a string or float is infinity.

    +1 for negative infinity; 0 for finite ; +1 for positive infinity
    """
    num = str(num).lower()
    return _infinity_map.get(num, 0)

def _isnan(num):
    """Determines whether a string or float is NaN

    (1, sign, diagnostic info as string) => NaN
    (2, sign, diagnostic info as string) => sNaN
    0 => not a NaN
    """
    num = str(num).lower()
    if not num:
        return 0

    # Get the sign, get rid of trailing [+-]
    sign = 0
    if num[0] == '+':
        num = num[1:]
    elif num[0] == '-':  # elif avoids '+-nan'
        num = num[1:]
        sign = 1

    if num.startswith('nan'):
        if len(num) > 3 and not num[3:].isdigit():  # diagnostic info
            return 0
        return (1, sign, num[3:].lstrip('0'))
    if num.startswith('snan'):
        if len(num) > 4 and not num[4:].isdigit():
            return 0
        return (2, sign, num[4:].lstrip('0'))
    return 0


##### Setup Specific Contexts ############################################

# The default context prototype used by Context()
# Is mutable, so that new contexts can have different default values

DefaultContext = Context(
        prec=28, rounding=ROUND_HALF_EVEN,
        traps=[DivisionByZero, Overflow, InvalidOperation],
        flags=[],
        _rounding_decision=ALWAYS_ROUND,
        Emax=999999999,
        Emin=-999999999,
        capitals=1
)

# Pre-made alternate contexts offered by the specification
# Don't change these; the user should be able to select these
# contexts and be able to reproduce results from other implementations
# of the spec.

BasicContext = Context(
        prec=9, rounding=ROUND_HALF_UP,
        traps=[DivisionByZero, Overflow, InvalidOperation, Clamped, Underflow],
        flags=[],
)

ExtendedContext = Context(
        prec=9, rounding=ROUND_HALF_EVEN,
        traps=[],
        flags=[],
)


##### Useful Constants (internal use only) ################################

# Reusable defaults
Inf = Decimal('Inf')
negInf = Decimal('-Inf')

# Infsign[sign] is infinity w/ that sign
Infsign = (Inf, negInf)

NaN = Decimal('NaN')

##### crud for parsing strings #############################################
import re

# There's an optional sign at the start, and an optional exponent
# at the end.  The exponent has an optional sign and at least one
# digit.  In between, must have either at least one digit followed
# by an optional fraction, or a decimal point followed by at least
# one digit.  Yuck.

_parser = re.compile(r"""
#    \s*
    (?P<sign>[-+])?
    (
        (?P<int>\d+) (\. (?P<frac>\d*))?
    |
        \. (?P<onlyfrac>\d+)
    )
    ([eE](?P<exp>[-+]? \d+))?
#    \s*
    $
""", re.VERBOSE).match  # Uncomment the \s* to allow leading or trailing spaces.

del re

def _string2exact(s):
    """Return sign, n, p s.t.

    Float string value == -1**sign * n * 10**p exactly
    """
    m = _parser(s)
    if m is None:
        raise ValueError("invalid literal for Decimal: %r" % s)

    if m.group('sign') == "-":
        sign = 1
    else:
        sign = 0

    exp = m.group('exp')
    if exp is None:
        exp = 0
    else:
        exp = int(exp)

    intpart = m.group('int')
    if intpart is None:
        intpart = ""
        fracpart = m.group('onlyfrac')
    else:
        fracpart = m.group('frac')
        if fracpart is None:
            fracpart = ""

    exp -= len(fracpart)

    mantissa = intpart + fracpart
    tmp = map(int, mantissa)
    backup = tmp
    while tmp and tmp[0] == 0:
        del tmp[0]

    # It's a zero
    if not tmp:
        if backup:
            return (sign, tuple(backup), exp)
        return (sign, (0,), exp)
    mantissa = tuple(tmp)

    return (sign, mantissa, exp)


if __name__ == '__main__':
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
