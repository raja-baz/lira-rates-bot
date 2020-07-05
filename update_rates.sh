#!/bin/bash

export ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

mkdir -p rates_out 2>/dev/null
mkdir -p rates_next 2>/dev/null

has_change=0

changes=$(
    (ls fetchers | while read script_name
    do
        source_name=$(echo $script_name | sed 's/\.[^.]*//')
        "./fetchers/$script_name" > rates_next/"$source_name"
        if [[ $? != 0 ]]
        then
            echo "Failed to fetch from: $source_name" >&2
            rm rates_next/"$source_name"
        else
            python cmp_rates.py "$source_name"
            res=$?
            if [[ $res == 0 ]]
            then
                echo "Change detected on source: $source_name" >&2
                echo "$source_name"
            fi
        fi
    done) | tr '\n' ',' | sed 's/,$//'
       )

echo $changes

mv rates_next/* rates_out/
if [[ "$changes" != "" ]]
then
    python3 post_rate.py "$changes"
fi
