#!/bin/sh
#
# Download hyphenation dictionary source from LibreOffice
#
# Use from top of build tree
#

set -eux

# Use exact commit ID instead of branch name ("master") for reproducible build
git_master=bcf7f049315dee2001cc2f7c7eabfbcb0b8ef21a

output_dir=./debian/resources-src/hyphenation/

mkdir -p "${output_dir}"

curl --fail --location --remote-name --output-dir "${output_dir}" "https://github.com/LibreOffice/dictionaries/archive/${git_master}.tar.gz"

# Link to stable name for build script
ln -sf "${git_master}.tar.gz" "${output_dir}/master.tar.gz"
