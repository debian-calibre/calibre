#!/bin/sh

set -eux

output_dir=./debian/resources-src/recent_uas/

curl --output - --cacert resources/calibre-ebook-root-CA.crt https://code.calibre-ebook.com/ua-popularity | bunzip2 > ${output_dir}/common_user_agents

curl --output ${output_dir}/firefox_versions.html https://www.mozilla.org/en-US/firefox/releases/

curl --output ${output_dir}/chrome_versions.html https://en.wikipedia.org/wiki/Google_Chrome_version_history
