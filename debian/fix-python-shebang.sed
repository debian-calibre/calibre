#!/bin/sed --separate
#
# "--separate" option is required to point the first line of each input file.

1 {
  /^#! \?\/usr\/bin\/env python$/ s/python/python3/
}
