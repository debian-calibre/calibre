#!/bin/sh
#
# Install manpages with Debian packaging style
#

set -eu

# default language
dh_installman --package=calibre --language=C man-pages/man1/*.1

# each languages
for i in man-pages/*
do
    lang=$(basename ${i})
    if [ "${lang}" = man1 ]
    then
	continue
    fi

    dh_installman --package=calibre --language=${lang} ${i}/man1/*.1
done
