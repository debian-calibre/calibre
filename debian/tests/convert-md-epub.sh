#!/bin/sh

set -eu

# Qt burfs some warnings to stderr when in Gnome-wayland session
unset XDG_SESSION_TYPE

output=${AUTOPKGTEST_ARTIFACTS}/convert-md-epub.epub

ebook-convert debian/tests/data/markdown.md ${output}

epubcheck ${output}
