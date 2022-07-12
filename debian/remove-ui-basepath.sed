#!/bin/sed --separate -f
#
# "--separate" option is required to point the 3rd line of each input file.
#
# Replace build dir to "<BUILDDIR>" in pyuic6 output file.

3 {
    s!^\(# Form implementation generated from reading ui file '/\).\+\(/src/calibre/gui2/.\+\.ui'\)$!\1<BUILDDIR>\2!
}
