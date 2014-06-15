#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/env/bin/activate
python3 $DIR/manage.py fetchepisodes
python3 $DIR/manage.py update_index
