#!/bin/bash

# Default values of arguments:
PROJECT="poc_fastapi"
APP="$PROJECT.app:app"

DEVELOPMENT=0
# New Relic on/off
NEW_RELIC=0
# New Relic Environment
NRE_LIST=("development" "test" "staging" "production")
NEW_RELIC_ENVIRONMENT="development"

# Server bind address and port
S_ADDRESS="0.0.0.0"
PORT="8000"
WORKERS_COUNT=4


display_help() {
    echo "Usage: $0 [option...] {n|p|a,nre}" >&2
    echo
    echo "   -h, --help                 Show this help message and exit"
    echo "   -d, --development          Set the application server to run as run-server dev mode"
    echo "   -n, --newrelic             Start with NewRelic"
    echo "   -nre=, --nrenv=            Set New Relic Environment {development|test|staging|production}, default=development"
    echo "   -p=, --port=               Set server starting port, default=8000"
    echo "   -a=, --address=            Set server listening address, default=0.0.0.0"

    echo
    exit 0
}


exit_with_error(){
    echo "Something went wrong"
    exit 1
}

display_argument_error(){
    echo "[ERROR] Check your arguments!!."
    echo "--You typed $1, yet you can only use:"
    for a in "${@:2}"; do
        echo "$a"
    done
    echo "For this argument."
    exit_with_error
}


elementIn () {
    # shopt -s nocasematch # Can be useful to disable case-matching
    local e
    for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
    return 1
}

test_argument(){
    elementIn $1 "${@:2}" || display_argument_error $1 "${@:2}"
}

start_server_with_newrelic(){
    echo "Starting server with NewRelic..."
    echo "NewRelic Environment: $NEW_RELIC_ENVIRONMENT"
    echo "NewRelic Conf file: newrelic.ini"
    NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn -b $S_ADDRESS:$PORT -w $WORKERS_COUNT --forwarded-allow-ips="*" $APP -k uvicorn.workers.UvicornWorker
    exit_with_error
}

start_server(){
    echo "Starting uvicorn..."
    gunicorn -b $S_ADDRESS:$PORT -w $WORKERS_COUNT --forwarded-allow-ips="*" $APP -k uvicorn.workers.UvicornWorker
}

start_server_in_development(){
    echo "Starting server in development mode..."
    FASTAPI_DEBUG=1 uvicorn $APP --reload --host $S_ADDRESS --port $PORT
    exit_with_error
}


wait_for_db(){
    echo "Waiting for PG to become online..."
    sleep 5
}

default_start(){
    wait_for_db
    migrate_data
    start_server
    exit_with_error
}

migrate_data(){
  echo "Migrating data..."
  alembic upgrade head
}


choose_starting_way(){
    if [ $DEVELOPMENT -eq 1 ]; then wait_for_db && migrate_data && start_server_in_development || exit_with_error; fi

    if [ $NEW_RELIC -eq 1 ]; then wait_for_db && migrate_data && start_server_with_newrelic || exit_with_error; fi

    default_start
}


main(){
    choose_starting_way
}

# Loop through arguments and process them
for arg in "$@"
do
    case $arg in
        -h|--help)
        display_help
        shift
        ;;
        -e=*|--nrenv=*)
        NEW_RELIC_ENVIRONMENT="${arg#*=}"
        [ -z $NEW_RELIC_ENVIRONMENT ] || test_argument $NEW_RELIC_ENVIRONMENT "${NRE_LIST[@]}"
        shift
        ;;
        -p=*|--port=*)
        PORT="${arg#*=}"
        shift
        ;;
        -a=*|--address=*)
        S_ADDRESS="${arg#*=}"
        shift
        ;;
        -n|--newrelic)
        NEW_RELIC=1
        shift # Remove --newrelic from processing
        ;;
        -d|--development)
        DEVELOPMENT=1
        shift
        ;;
        *)
        exec "$@"
        shift
        ;;
    esac
done

main