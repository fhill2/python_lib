from f.util import run_sh
from globals import REPO_TAG_DIR
import os, re
from util import symlink


def get_owner_hash_name(abs):
    """extracts owner name from filepath - fd output"""
    abs_split = abs.split("#")
    left = abs_split[0].split("/")
    right = abs_split[1].split("/")
    return "#".join([left[-1], right[0]])

def symlink_dotfiles_by_folder_name(foldername):
    """symlinks all folders existing within symlinked dotfiles to dotfiles_sym"""
    DOTFILES_SYM_DIR = os.path.join(REPO_TAG_DIR, "dotfiles_sym")
    os.makedirs(DOTFILES_SYM_DIR, mode = 0o777, exist_ok=True)
    for source in run_sh("fd -L -a -t d -g " + foldername, REPO_TAG_DIR + "/dotfiles"):
        # ignore any directories returned that are tag sub directories and not repos
        if "#" not in source:
            continue
        owner_hash_name = get_owner_hash_name(source)
        target = os.path.join(DOTFILES_SYM_DIR, foldername, owner_hash_name)
        symlink(source, target)


