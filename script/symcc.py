#!/usr/bin/env python3

import os

WORKSPACE = "/workspace"
DOCKER_IMAGE = "symcc:root"

def main(mount_path="./workspace"):
    if not os.path.exists(mount_path):
        print(f"[Error] path {mount_path} not found")
        quit()
    mount_path = os.path.abspath(mount_path)
    argv = ["docker", "run", "-ti", "--rm",
            "-v", f"{mount_path}:{WORKSPACE}",
            DOCKER_IMAGE]

    # compile and run with in this image
    os.system(" ".join(argv))
    # symcc_fuzzing_helper -o o -a afl-slave

if __name__ == '__main__':
    main()
