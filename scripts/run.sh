#! /bin/bash
set -euo pipefail

debug=false

while getopts ":drp" opt; do
    case $opt in
    d)
        debug=true
        ;;
    esac
done

cmd=""

# allow debugging the command
if [ $debug == true ]; then
    cmd+="python -m debugpy --listen 0.0.0.0:5678 -m "
fi

# run the application
cmd+="uvicorn api:app --port 8000 --host 0.0.0.0 --access-log --no-use-colors --log-level debug --reload"

$cmd
