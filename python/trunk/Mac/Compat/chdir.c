/* Chdir for the Macintosh.
   Public domain by Guido van Rossum, CWI, Amsterdam (July 1987).
   Pathnames must be Macintosh paths, with colons as separators. */

#include "macdefs.h"

/* Change current directory. */

int
chdir(path)
	char *path;
{
	WDPBRec pb;
	
	pb.ioNamePtr= (StringPtr) Pstring(path);
	pb.ioVRefNum= 0;
	pb.ioWDDirID= 0;
	if (PBHSetVol(&pb, FALSE) != noErr) {
		errno= ENOENT;
		return -1;
	}
	return 0;
}
