""" Python Character Mapping Codec generated from 'CP775.TXT' with gencodec.py.

Written by Marc-Andre Lemburg (mal@lemburg.com).

(c) Copyright CNRI, All Rights Reserved. NO WARRANTY.
(c) Copyright 2000 Guido van Rossum.

"""#"

import codecs

### Codec APIs

class Codec(codecs.Codec):

    def encode(self,input,errors='strict'):

        return codecs.charmap_encode(input,errors,encoding_map)
        
    def decode(self,input,errors='strict'):

        return codecs.charmap_decode(input,errors,decoding_map)

class StreamWriter(Codec,codecs.StreamWriter):
    pass
        
class StreamReader(Codec,codecs.StreamReader):
    pass

### encodings module API

def getregentry():

    return (Codec().encode,Codec().decode,StreamReader,StreamWriter)

### Decoding Map

decoding_map = codecs.make_identity_dict(range(256))
decoding_map.update({
	0x0080: 0x0106,	# LATIN CAPITAL LETTER C WITH ACUTE
	0x0081: 0x00fc,	# LATIN SMALL LETTER U WITH DIAERESIS
	0x0082: 0x00e9,	# LATIN SMALL LETTER E WITH ACUTE
	0x0083: 0x0101,	# LATIN SMALL LETTER A WITH MACRON
	0x0084: 0x00e4,	# LATIN SMALL LETTER A WITH DIAERESIS
	0x0085: 0x0123,	# LATIN SMALL LETTER G WITH CEDILLA
	0x0086: 0x00e5,	# LATIN SMALL LETTER A WITH RING ABOVE
	0x0087: 0x0107,	# LATIN SMALL LETTER C WITH ACUTE
	0x0088: 0x0142,	# LATIN SMALL LETTER L WITH STROKE
	0x0089: 0x0113,	# LATIN SMALL LETTER E WITH MACRON
	0x008a: 0x0156,	# LATIN CAPITAL LETTER R WITH CEDILLA
	0x008b: 0x0157,	# LATIN SMALL LETTER R WITH CEDILLA
	0x008c: 0x012b,	# LATIN SMALL LETTER I WITH MACRON
	0x008d: 0x0179,	# LATIN CAPITAL LETTER Z WITH ACUTE
	0x008e: 0x00c4,	# LATIN CAPITAL LETTER A WITH DIAERESIS
	0x008f: 0x00c5,	# LATIN CAPITAL LETTER A WITH RING ABOVE
	0x0090: 0x00c9,	# LATIN CAPITAL LETTER E WITH ACUTE
	0x0091: 0x00e6,	# LATIN SMALL LIGATURE AE
	0x0092: 0x00c6,	# LATIN CAPITAL LIGATURE AE
	0x0093: 0x014d,	# LATIN SMALL LETTER O WITH MACRON
	0x0094: 0x00f6,	# LATIN SMALL LETTER O WITH DIAERESIS
	0x0095: 0x0122,	# LATIN CAPITAL LETTER G WITH CEDILLA
	0x0096: 0x00a2,	# CENT SIGN
	0x0097: 0x015a,	# LATIN CAPITAL LETTER S WITH ACUTE
	0x0098: 0x015b,	# LATIN SMALL LETTER S WITH ACUTE
	0x0099: 0x00d6,	# LATIN CAPITAL LETTER O WITH DIAERESIS
	0x009a: 0x00dc,	# LATIN CAPITAL LETTER U WITH DIAERESIS
	0x009b: 0x00f8,	# LATIN SMALL LETTER O WITH STROKE
	0x009c: 0x00a3,	# POUND SIGN
	0x009d: 0x00d8,	# LATIN CAPITAL LETTER O WITH STROKE
	0x009e: 0x00d7,	# MULTIPLICATION SIGN
	0x009f: 0x00a4,	# CURRENCY SIGN
	0x00a0: 0x0100,	# LATIN CAPITAL LETTER A WITH MACRON
	0x00a1: 0x012a,	# LATIN CAPITAL LETTER I WITH MACRON
	0x00a2: 0x00f3,	# LATIN SMALL LETTER O WITH ACUTE
	0x00a3: 0x017b,	# LATIN CAPITAL LETTER Z WITH DOT ABOVE
	0x00a4: 0x017c,	# LATIN SMALL LETTER Z WITH DOT ABOVE
	0x00a5: 0x017a,	# LATIN SMALL LETTER Z WITH ACUTE
	0x00a6: 0x201d,	# RIGHT DOUBLE QUOTATION MARK
	0x00a7: 0x00a6,	# BROKEN BAR
	0x00a8: 0x00a9,	# COPYRIGHT SIGN
	0x00a9: 0x00ae,	# REGISTERED SIGN
	0x00aa: 0x00ac,	# NOT SIGN
	0x00ab: 0x00bd,	# VULGAR FRACTION ONE HALF
	0x00ac: 0x00bc,	# VULGAR FRACTION ONE QUARTER
	0x00ad: 0x0141,	# LATIN CAPITAL LETTER L WITH STROKE
	0x00ae: 0x00ab,	# LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
	0x00af: 0x00bb,	# RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
	0x00b0: 0x2591,	# LIGHT SHADE
	0x00b1: 0x2592,	# MEDIUM SHADE
	0x00b2: 0x2593,	# DARK SHADE
	0x00b3: 0x2502,	# BOX DRAWINGS LIGHT VERTICAL
	0x00b4: 0x2524,	# BOX DRAWINGS LIGHT VERTICAL AND LEFT
	0x00b5: 0x0104,	# LATIN CAPITAL LETTER A WITH OGONEK
	0x00b6: 0x010c,	# LATIN CAPITAL LETTER C WITH CARON
	0x00b7: 0x0118,	# LATIN CAPITAL LETTER E WITH OGONEK
	0x00b8: 0x0116,	# LATIN CAPITAL LETTER E WITH DOT ABOVE
	0x00b9: 0x2563,	# BOX DRAWINGS DOUBLE VERTICAL AND LEFT
	0x00ba: 0x2551,	# BOX DRAWINGS DOUBLE VERTICAL
	0x00bb: 0x2557,	# BOX DRAWINGS DOUBLE DOWN AND LEFT
	0x00bc: 0x255d,	# BOX DRAWINGS DOUBLE UP AND LEFT
	0x00bd: 0x012e,	# LATIN CAPITAL LETTER I WITH OGONEK
	0x00be: 0x0160,	# LATIN CAPITAL LETTER S WITH CARON
	0x00bf: 0x2510,	# BOX DRAWINGS LIGHT DOWN AND LEFT
	0x00c0: 0x2514,	# BOX DRAWINGS LIGHT UP AND RIGHT
	0x00c1: 0x2534,	# BOX DRAWINGS LIGHT UP AND HORIZONTAL
	0x00c2: 0x252c,	# BOX DRAWINGS LIGHT DOWN AND HORIZONTAL
	0x00c3: 0x251c,	# BOX DRAWINGS LIGHT VERTICAL AND RIGHT
	0x00c4: 0x2500,	# BOX DRAWINGS LIGHT HORIZONTAL
	0x00c5: 0x253c,	# BOX DRAWINGS LIGHT VERTICAL AND HORIZONTAL
	0x00c6: 0x0172,	# LATIN CAPITAL LETTER U WITH OGONEK
	0x00c7: 0x016a,	# LATIN CAPITAL LETTER U WITH MACRON
	0x00c8: 0x255a,	# BOX DRAWINGS DOUBLE UP AND RIGHT
	0x00c9: 0x2554,	# BOX DRAWINGS DOUBLE DOWN AND RIGHT
	0x00ca: 0x2569,	# BOX DRAWINGS DOUBLE UP AND HORIZONTAL
	0x00cb: 0x2566,	# BOX DRAWINGS DOUBLE DOWN AND HORIZONTAL
	0x00cc: 0x2560,	# BOX DRAWINGS DOUBLE VERTICAL AND RIGHT
	0x00cd: 0x2550,	# BOX DRAWINGS DOUBLE HORIZONTAL
	0x00ce: 0x256c,	# BOX DRAWINGS DOUBLE VERTICAL AND HORIZONTAL
	0x00cf: 0x017d,	# LATIN CAPITAL LETTER Z WITH CARON
	0x00d0: 0x0105,	# LATIN SMALL LETTER A WITH OGONEK
	0x00d1: 0x010d,	# LATIN SMALL LETTER C WITH CARON
	0x00d2: 0x0119,	# LATIN SMALL LETTER E WITH OGONEK
	0x00d3: 0x0117,	# LATIN SMALL LETTER E WITH DOT ABOVE
	0x00d4: 0x012f,	# LATIN SMALL LETTER I WITH OGONEK
	0x00d5: 0x0161,	# LATIN SMALL LETTER S WITH CARON
	0x00d6: 0x0173,	# LATIN SMALL LETTER U WITH OGONEK
	0x00d7: 0x016b,	# LATIN SMALL LETTER U WITH MACRON
	0x00d8: 0x017e,	# LATIN SMALL LETTER Z WITH CARON
	0x00d9: 0x2518,	# BOX DRAWINGS LIGHT UP AND LEFT
	0x00da: 0x250c,	# BOX DRAWINGS LIGHT DOWN AND RIGHT
	0x00db: 0x2588,	# FULL BLOCK
	0x00dc: 0x2584,	# LOWER HALF BLOCK
	0x00dd: 0x258c,	# LEFT HALF BLOCK
	0x00de: 0x2590,	# RIGHT HALF BLOCK
	0x00df: 0x2580,	# UPPER HALF BLOCK
	0x00e0: 0x00d3,	# LATIN CAPITAL LETTER O WITH ACUTE
	0x00e1: 0x00df,	# LATIN SMALL LETTER SHARP S (GERMAN)
	0x00e2: 0x014c,	# LATIN CAPITAL LETTER O WITH MACRON
	0x00e3: 0x0143,	# LATIN CAPITAL LETTER N WITH ACUTE
	0x00e4: 0x00f5,	# LATIN SMALL LETTER O WITH TILDE
	0x00e5: 0x00d5,	# LATIN CAPITAL LETTER O WITH TILDE
	0x00e6: 0x00b5,	# MICRO SIGN
	0x00e7: 0x0144,	# LATIN SMALL LETTER N WITH ACUTE
	0x00e8: 0x0136,	# LATIN CAPITAL LETTER K WITH CEDILLA
	0x00e9: 0x0137,	# LATIN SMALL LETTER K WITH CEDILLA
	0x00ea: 0x013b,	# LATIN CAPITAL LETTER L WITH CEDILLA
	0x00eb: 0x013c,	# LATIN SMALL LETTER L WITH CEDILLA
	0x00ec: 0x0146,	# LATIN SMALL LETTER N WITH CEDILLA
	0x00ed: 0x0112,	# LATIN CAPITAL LETTER E WITH MACRON
	0x00ee: 0x0145,	# LATIN CAPITAL LETTER N WITH CEDILLA
	0x00ef: 0x2019,	# RIGHT SINGLE QUOTATION MARK
	0x00f0: 0x00ad,	# SOFT HYPHEN
	0x00f1: 0x00b1,	# PLUS-MINUS SIGN
	0x00f2: 0x201c,	# LEFT DOUBLE QUOTATION MARK
	0x00f3: 0x00be,	# VULGAR FRACTION THREE QUARTERS
	0x00f4: 0x00b6,	# PILCROW SIGN
	0x00f5: 0x00a7,	# SECTION SIGN
	0x00f6: 0x00f7,	# DIVISION SIGN
	0x00f7: 0x201e,	# DOUBLE LOW-9 QUOTATION MARK
	0x00f8: 0x00b0,	# DEGREE SIGN
	0x00f9: 0x2219,	# BULLET OPERATOR
	0x00fa: 0x00b7,	# MIDDLE DOT
	0x00fb: 0x00b9,	# SUPERSCRIPT ONE
	0x00fc: 0x00b3,	# SUPERSCRIPT THREE
	0x00fd: 0x00b2,	# SUPERSCRIPT TWO
	0x00fe: 0x25a0,	# BLACK SQUARE
	0x00ff: 0x00a0,	# NO-BREAK SPACE
})

### Encoding Map

encoding_map = codecs.make_encoding_map(decoding_map)
