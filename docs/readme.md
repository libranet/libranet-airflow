[![Testing](https://img.shields.io/github/actions/workflow/status/libranet/libranet-airflow/testing.yaml?branch=main&longCache=true&style=flat-square&label=tests&logo=GitHub%20Actions&logoColor=fff")](https://github.com/libranet/libranet-airflow/actions/workflows/testing.yaml)
[![Linting](https://img.shields.io/github/actions/workflow/status/libranet/libranet-airflow/linting.yaml?branch=main&longCache=true&style=flat-square&label=linting&logo=GitHub%20Actions&logoColor=fff")](https://github.com/libranet/libranet-airflow/actions/workflows/linting.yaml)
[![Read the Docs](https://readthedocs.org/projects/libranet-airflow/badge/?version=latest)](https://libranet-airflow.readthedocs.io/en/latest/)
[![Codecov](https://codecov.io/gh/libranet/libranet-airflow/branch/main/graph/badge.svg?token=QTOWRXGH61)](https://codecov.io/gh/libranet/libranet-airflow)
[![PyPi Package](https://img.shields.io/pypi/v/libranet-airflow?color=%2334D058&label=pypi%20package)](https://pypi.org/project/libranet-airflow/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/libranet/libranet-airflow/blob/main/docs/license.md)



## Introduction

A Airflow-environment.


References:
 - [Official website](https://airflow.apache.org)
 - [docs](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
 - [installation](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html)


## Installation


```
cd <your-projects-dir>
git clone https://github.com/libranet/libranet-airflow.git
make install
```


## Running airflow
Initialize database:

```
make airflow-db-init
```

Running webserver in standalone-mode
```
bin/airflow standalone
```

And then point your browser to [http://127.0.0.1:8080](http://127.0.0.1:8080/)

## Running pytest
Run the unittests with pytest:

```
make pytest
```


## Open in VS Code

```
code .
```