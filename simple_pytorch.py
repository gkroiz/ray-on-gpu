import torch
import os

if __name__ == "__main__":
    rank = int(os.environ.get("RANK"))
    num_vms = int(os.environ.get("NUM_VMS"))
    gpus_per_node = int(os.environ.get("GPUS_PER_NODE"))
    world_size = num_vms * gpus_per_node
    print(f"In simple_pytorch.py, rank {rank}/{world_size}")
    torch.distributed.init_process_group("nccl", rank=rank, world_size=world_size)
    t = torch.tensor(1).to(rank % 8)
    torch.distributed.all_reduce(t)
    print("All reduce with global group complete!")