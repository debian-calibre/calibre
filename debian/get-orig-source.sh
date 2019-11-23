#!/bin/sh

set -eu

# Downloads the current upstream release according to debian/changelog, removes
# some bundled software copies, non-free image and replaces the non-free prs500
# TTFs with symlinks to their free liberation fonts counterparts. This also
# updates the unpacked source tree to the new upstream version and adds the
# original non-minimized javascript source for some minified JavaScript.

V=$(dpkg-parsechangelog --show-field=Version | cut --delimiter=+ --field=1)

mkdir -p debian/orig
cd debian/orig

wget -O - https://download.calibre-ebook.com/${V}/calibre-${V}.tar.xz | tar -Jx

rm -f calibre-${V}/src/odf/thumbnail.py
rm -r calibre-${V}/resources/mathjax
XZ_OPT="-9" tar -Jcf ../../../calibre_${V}+dfsg.orig.tar.xz calibre-${V}

cd ../..
rm -r debian/orig
