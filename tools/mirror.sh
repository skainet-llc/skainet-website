#!/bin/sh
# Re-fetch skainet.io into the repo root, then clean it for static hosting.
set -eu
cd "$(dirname "$0")/.."
wget --mirror --page-requisites --convert-links --adjust-extension \
     --no-host-directories --no-verbose -e robots=off \
     --reject-regex 'wp-json|xmlrpc\.php|/feed/|wp-login|\?p=|oembed' \
     --domains skainet.io https://skainet.io/
python3 tools/clean.py .
