#!/bin/sh

set -eux

output_dir=./debian/resources-src/hyphenation/

git_master=$(git ls-remote --exit-code https://github.com/LibreOffice/dictionaries.git refs/heads/master | cut --fields=1)

curl --fail --location --remote-name --output-dir "${output_dir}" "https://github.com/LibreOffice/dictionaries/archive/${git_master}.tar.gz"

ln -sf "${git_master}.tar.gz" "${output_dir}/master.tar.gz"
