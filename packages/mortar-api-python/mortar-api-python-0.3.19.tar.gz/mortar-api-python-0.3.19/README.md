# mortar-api-python

The Mortar API Client for Python is a Python wrapper to interact with [Mortar](https://github.com/DataDog/devops/wiki/Mortar).

[![Build Status](https://travis-ci.org/mortardata/mortar-api-python.png?branch=master)](https://travis-ci.org/mortardata/mortar-api-python)

# Installation

Pick up the latest version of mortar-api-python from PyPi:


```bash
pip install mortar-api-python
````

# Examples

## Running a Mortar Job

To run a job on a new cluster:

```python
from mortar.api.v2 import API
from mortar.api.v2 import jobs

# mortar credentials
email = 'myemail@me.org'
api_key = 'my-API-key'

# job to run
project_name = 'mortar-examples'
script_name = 'top_density_songs'
cluster_size = 2

# run and monitor the job
api = API(email, api_key)
job_id = jobs.post_job_new_cluster(api, project_name, script_name, cluster_size)
final_job_status = jobs.block_until_job_complete(api, job_id)
```

## Listing Your Mortar Projects

To fetch a list of Mortar projects:

```python
from mortar.api.v2 import API
from mortar.api.v2 import projects

# mortar credentials
email = 'myemail@me.org'
api_key = 'my-API-key'

api = API(email, api_key)
my_projects = projects.get_projects(api)
```

## Listing Your Running Clusters

```python
from mortar.api.v2 import API
from mortar.api.v2 import clusters

# mortar credentials
email = 'myemail@me.org'
api_key = 'my-API-key'

api = API(email, api_key)
recent_clusters = clusters.get_clusters(api)

running_clusters = [c for c in recent_clusters if c['status_code] == clusters.CLUSTER_STATUS_RUNNING]
```
# Documentation

* [mortar-api-python doc](http://mortar-api-python.readthedocs.org/en/latest/)
