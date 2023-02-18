#!/bin/sh
#
# Download hyphenation dictionary source from LibreOffice
#
# Use from top of build tree
#

set -eux

output_dir=./debian/resources-src/hyphenation/

# Use exact commit ID instead of branch name ("master") for reproducible build
git_master=$(git ls-remote --exit-code https://github.com/LibreOffice/dictionaries.git refs/heads/master | cut --fields=1)

curl --fail --location --remote-name --output-dir "${output_dir}" "https://github.com/LibreOffice/dictionaries/archive/${git_master}.tar.gz"

# Link to stable name for build script
ln -sf "${git_master}.tar.gz" "${output_dir}/master.tar.gz"
