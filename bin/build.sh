#!/bin/bash

set -euo pipefail

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

# generate requirements
for rin in $PROJECT_DIR/services/*/requirements.in; do
    dir=$(dirname "${rin}")
    echo "compiling ${dir}/requirements.in"
    cd $dir && uv pip compile -q -o $dir/requirements.txt $dir/requirements.in
done

# build docker images
for df in $PROJECT_DIR/services/*/Dockerfile; do
    dir=$(dirname "${df}")
    service_name="$(basename "$dir")"
    cd $dir && docker build -t ${service_name} .
done
