#!/bin/sh

set -eu

# Qt burfs some warnings to stderr when in Gnome-wayland session
unset XDG_SESSION_TYPE

################
# ebook-convert
################
echo "Test: ebook-convert"

mdown=debian/tests/data/markdown.md
epub=${AUTOPKGTEST_ARTIFACTS}/convert-md-epub.epub

ebook-convert ${mdown} ${epub}

#############
# ebook-meta
#############
echo "Test: ebook-meta"

title_mdown=$(cat ${mdown}      | grep '^title' | cut -d : -f 2 | sed -e 's/^ \+//')
title_epub=$(ebook-meta ${epub} | grep '^Title' | cut -d : -f 2 | sed -e 's/^ \+//')

echo "Markdown title : ${title_mdown}"
echo "ePub     title : ${title_epub}"

if [ "${title_mdown}" != "${title_epub}" ] ; then
    exit 1
fi

epubcheck ${epub}

###############
# ebook-polish
###############
echo "Test: ebook-polish"

epub_polished=${AUTOPKGTEST_ARTIFACTS}/convert-md-epub_pol.epub

ebook-polish --add-soft-hyphens --compress-images --remove-unused-css ${epub} ${epub_polished}

epubcheck ${epub_polished}
