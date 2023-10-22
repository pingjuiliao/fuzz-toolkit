#!/usr/bin/env python3

import argparse
import os
import time

AFL_DOCKER = 'afl-docker.py'
QSYM_DOCKER = 'qsym-docker.py'
SLAVE_NAME = 'afl-slave'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str,
                        help='fuzzing input directory')
    parser.add_argument('-o', '--output', type=str,
                        help='fuzzing output directory')
    parser.add_argument('-p', '--program', type=str,
                        help='fuzzing program directory')

    args = parser.parse_args()
    assert(os.path.exists(args.input))
    assert(os.path.exists(args.output))
    assert(os.path.exists(args.program))

    # qsym = ['qsym-docker.py', '-a', SLAVE_NAME,
      #       '-o', args.output, '-p', args.program]

    tmux_tag = 'afl-trio'

    afl_master_cmd = ['tmux', 'split-window', '-h',
                      AFL_DOCKER,
                      '-i', args.input,
                      '-o', args.output,
                      '-p', args.program,
                      '-M']
    afl_slave_cmd = ['tmux', 'split-window', '-h',
                     AFL_DOCKER,
                     '-i', args.input,
                     '-o', args.output,
                     '-p', args.program,
                     '-S', SLAVE_NAME]
    qsym_cmd = ['tmux', 'split-window', '-h',
                QSYM_DOCKER,
                '-a', SLAVE_NAME,
                '-o', args.output,
                '-p', args.program]
    os.system(' '.join(afl_master_cmd))
    time.sleep(1)
    os.system(' '.join(afl_slave_cmd))
    time.sleep(1)
    os.system(' '.join(qsym_cmd))


if __name__ == '__main__':
    main()
