# Airflow Docker Helper
[![CircleCI](https://circleci.com/gh/huntcsg/airflow-docker-helper/tree/master.svg?style=svg)](https://circleci.com/gh/huntcsg/airflow-docker-helper/tree/master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/3e2f177d8c314f43903fe9d9b7af0647)](https://www.codacy.com/app/fool.of.god/airflow-docker-helper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=huntcsg/airflow-docker-helper&amp;utm_campaign=Badge_Grade) [![codecov](https://codecov.io/gh/huntcsg/airflow-docker-helper/branch/master/graph/badge.svg)](https://codecov.io/gh/huntcsg/airflow-docker-helper)

## Description
A light sdk to be used by the operators in airflow-docker and in task code to participate in host/container communication.

## Installation

```bash
pip install airflow-docker-helper
```

## Usage

### Sensor
```python
from airflow_docker_helper import client

if sensed:
    client.sensor(True)
else:
    client.sensor(False)
```

### Short Circuit

```python
from airflow_docker_helper import client

if should_short_circuit:
    client.short_circuit()
```

### Branching

You can pass a list...
```python
from airflow_docker_helper import client

branch_to_task_ids = ['foo', 'bar']

client.branch_to_tasks(branch_to_task_ids)

```

... or a string.
```python
from airflow_docker_helper import client

client.branch_to_tasks('some-other-task')

```
