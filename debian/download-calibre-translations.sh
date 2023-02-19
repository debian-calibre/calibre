#!/bin/sh

set -eux

# Use exact commit ID instead of branch name ("master") for reproducible build
git_master=1688698647b6fff7ee213d85f5a58e44c9dfd5d4

output_dir=./debian/resources-src/calibre-translations/

mkdir -p "${output_dir}"

curl --fail --location --remote-name --output-dir "${output_dir}" "https://github.com/kovidgoyal/calibre-translations/archive/${git_master}.tar.gz"

# Link to stable name for build script
ln -sf "${git_master}.tar.gz" "${output_dir}/master.tar.gz"
