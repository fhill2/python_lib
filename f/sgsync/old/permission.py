import os
from globals import REPO_TAG_DIR, SOURCEGRAPH_REPO_DIR

from f.util import run_sh
import subprocess
#
#
# MAX_DEPTH = 3
# for root, dirs, files in os.walk(SOURCEGRAPH_REPO_DIR, topdown=True):
#     print("there are", len(files), "files in", root)
#     if root.count(os.sep) - SOURCEGRAPH_REPO_DIR.count(os.sep) == MAX_DEPTH - 1:
#         del dirs[:]


# for abs in run_sh(["starfarm_find_git_repos " + SOURCEGRAPH_REPO_DIR]):
#     os.chdir(abs) # chdir changes the cwd of all child processes
#     run_sh("if [ $(git worktree list | wc -l) -lt 2 ]; then git worktree add wt; fi")

print(os.listdir("/home/f1/.sourcegraph/data/repos/github.com/i3/i3"))

