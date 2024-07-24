#!/bin/bash

function create_microservice() {
    NAME=${1:-"NewMicorservice"}

    mkdir "$NAME" && printf "\033[0;32mCreated Directory %s\033[0m\n" "${NAME}"

    cd "$NAME" || exit
    REPO_ROOT=$(realpath "$PWD")

    mkdir app docker scripts tests
    printf "\033[0;32mCreated dirs: app, docker, scripts, tests\033[0m\n"
    touch README.md pytest.ini
    printf "\033[0;32mCreated files in root: README.md, pytest.ini\033[0m\n"

    cd app || exit

    mkdir api schemas services
    printf "\033[0;32mCreated dirs in app: api, schemas, services\033[0m\n"
    touch __init__.py config.py main.py requirements.txt
    printf "\033[0;32mCreated files in app: __init__.py, config.py, main.py, requirements.txt\033[0m\n"

    find "$REPO_ROOT/app" -mindepth 1 -type d | while IFS= read -r directory; do
        touch "$directory/__init__.py"
    done
    printf "\033[0;32mAdded __init__.py to each dir in app\033[0m\n"

    cd "$REPO_ROOT/tests/" || exit
    touch requirements.txt

    cd "$REPO_ROOT" || exit
}