#!/bin/sh

set -eux

output_dir=./debian/resources-src/calibre-translations/

# Use exact commit ID instead of branch name ("master") for reproducible build
git_master=$(git ls-remote --exit-code https://github.com/kovidgoyal/calibre-translations.git refs/heads/master | cut --fields=1)

curl --fail --location --remote-name --output-dir "${output_dir}" "https://github.com/kovidgoyal/calibre-translations/archive/${git_master}.tar.gz"

# Link to stable name for build script
ln -sf "${git_master}.tar.gz" "${output_dir}/master.tar.gz"
