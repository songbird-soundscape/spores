#!/bin/sh
# Copy the Sporae Dispersae page and the files it loads into the main site repo,
# where it is served at https://songbird-soundscape.github.io/spores/
# Usage: tools/publish_to_site.sh ../songbird-soundscape.github.io
set -e
SITE="${1:?path to the songbird-soundscape.github.io checkout}"
mkdir -p "$SITE/spores"
rsync -a --delete --exclude .git --exclude R --exclude data --exclude tools --exclude TODO.md ./ "$SITE/spores/"
echo "Copied to $SITE/spores/. Commit and push that repo to publish."
