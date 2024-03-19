import ray
import os
import subprocess

ray.init()
print("Available resources: ", ray.available_resources())


NUM_VMS = 4
GPUS_PER_NODE = 8

@ray.remote(num_gpus=GPUS_PER_NODE)
def run(node_rank):
    os.environ["NODE_RANK"] = str(node_rank)
    os.environ["MASTER_ADDR"] = "pytorch-leader-simple-torch"
    os.environ["MASTER_PORT"] = "6002"

    print("Running entrypoint script.")
    subprocess.run(["bash entrypoint_script.sh"], shell=True)
    print("Entrypoint script complete.")

ray.get([run.remote(node_rank) for node_rank in range(NUM_VMS)])
