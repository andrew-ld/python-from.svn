# A generic Python debugger base class.
# This class takes care of details of the trace facility;
# a derived class should implement user interaction.
# There are two debuggers based upon this:
# 'pdb', a text-oriented debugger not unlike dbx or gdb;
# and 'wdb', a window-oriented debugger.
# And of course... you can roll your own!

import sys
import types

BdbQuit = 'bdb.BdbQuit' # Exception to give up completely


class Bdb: # Basic Debugger
	
	def __init__(self):
		self.breaks = {}
	
	def reset(self):
		import linecache
		linecache.checkcache()
		self.botframe = None
		self.stopframe = None
		self.returnframe = None
		self.quitting = 0
	
	def trace_dispatch(self, frame, event, arg):
		if self.quitting:
			return # None
		if event == 'line':
			return self.dispatch_line(frame)
		if event == 'call':
			return self.dispatch_call(frame, arg)
		if event == 'return':
			return self.dispatch_return(frame, arg)
		if event == 'exception':
			return self.dispatch_exception(frame, arg)
		print 'bdb.Bdb.dispatch: unknown debugging event:', `event`
		return self.trace_dispatch
	
	def dispatch_line(self, frame):
		if self.stop_here(frame) or self.break_here(frame):
			self.user_line(frame)
			if self.quitting: raise BdbQuit
		return self.trace_dispatch
	
	def dispatch_call(self, frame, arg):
		# XXX 'arg' is no longer used
		if self.botframe is None:
			# First call of dispatch since reset()
			self.botframe = frame
			return self.trace_dispatch
		if not (self.stop_here(frame) or self.break_anywhere(frame)):
			# No need to trace this function
			return # None
		self.user_call(frame, arg)
		if self.quitting: raise BdbQuit
		return self.trace_dispatch
	
	def dispatch_return(self, frame, arg):
		if self.stop_here(frame) or frame == self.returnframe:
			self.user_return(frame, arg)
			if self.quitting: raise BdbQuit
	
	def dispatch_exception(self, frame, arg):
		if self.stop_here(frame):
			self.user_exception(frame, arg)
			if self.quitting: raise BdbQuit
		return self.trace_dispatch
	
	# Normally derived classes don't override the following
	# methods, but they may if they want to redefine the
	# definition of stopping and breakpoints.
	
	def stop_here(self, frame):
		if self.stopframe is None:
			return 1
		if frame is self.stopframe:
			return 1
		while frame is not None and frame is not self.stopframe:
			if frame is self.botframe:
				return 1
			frame = frame.f_back
		return 0

	def break_here(self, frame):
		filename=frame.f_code.co_filename
		if not self.breaks.has_key(filename):
			return 0
		lineno=frame.f_lineno
		if not lineno in self.breaks[filename]:
			return 0
		# flag says ok to delete temp. bp
		(bp, flag) = effective(filename, lineno, frame)
		if bp:
			self.currentbp = bp.number
			if (flag and bp.temporary):
				self.do_clear(str(bp.number))
			return 1
		else:
			return 0
	
	def break_anywhere(self, frame):
		return self.breaks.has_key(frame.f_code.co_filename)
	
	# Derived classes should override the user_* methods
	# to gain control.
	
	def user_call(self, frame, argument_list):
		# This method is called when there is the remote possibility
		# that we ever need to stop in this function
		pass
	
	def user_line(self, frame):
		# This method is called when we stop or break at this line
		pass
	
	def user_return(self, frame, return_value):
		# This method is called when a return trap is set here
		pass
	
	def user_exception(self, frame, (exc_type, exc_value, exc_traceback)):
		# This method is called if an exception occurs,
		# but only if we are to stop at or just below this level
		pass
	
	# Derived classes and clients can call the following methods
	# to affect the stepping state.
	
	def set_step(self):
		# Stop after one line of code
		self.stopframe = None
		self.returnframe = None
		self.quitting = 0
	
	def set_next(self, frame):
		# Stop on the next line in or below the given frame
		self.stopframe = frame
		self.returnframe = None
		self.quitting = 0
	
	def set_return(self, frame):
		# Stop when returning from the given frame
		self.stopframe = frame.f_back
		self.returnframe = frame
		self.quitting = 0
	
	def set_trace(self):
		# Start debugging from here
		try:
			1 + ''
		except:
			frame = sys.exc_info()[2].tb_frame.f_back
		self.reset()
		while frame:
			frame.f_trace = self.trace_dispatch
			self.botframe = frame
			frame = frame.f_back
		self.set_step()
		sys.settrace(self.trace_dispatch)

	def set_continue(self):
		# Don't stop except at breakpoints or when finished
		self.stopframe = self.botframe
		self.returnframe = None
		self.quitting = 0
		if not self.breaks:
			# no breakpoints; run without debugger overhead
			sys.settrace(None)
			try:
				1 + ''	# raise an exception
			except:
				frame = sys.exc_info()[2].tb_frame.f_back
			while frame and frame is not self.botframe:
				del frame.f_trace
				frame = frame.f_back
	
	def set_quit(self):
		self.stopframe = self.botframe
		self.returnframe = None
		self.quitting = 1
		sys.settrace(None)
	
	# Derived classes and clients can call the following methods
	# to manipulate breakpoints.  These methods return an
	# error message is something went wrong, None if all is well.
	# Set_break prints out the breakpoint line and file:lineno.
	# Call self.get_*break*() to see the breakpoints or better
	# for bp in Breakpoint.bpbynumber: if bp: bp.bpprint().
	
	def set_break(self, filename, lineno, temporary=0, cond = None):
		import linecache # Import as late as possible
		line = linecache.getline(filename, lineno)
		if not line:
			return 'That line does not exist!'
		if not self.breaks.has_key(filename):
			self.breaks[filename] = []
		list = self.breaks[filename]
		if not lineno in list:
			list.append(lineno)
		bp = Breakpoint(filename, lineno, temporary, cond)
		print 'Breakpoint %d, at %s:%d.' %(bp.number, filename, lineno)

	def clear_break(self, arg):
		try:
			number = int(arg)
			bp = Breakpoint.bpbynumber[int(arg)]
		except:
			return 'Invalid argument'
		if not bp:
			return 'Breakpoint already deleted'
		filename = bp.file
		lineno = bp.line
		if not self.breaks.has_key(filename):
			return 'There are no breakpoints in that file!'
		if lineno not in self.breaks[filename]:
			return 'There is no breakpoint there!'
		# If there's only one bp in the list for that file,line
		# pair, then remove the breaks entry
		if len(Breakpoint.bplist[filename, lineno]) == 1:
			self.breaks[filename].remove(lineno)
		if not self.breaks[filename]:
			del self.breaks[filename]
		bp.deleteMe()
	
	def clear_all_file_breaks(self, filename):
		if not self.breaks.has_key(filename):
			return 'There are no breakpoints in that file!'
		for line in self.breaks[filename]:
			blist = Breakpoint.bplist[filename, line]
			for bp in blist:
				bp.deleteMe()
		del self.breaks[filename]
	
	def clear_all_breaks(self):
		if not self.breaks:
			return 'There are no breakpoints!'
		for bp in Breakpoint.bpbynumber:
			if bp:
				bp.deleteMe()
		self.breaks = {}
	
	def get_break(self, filename, lineno):
		return self.breaks.has_key(filename) and \
			lineno in self.breaks[filename]
	
	def get_file_breaks(self, filename):
		if self.breaks.has_key(filename):
			return self.breaks[filename]
		else:
			return []
	
	def get_all_breaks(self):
		return self.breaks
	
	# Derived classes and clients can call the following method
	# to get a data structure representing a stack trace.
	
	def get_stack(self, f, t):
		stack = []
		if t and t.tb_frame is f:
			t = t.tb_next
		while f is not None:
			stack.append((f, f.f_lineno))
			if f is self.botframe:
				break
			f = f.f_back
		stack.reverse()
		i = max(0, len(stack) - 1)
		while t is not None:
			stack.append((t.tb_frame, t.tb_lineno))
			t = t.tb_next
		return stack, i
	
	# 
	
	def format_stack_entry(self, frame_lineno, lprefix=': '):
		import linecache, repr, string
		frame, lineno = frame_lineno
		filename = frame.f_code.co_filename
		s = filename + '(' + `lineno` + ')'
		if frame.f_code.co_name:
			s = s + frame.f_code.co_name
		else:
			s = s + "<lambda>"
		if frame.f_locals.has_key('__args__'):
			args = frame.f_locals['__args__']
		else:
			args = None
		if args:
			s = s + repr.repr(args)
		else:
			s = s + '()'
		if frame.f_locals.has_key('__return__'):
			rv = frame.f_locals['__return__']
			s = s + '->'
			s = s + repr.repr(rv)
		line = linecache.getline(filename, lineno)
		if line: s = s + lprefix + string.strip(line)
		return s
	
	# The following two methods can be called by clients to use
	# a debugger to debug a statement, given as a string.
	
	def run(self, cmd, globals=None, locals=None):
		if globals is None:
			import __main__
			globals = __main__.__dict__
		if locals is None:
			locals = globals
		self.reset()
		sys.settrace(self.trace_dispatch)
		if type(cmd) <> types.CodeType:
			cmd = cmd+'\n'
		try:
			try:
				exec cmd in globals, locals
			except BdbQuit:
				pass
		finally:
			self.quitting = 1
			sys.settrace(None)
	
	def runeval(self, expr, globals=None, locals=None):
		if globals is None:
			import __main__
			globals = __main__.__dict__
		if locals is None:
			locals = globals
		self.reset()
		sys.settrace(self.trace_dispatch)
		if type(expr) <> types.CodeType:
			expr = expr+'\n'
		try:
			try:
				return eval(expr, globals, locals)
			except BdbQuit:
				pass
		finally:
			self.quitting = 1
			sys.settrace(None)

	def runctx(self, cmd, globals, locals):
		# B/W compatibility
		self.run(cmd, globals, locals)

	# This method is more useful to debug a single function call.

	def runcall(self, func, *args):
		self.reset()
		sys.settrace(self.trace_dispatch)
		res = None
		try:
			try:
				res = apply(func, args)
			except BdbQuit:
				pass
		finally:
			self.quitting = 1
			sys.settrace(None)
		return res


def set_trace():
	Bdb().set_trace()


class Breakpoint:

	"""Breakpoint class

	Implements temporary breakpoints, ignore counts, disabling and
	(re)-enabling, and conditionals.

	Breakpoints are indexed by number through bpbynumber and by
	the file,line tuple using bplist.  The former points to a
	single instance of class Breakpoint.  The latter points to a
	list of such instances since there may be more than one
	breakpoint per line.

	"""


	next = 1		# Next bp to be assigned
	bplist = {}		# indexed by (file, lineno) tuple
	bpbynumber = [None]	# Each entry is None or an instance of Bpt
				# index 0 is unused, except for marking an
				# effective break .... see effective()

	def __init__(self, file, line, temporary=0, cond = None):
		self.file = file
		self.line = line
		self.temporary = temporary
		self.cond = cond
		self.enabled = 1
		self.ignore = 0
		self.hits = 0
		self.number = Breakpoint.next
		Breakpoint.next = Breakpoint.next + 1
		# Build the two lists
		self.bpbynumber.append(self)
		if self.bplist.has_key((file, line)):
			self.bplist[file, line].append(self)
		else:
			self.bplist[file, line] = [self]

		
	def deleteMe(self):
		index = (self.file, self.line)
		self.bpbynumber[self.number] = None   # No longer in list
		self.bplist[index].remove(self)
		if not self.bplist[index]:
			# No more bp for this f:l combo
			del self.bplist[index]

	def enable(self):
		self.enabled = 1

	def disable(self):
		self.enabled = 0

	def bpprint(self):
		if self.temporary:
		   disp = 'del  '
		else:
		   disp = 'keep '
		if self.enabled:
		   disp = disp + 'yes'
		else:
		   disp = disp + 'no '
		print '%-4dbreakpoint	 %s at %s:%d' % (self.number, disp,
							 self.file, self.line)
		if self.cond:
			print '\tstop only if %s' % (self.cond,)
		if self.ignore:
			print '\tignore next %d hits' % (self.ignore)
		if (self.hits):
			if (self.hits > 1): ss = 's'
			else: ss = ''
			print ('\tbreakpoint already hit %d time%s' %
			       (self.hits, ss))

# -----------end of Breakpoint class----------

# Determines if there is an effective (active) breakpoint at this
# line of code.  Returns breakpoint number or 0 if none
def effective(file, line, frame):
	"""Determine which breakpoint for this file:line is to be acted upon.

	Called only if we know there is a bpt at this
	location.  Returns breakpoint that was triggered and a flag
	that indicates if it is ok to delete a temporary bp.

	"""
	possibles = Breakpoint.bplist[file,line]
	for i in range(0, len(possibles)):
		b = possibles[i]
		if b.enabled == 0:
			continue
		# Count every hit when bp is enabled
		b.hits = b.hits + 1
		if not b.cond:
			# If unconditional, and ignoring,
			# go on to next, else break
			if b.ignore > 0:
				b.ignore = b.ignore -1
				continue
			else:
				# breakpoint and marker that's ok
				# to delete if temporary
				return (b,1)
		else:
			# Conditional bp.
			# Ignore count applies only to those bpt hits where the
			# condition evaluates to true.
			try:
				val = eval(b.cond, frame.f_globals,
					   frame.f_locals) 
				if val:
					if b.ignore > 0:
						b.ignore = b.ignore -1
						# continue
					else:
						return (b,1)
				# else:
				#	continue
			except:
				# if eval fails, most conservative
				# thing is to stop on breakpoint
				# regardless of ignore count. 
				# Don't delete temporary,
				# as another hint to user.
				return (b,0)
	return (None, None)

# -------------------- testing --------------------

class Tdb(Bdb):
	def user_call(self, frame, args):
		name = frame.f_code.co_name
		if not name: name = '???'
		print '+++ call', name, args
	def user_line(self, frame):
		import linecache, string
		name = frame.f_code.co_name
		if not name: name = '???'
		fn = frame.f_code.co_filename
		line = linecache.getline(fn, frame.f_lineno)
		print '+++', fn, frame.f_lineno, name, ':', string.strip(line)
	def user_return(self, frame, retval):
		print '+++ return', retval
	def user_exception(self, frame, exc_stuff):
		print '+++ exception', exc_stuff
		self.set_continue()

def foo(n):
	print 'foo(', n, ')'
	x = bar(n*10)
	print 'bar returned', x

def bar(a):
	print 'bar(', a, ')'
	return a/2

def test():
	t = Tdb()
	t.run('import bdb; bdb.foo(10)')
