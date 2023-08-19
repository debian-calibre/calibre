#!/usr/bin/sed -f
#
# Typo fix in man pages
#
# ".ft C" => ".ft B"
#
# ".ft B" means "set font to bold font".
# See /usr/share/groff/current/font/devutf8/* and groff_font(5) man page
# for available fonts.
#
# Usage:
# $ find man-pages -name "*.1" -type f -print | xargs --no-run-if-empty sed -f debian/manpage-fix.sed -i~

/^\.ft C$/ s/C$/B/g
