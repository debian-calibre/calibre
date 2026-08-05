#!/bin/sh

set -eu

# Qt burfs some warnings to stderr when in Gnome-wayland session
unset XDG_SESSION_TYPE

# Qt outputs some warnings to stderr if XDG_RUNTIME_DIR is not set
export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:=/tmp/runtime-debci}
echo "#### XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR}"

# input file was taken from EPUB 3 Samples
#   https://github.com/IDPF/epub3-samples/releases/download/20230704/wasteland-woff-obf.epub
#   https://idpf.github.io/epub3-samples/30/samples.html
#   https://github.com/IDPF/epub3-samples/
input_file=debian/tests/data/wasteland-woff-obf.epub
output_file=${AUTOPKGTEST_ARTIFACTS}/wasteland-woff-obf.txt

ebook-convert ${input_file} ${output_file}
