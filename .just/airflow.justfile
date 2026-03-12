# airflow - Apache Airflow task runner commands

# ======
# GENERAL
# ======

# show version of airflow
[group: 'airflow']
airflow-version:
    @ uv run airflow version

# show help for airflow
[group: 'airflow']
airflow-help:
    @ uv run airflow --help

# show airflow environment info
[group: 'airflow']
airflow-info:
    @ uv run airflow info

# show airflow config
[group: 'airflow']
airflow-config:
    uv run airflow config list

# get a specific config value
[group: 'airflow']
airflow-config-get section key:
    uv run airflow config get-value {{section}} {{key}}

# ======
# STANDALONE / STARTUP
# ======

# start airflow standalone server (webserver + scheduler + db)
[group: 'airflow']
airflow-standalone *args:
    uv run airflow standalone {{args}}

alias airflow-start := airflow-standalone

# start webserver only (port 8080 by default)
[group: 'airflow']
airflow-webserver *args:
    uv run airflow webserver {{args}}

# start scheduler only
[group: 'airflow']
airflow-scheduler *args:
    uv run airflow scheduler {{args}}

# start triggerer (for deferrable operators)
[group: 'airflow']
airflow-triggerer *args:
    uv run airflow triggerer {{args}}

# ======
# DATABASE
# ======

# migrate airflow database to latest schema (Airflow 3.x)
[group: 'airflow']
airflow-db-migrate *args:
    uv run airflow db migrate {{args}}

# initialize airflow database (legacy, Airflow 2.x)
# [group: 'airflow']
# airflow-db-init *args:
#     uv run airflow db init {{args}}

# upgrade airflow database to latest schema
# [group: 'airflow']
# airflow-db-upgrade *args:
#     uv run airflow db upgrade {{args}}

# open a shell to access the database
[group: 'airflow']
airflow-db-shell *args:
    uv run airflow db shell {{args}}

# reset database (WARNING: destroys all data)
[group: 'airflow']
airflow-db-reset *args:
    uv run airflow db reset {{args}}

# check database migrations
[group: 'airflow']
airflow-db-check:
    uv run airflow db check

# ======
# DAG MANAGEMENT
# ======

# list all DAGs
[group: 'airflow']
airflow-dags-list *args:
    uv run airflow dags list {{args}}

alias dags := airflow-dags-list
alias airflow-list-dags := airflow-dags-list

# list DAG import errors
[group: 'airflow']
airflow-dags-errors:
    uv run airflow dags list-import-errors

# show details of a specific DAG
[group: 'airflow']
airflow-dag-details dag_id:
    uv run airflow dags details {{dag_id}}

# test a DAG (dry run without writing to db)
[group: 'airflow']
airflow-dag-test dag_id date="2024-01-01":
    uv run airflow dags test {{dag_id}} {{date}}

# trigger a DAG run
[group: 'airflow']
airflow-dag-trigger dag_id *args:
    uv run airflow dags trigger {{dag_id}} {{args}}

# pause a DAG
[group: 'airflow']
airflow-dag-pause dag_id:
    uv run airflow dags pause {{dag_id}}

# unpause a DAG
[group: 'airflow']
airflow-dag-unpause dag_id:
    uv run airflow dags unpause {{dag_id}}

# show next execution date for a DAG
[group: 'airflow']
airflow-dag-next dag_id:
    uv run airflow dags next-execution {{dag_id}}

# backfill a DAG for a date range
[group: 'airflow']
airflow-dag-backfill dag_id start_date end_date *args:
    uv run airflow dags backfill {{dag_id}} -s {{start_date}} -e {{end_date}} {{args}}

# reserialize all DAGs (refresh from files)
[group: 'airflow']
airflow-dags-reserialize:
    uv run airflow dags reserialize

# ======
# TASK MANAGEMENT
# ======

# list tasks in a DAG
[group: 'airflow']
airflow-tasks-list dag_id:
    uv run airflow tasks list {{dag_id}}

# list tasks in a DAG (tree view)
[group: 'airflow']
airflow-tasks-tree dag_id:
    uv run airflow tasks list {{dag_id}} --tree

# test a single task (runs task without dependencies)
[group: 'airflow']
airflow-task-test dag_id task_id date="2024-01-01":
    uv run airflow tasks test {{dag_id}} {{task_id}} {{date}}

# render task template
[group: 'airflow']
airflow-task-render dag_id task_id date="2024-01-01":
    uv run airflow tasks render {{dag_id}} {{task_id}} {{date}}

# show task state
[group: 'airflow']
airflow-task-state dag_id task_id date:
    uv run airflow tasks state {{dag_id}} {{task_id}} {{date}}

# clear task instances (allows re-run)
[group: 'airflow']
airflow-task-clear dag_id *args:
    uv run airflow tasks clear {{dag_id}} {{args}}

# get logs for a task instance
[group: 'airflow']
airflow-task-logs dag_id task_id date:
    uv run airflow tasks logs {{dag_id}} {{task_id}} {{date}}

# ======
# USERS
# ======

# list users
[group: 'airflow']
airflow-users-list:
    uv run airflow users list

# create admin user
[group: 'airflow']
airflow-user-create username email password="admin":
    uv run airflow users create \
        --username {{username}} \
        --email {{email}} \
        --password {{password}} \
        --firstname Admin \
        --lastname User \
        --role Admin

# delete a user
[group: 'airflow']
airflow-user-delete username:
    uv run airflow users delete {{username}}

# ======
# CONNECTIONS
# ======

# list all connections
[group: 'airflow']
airflow-connections-list:
    uv run airflow connections list

# get connection details
[group: 'airflow']
airflow-connection-get conn_id:
    uv run airflow connections get {{conn_id}}

# add a connection
[group: 'airflow']
airflow-connection-add conn_id conn_type host *args:
    uv run airflow connections add {{conn_id}} --conn-type {{conn_type}} --conn-host {{host}} {{args}}

# delete a connection
[group: 'airflow']
airflow-connection-delete conn_id:
    uv run airflow connections delete {{conn_id}}

# test a connection
[group: 'airflow']
airflow-connection-test conn_id:
    uv run airflow connections test {{conn_id}}

# ======
# VARIABLES
# ======

# list all variables
[group: 'airflow']
airflow-variables-list:
    uv run airflow variables list

# get a variable
[group: 'airflow']
airflow-variable-get key:
    uv run airflow variables get {{key}}

# set a variable
[group: 'airflow']
airflow-variable-set key value:
    uv run airflow variables set {{key}} {{value}}

# delete a variable
[group: 'airflow']
airflow-variable-delete key:
    uv run airflow variables delete {{key}}

# import variables from JSON file
[group: 'airflow']
airflow-variables-import file:
    uv run airflow variables import {{file}}

# export variables to JSON file
[group: 'airflow']
airflow-variables-export file:
    uv run airflow variables export {{file}}

# ======
# POOLS
# ======

# list all pools
[group: 'airflow']
airflow-pools-list:
    uv run airflow pools list

# set a pool
[group: 'airflow']
airflow-pool-set name slots description="":
    uv run airflow pools set {{name}} {{slots}} "{{description}}"

# delete a pool
[group: 'airflow']
airflow-pool-delete name:
    uv run airflow pools delete {{name}}

# ======
# PROVIDERS
# ======

# list installed providers
[group: 'airflow']
airflow-providers-list:
    uv run airflow providers list

# get provider info
[group: 'airflow']
airflow-provider-get provider:
    uv run airflow providers get {{provider}}

# ======
# DEBUGGING
# ======

# run airflow cheat-sheet
[group: 'airflow']
airflow-cheatsheet:
    uv run airflow cheat-sheet

# check airflow plugins
[group: 'airflow']
airflow-plugins:
    uv run airflow plugins

# show scheduler jobs
[group: 'airflow']
airflow-jobs-list *args:
    uv run airflow jobs list {{args}}
