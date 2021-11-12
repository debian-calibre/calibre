#!/bin/sed --separate -f
#
# "--separate" option is required to point the 3rd line of each input file.

3 {
    s!'/.\+/src/!'<BUILDDIR>/src/!
}
