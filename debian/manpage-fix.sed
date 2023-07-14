#!/usr/bin/sed -f
#
# Typo fix in man pages
#
# ".ft C" => ".ft CR"
#
# ".ft CR" means "set font to constant-width font".
#
# Usage:
# $ find man-pages -name "*.1" -type f -print | xargs --no-run-if-empty sed -f debian/manpage-fix.sed -i~

/^\.ft C$/ s/C$/CR/g
