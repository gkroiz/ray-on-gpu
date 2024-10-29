import ray
import socket
import jax

# Initialize Ray
ray.init()

@ray.remote(num_gpus=4)
def worker_task(x):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"hostname: {hostname}, local_ip: {local_ip}")
    print(f"jax devices: {jax.devices()}")
    return x * x

# Run tasks on worker(s)
futures = [worker_task.remote(i) for i in range(4)]
results = ray.get(futures)

print("Results from workers:", results)

# Shutdown Ray
ray.shutdown()