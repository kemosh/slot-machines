#!/bin/bash

set -euo pipefail

function log { echo "$@" >&2; }
function error { log "ERROR: $@"; exit 1; }

export DOCKER_CLI_HINTS=false

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_DIR="$(cd "$dir/.." && pwd)"

# create pvs mount points
for vfile in $PROJECT_DIR/services/*/volumes.yaml; do
    dir=$(dirname "${vfile}")
    service_name="$(basename "$dir")"
    for mount_point in $(yq .volumes[] < $vfile); do
        rm -rf "$PROJECT_DIR/pvs/$service_name/$mount_point"
    done
    rm -rf $PROJECT_DIR/pvs/$service_name
done

