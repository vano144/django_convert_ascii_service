#!/bin/bash

# http://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

if ! [ -d lib ]; then
    mkdir lib
fi

cd lib

deps=("https://raw.githubusercontent.com/HubSpot/pace/v1.0.0/pace.min.js" \
      "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" \
      "https://raw.githubusercontent.com/eligrey/FileSaver.js/master/FileSaver.min.js" \
      "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/9.8.0/bootstrap-slider.min.js" \
      "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/9.8.0/css/bootstrap-slider.min.css" \
)

if [[ "$1." == "--force." ]]; then
    rm ".gitignore" 2> /dev/null
fi

for dep in ${deps[@]}; do
    fname=$(echo "$dep" | grep -oE '[^/]+$')
    if [[ "$1." == "--force." ]]; then
        rm "$fname" 2> /dev/null
    fi
    if ! [[ -e "$fname" ]]; then
        echo "Loading: " "$fname"
        wget "$dep"
        echo "$fname" >> ./.gitignore
    else
        echo "$fname" "already exists"
    fi
done
