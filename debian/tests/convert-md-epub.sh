#!/bin/sh

set -eu

# Qt burfs some warnings to stderr when in Gnome-wayland session
unset XDG_SESSION_TYPE

# Qt outputs some warnings to stderr if XDG_RUNTIME_DIR is not set
export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:=/tmp/runtime-debci}
echo "#### XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR}"

################
# ebook-convert
################
echo "Test: ebook-convert"

mdown=debian/tests/data/markdown.md
epub=${AUTOPKGTEST_ARTIFACTS}/convert-md-epub.epub


echo "#### ebook-convert ${mdown} ${epub}"
ebook-convert ${mdown} ${epub}

echo ":::: end"

#############
# ebook-meta
#############
echo "Test: ebook-meta"

title_mdown=$(cat ${mdown}      | grep '^title' | cut -d : -f 2 | sed -e 's/^ \+//')
title_epub=$(ebook-meta ${epub} | grep '^Title' | cut -d : -f 2 | sed -e 's/^ \+//')

echo "Markdown title : \"${title_mdown}\""
echo "ePub     title : \"${title_epub}\""

if [ "${title_mdown}" != "${title_epub}" ] ; then
    exit 1
fi

echo ":::: end"

###############
# ebook-polish
###############
echo "Test: ebook-polish"

epub_polished=${AUTOPKGTEST_ARTIFACTS}/convert-md-epub_pol.epub

echo "#### ebook-polish ${epub} ${epub_polished}"
ebook-polish --add-soft-hyphens --compress-images --remove-unused-css ${epub} ${epub_polished}

echo ":::: end"
