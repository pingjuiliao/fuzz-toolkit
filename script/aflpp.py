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

class CommandLineExecutor:
    def __init__(self):
        self.argv = []
        self.runnable = False

    def run(self):
        if not self.runnable:
            print(f"Command {self.argv} not runnable")
            return
        cmd = " ".join(self.argv)
        logger.info(f"Running command '{cmd}' (end of command)")
        os.system(cmd)
        self.argv = []
        self.runnable = False
        return cmd

    def tmux_new(self, session_name, window_name):
        self.argv += ["tmux", "new-session", "-d", "-s",
                      session_name, "-n", window_name]
        self.runnable = False
        return self

    def tmux_add(self, session_name, window_name):
        self.argv = ["tmux", "new-window",
                     "-t", session_name + ":1",
                     "-n", window_name]
        self.runnable = False
        return self

    def docker_run(self, container_name, mount_path):
        self.argv += ["docker", "run", "-ti", "--rm",
                      "--name", f"{container_name}",
                      "--volume", f"{mount_path}:{WORKSPACE}",
                      DOCKER_IMAGE]
        self.runnable = True
        return self

    def aflfuzz_run(self, is_master, target_argv):
        # input/output paths
        input_dir = f"{WORKSPACE}/i"
        output_dir = f"{WORKSPACE}/o"

        self.argv += ["afl-fuzz",
                      "-i", input_dir,
                      "-o", output_dir]
        if is_master:
            self.argv += ["-M", "afl-master"]
        else:
            self.argv += ["-S", "afl-slave"]
        self.argv += ["--"] + target_argv
        self.runnable = True
        return self

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
    cle = CommandLineExecutor()
    if args.config:
        cle.docker_run("afl-config", mount_path).run()
        # cmd = docker_cmd("afl-config", mount_path)
        # execute(cmd)

    elif args.fuzz is not None:
        session_tag = "parallelfuzzing"

        # run master fuzzer
        (cle.tmux_new(session_tag, "fuzzer00")
         .docker_run("afl-master", mount_path)
         .aflfuzz_run(AFL_MASTER, args.fuzz).run())

        # run slave fuzzer
        (cle.tmux_add(session_tag, "fuzzer01")
         .docker_run("afl-slave", mount_path)
         .aflfuzz_run(AFL_SLAVE, args.fuzz).run())

    else:
        logger.error("Unexpected behavior")

if __name__ == '__main__':
    main()
