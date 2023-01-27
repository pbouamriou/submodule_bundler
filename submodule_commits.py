#!/usr/bin/env python3
""" Print the commit of each submodule (recursively) at some commit"""

import os
import argparse
import subprocess
import re


def print_submodule_commits(parent_dir, root_subdir, root_commit):
    for result in submodule_commits(parent_dir, root_subdir, root_commit):
        print(f'{result["subdir"]} {result["commit"]}')


def submodule_commits(parentdir='', subdir='.', commit='HEAD', prefix=''):
    subdir_path = os.path.join(parentdir, subdir)
    git_ls_tree = subprocess.check_output(
        ['git', 'ls-tree', '-r', commit], cwd=subdir_path)
    ls_tree_lines = filter(None, git_ls_tree.decode("utf-8").split("\n"))
    submodule_regex = re.compile(r'^[0-9]+\s+commit')
    for line in ls_tree_lines:
        if submodule_regex.match(line):
            line_split = line.split()
            commit_hash = line_split[2]
            subdirectory = line_split[3]
            submodule_prefix = subdirectory
            if prefix != '':
                submodule_prefix = f'{prefix}/{subdirectory}'
            yield {'subdir': submodule_prefix, 'commit': commit_hash}
            yield from submodule_commits(subdir_path, subdirectory, commit_hash, submodule_prefix)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Print the commit of each submodule (recursively) at some commit')
    parser.add_argument('commit', metavar='commit_hash', type=str, default='HEAD', nargs='?',
                        help='commit to examine; defaults to HEAD')
    args = parser.parse_args()
    print_submodule_commits(os.getcwd(), '.', args.commit)
