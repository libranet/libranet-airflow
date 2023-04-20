# This is a comment.
# See ../makefile

.PHONY: airflow-which  ## show which airflow is used
airflow-which:
	@ which airflow


.PHONY: airflow-version  ## show airflow version
airflow-version:
	airflow version


.PHONY: airflow-help  ## show airflow help
airflow-help:
	airflow --help


.PHONY: airflow-info  ## show airflow info
airflow-info:
	airflow info


.PHONY: airflow-list-config  ## show airflow config
airflow-list-config:
	airflow config --list


.PHONY: airflow-db-init  ## airflow initialize database
airflow-db-init:
	airflow db init


.PHONY: airflow-db-upgrade  ## airflow upgrade database
airflow-db-upgrade:
	airflow db upgrade


.PHONY: airflow-standalone  ## airflow run standalone server
airflow-standalone:
	# this generates a password in the log-ouput
	airflow standalone