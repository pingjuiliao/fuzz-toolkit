#!/usr/bin/env python3

import argparse
import logging
import os


logger = logging.getLogger('fuzz-toolkit.aflpp')
logging.basicConfig(level=logging.INFO)

# the workspace path inside docker container
WORKSPACE = "/workspace"
DOCKER_IMAGE = "aflplusplus/aflplusplus"
FUZZING_SESSION_NAME = "Parallel Fuzzing"
AFL_MASTER = True
AFL_SLAVE = False


def execute(argv):
    os.system(" ".join(argv))
    return

def tmux_cmd(session_name, window_name, argv):
    return ["tmux", "new-session", "-d", "-s",
            session_name, "-n", window_name] + argv

def tmux_slave_cmd(session_name, window_name, argv):
    return ["tmux", "new-window", "-t", session_name + ":1",
            "-n", window_name] + argv

def docker_cmd(container_name, mount_path, argv=["/bin/bash"]):
    return ["docker", "run", "-ti", "--rm", "--name",
            f"{container_name}",
            "--volume", f"{mount_path}:{WORKSPACE}",
            DOCKER_IMAGE] + argv

def aflfuzz_cmd(is_master, argv):
    # paths
    input_dir = f"{WORKSPACE}/i"
    output_dir = f"{WORKSPACE}/o"

    afl_argv = ["afl-fuzz", "-i", input_dir,
                "-o", output_dir]
    if is_master:
        afl_argv += ["-M", "afl-master"]
    else:
        afl_argv += ["-S", "afl-slave"]
    return afl_argv + ["--"]  + argv

def run_parallel_fuzzing(mount_path, target_argv):
    # paths
    input_dir = f"{WORKSPACE}/i"
    output_dir = f"{WORKSPACE}/o"

    # names & tags
    target_program = target_argv[0].split('/')[-1]
    master_name = "fuzzer00"
    slave_name = "fuzzer01"
    session_name = "parallel-fuzzing"

    # argv
    tmux_argv = ["tmux", "new-session", "-d", "-s",
                 session_name, "-n", master_name]
    master_argv = ["afl-fuzz", "-i", input_dir, "-o", output_dir,
                    "-M", master_name, "--"]
    argv = tmux_argv + master_argv + target_argv
    master_cmd = " ".join(argv)
    logger.info(f"running: {master_cmd}")
    run_docker(master_name, mount_path, master_cmd)


def mount_path_check(path):
    # Mounting the path
    mount_path = path if path is not None else "./workspace"
    logger.info(f"Mounting {mount_path} as a workspace directory")
    if not os.path.exists(mount_path):
        logger.error(f"{mount_path} not found")
        quit()

    if not os.path.isdir(mount_path):
        logger.error(f"{mount_path} is not a directory")
        quit()
    return os.path.abspath(mount_path)




def main():
    parser = argparse.ArgumentParser()
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("-c", "--config", action="store_true")
    action_group.add_argument("-f", "--fuzz", nargs="+")
    parser.add_argument("-m", "--mount_path", type=str)
    args = parser.parse_args()

    mount_path = mount_path_check(args.mount_path)
    # Run mode: config mode or fuzz mode
    if args.config:
        cmd = docker_cmd("afl-config", mount_path)
        execute(cmd)
    elif args.fuzz is not None:
        # TODO: use chained method
        session_tag = "parallelfuzzing"

        # run master fuzzer
        master_cmd = tmux_cmd(session_tag, "fuzzer00",
            docker_cmd("afl-master", mount_path,
            aflfuzz_cmd(AFL_MASTER, args.fuzz)))
        execute(master_cmd)

        # run slave fuzzer
        slave_cmd = tmux_slave_cmd(session_tag, "fuzzer01",
            docker_cmd("afl-slave", mount_path,
            aflfuzz_cmd(AFL_SLAVE, args.fuzz)))

        execute(slave_cmd)

    else:
        logger.error("Please use either --master or --slave")

if __name__ == '__main__':
    main()
