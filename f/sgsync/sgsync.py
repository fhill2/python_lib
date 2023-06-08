#!/usr/bin/python
from sync_syms import sync_syms
from sync_configs import symlink_dotfiles_by_folder_name
from sync_xplr_plugins import sync_xplr_plugins

from globals import home, CONFIG_DIR, SOURCEGRAPH_REPO_DIR, SOURCEGRAPH_TOKEN, SOURCEGRAPH_URL, SOURCEGRAPH_DIR, SOURCEGRAPH_REPOS_JSON
from f.util import run_sh
from f.fs import git_dirs
import json, yaml, os
from get import get_repos, get_sourcegraph_repos_config
from python_graphql_client import GraphqlClient
client = GraphqlClient(endpoint=SOURCEGRAPH_URL)
client.headers = {"Authorization": "token " + SOURCEGRAPH_TOKEN}

# TODO:
# add starring for repos in tags not starred

# PLAN:
# sort all repos
# sort repo world class uol, then go through final projects
# make sure i can sync script, adding new repos and then fuzzy on them

# ========== FUNCTIONS ==========

# setup folders incase they dont exist
os.makedirs(os.path.join(CONFIG_DIR, "tags.d"), mode = 0o777, exist_ok=True)
os.makedirs(os.path.join(SOURCEGRAPH_DIR, "data", "repos"), mode = 0o777, exist_ok=True)

def write_sourcegraph_config(full_names):
    print("writing all repos to sourcegraph repos.json")
    # do not read/write to dotfiles, as the json file contains the gh api key
    # for some reason merging the json files on sourcegraph startup isnt working

    # TODO: if file does not exist , script will error
    config = get_sourcegraph_repos_config()
    config["GITHUB"][0]["repos"] = list(full_names)
    with open(SOURCEGRAPH_REPOS_JSON, "w") as f: 
        # f.seek(0)
        f.write(json.dumps(config, indent=4))
        # f.truncate()

def write_tags_unsorted(full_names):
    with open(os.path.join(CONFIG_DIR, 'tags_unsorted.yaml'), 'w') as file:
        yaml.dump(full_names, file)

def add_sourcegraph_tag(tag, repoID):
    query = """
        mutation AddSecurityOwner($repoID: ID!, $tag: String!) {
            addRepoKeyValuePair(repo: $repoID, key: $tag, value: null) {
                alwaysNil
            }
        }"""
    variables = {
            "repoID": repoID,
            "tag": tag,
            }

    res = client.execute(query=query, variables=variables)

def delete_sourcegraph_tag(tag, repoID):
    query = """
            mutation AddSecurityOwner($repoID: ID!, $tag: String!) {
                deleteRepoKeyValuePair(repo: $repoID, key: $tag) {
                    alwaysNil
                }
            }"""
    variables = {
        "repoID": repoID,
        "tag": tag,
    }

    res = client.execute(query=query, variables=variables)


# ========= SCRIPT START ==========
repos = get_repos()

# find tags_unsorted then write
print("for stars not in tags -> write to tags_unsorted.yaml")
# untagged = [repo["name"] for repo in repos if "untagged" in repo]
# untagged = list(repo["name"] for repo in repos.values() if "untagged" in repo)
unsorted = list(repo["name"] for repo in repos.values() if "unsorted" in repo["config_tags"])
write_tags_unsorted(unsorted)

# write all repos to sourcegraph repos.json
write_sourcegraph_config(repos.keys())

# for tags that are in config, but not in sourcegraph
# add them to sourcegraph
for [full_name, repo] in repos.items():
    for config_tag in repo["config_tags"]:
        if config_tag not in repo["sourcegraph_tags"]:
            if "sourcegraph_id" in repo:
                print("add sourcegraph tag -> " + repo["name"] + " " + config_tag)
                add_sourcegraph_tag(config_tag, repo["sourcegraph_id"])
            else:
                print("add_sourcegraph_tag -> " + repo["name"] + " failed - no repo in sourcegraph")


    # for tags that are in sourcegraph, but not in config
    # delete them from sourcegraph
    for sourcegraph_tag in repo["sourcegraph_tags"]:
        if sourcegraph_tag not in repo["config_tags"]:
            print("delete sourcegraph tag -> " + repo["name"] + " " + sourcegraph_tag)
            delete_sourcegraph_tag(sourcegraph_tag, repo["sourcegraph_id"])

run_sh("systemctl --user restart sourcegraph.service")

#

print("ensuring all sourcegraph bare repos have a checked out worktree")
for abs in git_dirs(SOURCEGRAPH_REPO_DIR):
    # os.chdir(abs) # chdir changes the cwd of all child processes
    if "wt" not in os.listdir(abs):
        print(abs + " -> " + 'run_sh("sudo git worktree add wt")')
        run_sh("sudo git worktree add wt", abs)

# =========== generate / sync tag syms folder ==========
print("generating / syncing tag syms folder...")
sync_syms(repos)

print("creating nvim dotfiles symlinks..")
symlink_dotfiles_by_folder_name("nvim")
print("creating xplr dotfiles symlinks..")
symlink_dotfiles_by_folder_name("xplr")

print("starring xplr.dev/en/awesome-plugins all plugins")
sync_xplr_plugins(repos)


print("recursively chown f1 on sourcegraph repos..")
run_sh("cd ~/.sourcegraph/data && chown -R f1 repos")

#

