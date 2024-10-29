# Using GPUs with Ray on GCP VMs
These instructions are catered specifically for L4 GPUs. To use a different generation of GPUs, adjust the values in [cluster.yaml](cluster.yaml).

## Instructions
### Setup the cluster
First, set the `project_id` and `serviceAccounts.email` in [cluster.yaml](cluster.yaml).

To spin up the cluster, run
```
$ ray up -y cluster.yaml
```
*Note: The workers take a few minutes to setup. Check the dashboard for the status of the ray head and workers.*

### Teardown the cluster
To spin down the cluster, run
```
$ ray down -y cluster.yaml
```

### Run dashboard (optional)
The Ray dashboard is a great way to get an overview of the cluster's activity. To start the dashboard, run
```
$ ray dashboard cluster.yaml
```

### Run workload
To start a workload, run
```
$ export RAY_ADDRESS=http://127.0.0.1:8265
$ ray job submit --working-dir . -- RAY_DEDUP_LOGS=0 python main.py
```

### Stop workload
To stop the workload, run
```
$ ray job stop $JOB_ID
```

### Run tests
To run simple script to test ray's head worker connection:
```
$ export RAY_ADDRESS=http://127.0.0.1:8265
$ ray job submit --working-dir . -- python3 test_ray.py 
```

To test jax + CUDA setup:
```
$ export RAY_ADDRESS=http://127.0.0.1:8265
$ ray job submit --working-dir . -- python3 test_ray_jax.py 
```