#!/usr/bin/env sh
set -o errexit -o pipefail
export DEBUG="${DEBUG:-false}"
if [ ${DEBUG} = "true" ]; then set -o xtrace; fi

export ENVSUBST_TEMP="/tmp/envsubst.temp"

envsubst < ${APP_CONFIG_FILE} > ${ENVSUBST_TEMP}
mv ${ENVSUBST_TEMP} ${APP_CONFIG_FILE}
if [ ${DEBUG} = "true" ]; then cat ${APP_CONFIG_FILE}; fi

case ${1} in
    app) exec python src/cli.py ;;
    *) exec "$@" ;;
esac
