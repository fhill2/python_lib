from globals import SOURCEGRAPH_REPO_DIR, REPO_TAG_DIR, PLUGIN_DIR
import subprocess, os
from f.util import run_sh
from f.fs import git_dirs
from util import symlink

def get_packer():
    """gets fullnames of all packer plugins as a list"""
    """important: repo["full_name"] keeps case - the key it is stored under is forced to lower()"""
    """so the name of the repo in the packer plugin list can be used as a source to symlink for syms"""
    plugins = {}
    # for abs in run_sh(["starfarm_find_git_repos " + PLUGIN_DIR]):
    for abs in git_dirs(PLUGIN_DIR):
        name = os.path.relpath(abs, PLUGIN_DIR) # no lower case on purpose
        # name = name.startswith("start/") and name.replace("start/", "") or name.replace("opt/", "")
        sub = name.split("/")[0]

        # get repo owner from git config shell command for each subdir of plugin dir
        cmd_str = "git config --get remote.origin.url"
        output = subprocess.run(["zsh", "-c", cmd_str], capture_output=True, cwd=abs).stdout.decode('utf-8').strip()
        full_name = output.replace("https://github.com/", "").replace("git@github.com:", "").replace(".git", "")
        plugins[full_name.lower()] = { "sub" : sub, "full_name" : full_name }

    return plugins


def sync_syms(repos):
    """important: under repos the fullname is all lowercase as this is what is returned from gh api"""
    """yet packer plugs are not lowercase - so the comparison needs to be done lowercase and the returned result without it"""
    plugins = get_packer()
    plugins_lower = [plug["full_name"].lower() for plug in plugins.values()]

    for [full_name, repo] in repos.items():
        # iterate all repos, if tag isnt found as a symlink in REPO_TAG_DIR, create symlink
        for tag in repo["config_tags"].copy():
            if tag not in repo["config_syms"]: # config_syms = fs syms that already exist
                full_name = repo["name"]
                if full_name in plugins_lower:
                    plug = plugins[full_name]
                    name = plug["full_name"].split("/")[1]
                    source = os.path.join(PLUGIN_DIR, plug["sub"], name) # use the full name that keeps case
                    print("repo exists in packer plugin, changing source: ", source)
                else:
                    source = os.path.join(SOURCEGRAPH_REPO_DIR, full_name)

                dest = os.path.join(REPO_TAG_DIR, tag, full_name.replace("/", "#"))
                symlink(source, dest)
                repo["config_tags"].append(tag)

        for tag in repo["config_syms"]:
            if tag not in repo["config_tags"]:  
                # if there is a sym that exists on filesystem, but not a corresponding tag in tags.yaml
                # print("deleting" + repo["full_name"] + " from " + str(os.path.join(REPO_TAG_DIR, tag)) )
                target = os.path.join(REPO_TAG_DIR, tag, full_name.replace("/", "#"))
                print("deleting " + target)
                os.remove(target)





# OLD
# def get_packer():
#     def opt_start(opt_start):
#         folder = os.path.join(PLUGIN_DIR, opt_start)
#         dirs = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
#         cmd_str = ""
#         for dir in dirs:
#             cmd_str += "cd " + dir + " && git config --get remote.origin.url && cd .. && "
#         cmd_str += "exit"
#         output = subprocess.run(["zsh", "-c", cmd_str], capture_output=True, cwd=folder).stdout.decode('utf-8')
#         return output.replace("https://github.com/", "").replace("git@github.com:", "").replace(".git", "")
#
#     # returns as repos = ["owner/repo", "owner/repo"]
#     repos = (opt_start("start") + opt_start("opt")).split("\n")
#
#     # remove empty strings in list
#     while ("" in repos):
#         repos.remove("")
#
#     plugins = []
#     for repo_str in repos:
#         repo_str = repo_str.lower()
#         owner_name = repo_str.split("/")
#         plugins.append({
#             'owner': owner_name[0],
#             'name': owner_name[1],
#             'full_name': repo_str
#         })
#     return plugins

