# Testing select module
from test_support import verbose
import select
import os

# test some known error conditions
try:
    rfd, wfd, xfd = select.select(1, 2, 3)
except TypeError:
    pass
else:
    print 'expected TypeError exception not raised'

class Nope:
    pass

class Almost:
    def fileno(self):
	return 'fileno'
    
try:
    rfd, wfd, xfd = select.select([Nope()], [], [])
except TypeError:
    pass
else:
    print 'expected TypeError exception not raised'

try:
    rfd, wfd, xfd = select.select([Almost()], [], [])
except TypeError:
    pass
else:
    print 'expected TypeError exception not raised'


def test():
	import sys
	if sys.platform in ('win', 'mac'):
		if verbose:
			print "Can't test select easily"
		return
	cmd = 'for i in 0 1 2 3 4 5 6 7 8 9; do echo testing...; sleep 1; done'
	p = os.popen(cmd, 'r')
	for tout in (0, 1, 2, 4, 8, 16) + (None,)*10:
		if verbose:
			print 'timeout =', tout
		rfd, wfd, xfd = select.select([p], [], [], tout)
## 		print rfd, wfd, xfd
		if (rfd, wfd, xfd) == ([], [], []):
			continue
		if (rfd, wfd, xfd) == ([p], [], []):
			line = p.readline()
			if verbose:
				print `line`
			if not line:
				if verbose:
					print 'EOF'
				break
			continue
		print 'Heh?'
	p.close()

test()

