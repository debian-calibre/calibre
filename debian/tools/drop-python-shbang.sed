#!/bin/sed --separate --in-place --file
#
# drop unused Python shbang to Lintian clean
#

1 {
  s%^#! \?/usr/bin/env python$%#### &%
}
