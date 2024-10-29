# Using GPUs with Ray + GKE
Assuming everything is setup correctly, [main.py](main.py) runs the entrypoint script, [entrypoint_script.sh](entrypoint_script.sh), which calls the pytorch workload [simple_pytorch.py](simple_pytorch.py).

If you want to run your own workloads using this repository as a skeleton, you will need to use your own docker image in [values.yaml](helm/values.yaml) and will need to update the entrypoint script to match your workload.

## Setup on GKE
The instructions below are specifically for using A3s. To use different class of GPUs, adjust flags accordingly.
### Set up the cluster
```
$ gcloud container clusters create <CLUSTER_NAME> \
    --num-nodes=1 \
    --min-nodes 0 \
    --max-nodes 1 \
    --enable-autoscaling \
    --zone=us-central1-c \
    --machine-type e2-standard-8
```

### Set up the node pool
```
$ gcloud container node-pools create <NODE POOL> \
    --accelerator type=nvidia-h100-80gb,count=8 \
    --zone us-central1-c \
    --cluster <CLUSTER_NAME> \
    --num-nodes 4 \
    --min-nodes 4 \
    --max-nodes 4 \
    --enable-autoscaling \
    --machine-type a3-highgpu-8g
```

### Install NVIDIA GPU device driver
```
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml
```

### Deploy a Ray cluster on Kubernetes with the KubeRay operator.
Please make sure you are connected to your Kubernetes cluster. For GCP, you can do so by:
- (Method 1) Copy the connection command from the GKE console
- (Method 2) "gcloud container clusters get-credentials <your-cluster-name> --region <your-region> --project <your-project>"
- (Method 3) "kubectl config use-context ..."

### Install both CRDs and KubeRay operator
```
$ helm repo add kuberay https://ray-project.github.io/kuberay-helm/
$ helm repo update
$ helm install kuberay-operator kuberay/kuberay-operator --version 1.0.0
```

### Create a Ray cluster
This tutorial uses helm to create the ray cluster

[values.yaml](helm/values.yaml) has several variables that the user can adjust.
* `nNodes`: number of nodes
* `gpusPerNode`: gpus per node
* `image`: docker image that includes code for user's workload.

For more information on the image value, please refer to ["Create Docker Image"](#create-docker-image)

Command to create the ray cluster:
```
helm install simple-torch -f helm/values.yaml helm/
```

### Create Docker Image
This tutorial provides a basic [Dockerfile](Dockerfile) that can be used to create the image. If you wish to use your own Docker container, make sure that it installs all of the dependencies needed to run your workload, including Ray.

If you wish to create a docker image using the Dockerfile provided in this repository, please first create an artifact registry by following https://cloud.google.com/artifact-registry/docs/repositories/create-repos. Then, create the docker image locally:
```
DOCKER_BUILDKIT=1 docker build -f Dockerfile -t <IMAGE_NAME>
```
follwed by
```
gcloud builds submit --region=us-central1 --tag <REGISTRY_URL>/<CONTAINER_NAME>:<TAG>
```

The `REGISTRY_URL` should look something like `us-central1-docker.pkg.dev/<PROJECT_NAME>/<REPO_NAME>`.

In [values.yaml](helm/values.yaml), replace the image docker image with the same value you use for the tag flag, `<REGISTRY_URL>/<CONTAINER_NAME>:<TAG>`.

### Set up port-forwarding
```
kubectl port-forward --address 0.0.0.0 services/<POD_PREFIX>-helm-raycluster-head-svc 8265:8265
```

## Run workload
### Running the simple_pytorch script
```
$ export RAY_ADDRESS=http://127.0.0.1:8265
$ ray job submit --working-dir . -- RAY_DEDUP_LOGS=0 python main.py
```

### Stop a job
```
$ ray job stop $JOB_ID
```
