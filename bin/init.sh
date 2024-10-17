#!/bin/bash
dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PROJECT_DIR="$(cd "$dir/.." && pwd)"

. "$PROJECT_DIR/.env"

export DOCKER_CLI_HINTS=false

mongo_eval="docker exec -it mongodb mongosh -u ${MONGO_INITDB_ROOT_USERNAME} -p ${MONGO_INITDB_ROOT_PASSWORD} --eval"

$mongo_eval 'use user_manager'
$mongo_eval 'db.tokens.drop()'
$mongo_eval 'db.createCollection("tokens")'
$mongo_eval 'use login'
$mongo_eval 'db.users.drop()'
$mongo_eval 'db.createCollection("users")'

