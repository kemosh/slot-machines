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
    mkdir -p $PROJECT_DIR/pvs/$service_name
    for mount_point in $(yq .volumes[] < $vfile); do
        mkdir -pv "$PROJECT_DIR/pvs/$service_name/$mount_point"
    done
done

# build docker images
for df in $PROJECT_DIR/services/*/Dockerfile; do
    dir=$(dirname "${df}")
    service_name="$(basename "$dir")"
    log "building service: ${service_name}"
    cd $dir && docker build -t ${service_name} .
done

