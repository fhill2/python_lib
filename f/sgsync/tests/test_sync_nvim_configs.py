# from sync_nvim_configs import sync_nvim_configs
from f.fs import git_dirs

for git_dir in git_dirs("/home/f1/.sourcegraph/data/repos"):
    print(git_dir)
