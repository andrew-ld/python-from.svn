"""Suite URL Suite: Standard suite for Uniform Resource Locators
Level 1, version 1

Generated from Macintosh HD:Internet:Internet-programma's:Internet Explorer 4.5-map:Internet Explorer 4.5
AETE/AEUT resource version 1/0, language 0, script 0
"""

import aetools
import MacOS

_code = 'GURL'

class URL_Suite_Events:

	_argmap_GetURL = {
		'to' : 'dest',
	}

	def GetURL(self, _object, _attributes={}, **_arguments):
		"""GetURL: Open the URL (and optionally save it to disk)
		Required argument: The URL
		Keyword argument to: Save the resolved URL contents to this file.
		Keyword argument _attributes: AppleEvent attribute dictionary
		"""
		_code = 'GURL'
		_subcode = 'GURL'

		aetools.keysubst(_arguments, self._argmap_GetURL)
		_arguments['----'] = _object


		_reply, _arguments, _attributes = self.send(_code, _subcode,
				_arguments, _attributes)
		if _arguments.has_key('errn'):
			raise aetools.Error, aetools.decodeerror(_arguments)
		# XXXX Optionally decode result
		if _arguments.has_key('----'):
			return _arguments['----']


#
# Indices of types declared in this module
#
_classdeclarations = {
}

_propdeclarations = {
}

_compdeclarations = {
}

_enumdeclarations = {
}
