#!/usr/bin/env bash

# This script could be symlinked from another location.
CANONICAL_SCRIPT_DIR=$(readlink -f $(dirname $(readlink -f $0)))
# PARENT_DIR=$(readlink -m ${CANONICAL_SCRIPT_DIR}/..)
# PARENT_DIR=$(realpath -m "${CANONICAL_SCRIPT_DIR}/..")
PARENT_DIR=$(${READLINK} -f $(dirname $(readlink -f $0)))

bin/airflow standalone
