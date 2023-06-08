#!/usr/bin/python

# ========== GLOBALS ==========
# from farm import Repo
from globals import home, CONFIG_DIR, REPO_TAG_DIR, GITHUB_TOKEN, SOURCEGRAPH_TOKEN, SOURCEGRAPH_URL, SOURCEGRAPH_REPOS_JSON
import json, os, yaml, re, copy
from f.util import run_sh

from python_graphql_client import GraphqlClient
client = GraphqlClient(endpoint=SOURCEGRAPH_URL)
client.headers = {"Authorization": "token " + SOURCEGRAPH_TOKEN}

from f.github import get_raw_stars, get_org




new_repo_template = { 
        "in_stars" : False, # if the repo is starred on my github account
        "config_tags":  [], # the tags that exists in the tags.yaml file
        "config_syms": [], # the syms that currently exist to represent the tags in the REPO_TAG_DIR directory
        "sourcegraph_tags" : [] } # the KeyValuePairs graphQL metadata in the sourcegraph local server 


# ========== SCRIPT START ==========
# get github stars
def get_github_stars(repos):
    print("getting stars...")
    stars = get_raw_stars()
    for star in stars:
        name = star["full_name"].lower()
        repos[name] = copy.deepcopy(new_repo_template)
        repos[name]["in_stars"] = True 
        repos[name]["name"] = name
    return repos

# ========== GET_TAGS_CONFIG ==========
def load_yaml_file(path):
    with open(os.path.join(CONFIG_DIR, path)) as f:
        file = yaml.safe_load(f)
    return file if file is not None else []

def parse_tag_block(tags_config, repos, tag, tagged_repos):
    for full_name in tagged_repos:
        if full_name is not None:
            full_name = full_name.lower()
        else:
            continue

        # if entry is an org, get all the repos under the org
        if "/" not in full_name:
            for org_repo in get_org(full_name):
                tags_config[tag].append(org_repo.lower())
            tagged_repos.remove(full_name)
            continue
        # because the repo might not exist in stars 
        # it might have been added to tags.yaml manually
        if full_name not in repos.keys():
            repos[full_name] = copy.deepcopy(new_repo_template)
            repos[full_name]["name"] = full_name

        if "*" in tag:
            # does the same thing, in the future handle this to not star repos
            repos[full_name]["config_tags"].append(tag.replace("*", ""))
        else:
            repos[full_name]["config_tags"].append(tag)
    return tags_config, repos

def get_single_tags_config_file(repos, abs):
    print("getting tags...")
    tags_config = load_yaml_file(abs)
    if tags_config is None:
        print("Failed to parse tags.yaml")
        exit()

    for [tag, tagged_repos] in tags_config.items():
        tag = tag.strip()
        if " " in tag:
            for multitag in tag.split(" "):
                tags_config, repos = parse_tag_block(tags_config, repos, multitag, tagged_repos)
        else:
            tags_config, repos = parse_tag_block(tags_config, repos, tag, tagged_repos)


def get_tags_config(repos):
    all_tags_files = [os.path.join(CONFIG_DIR, "tags.d", file) for file in os.listdir("/home/f1/.config/sgsync/tags.d") if file.endswith(".yaml") or file.endswith(".yml")]
    all_tags_files.append(os.path.join(CONFIG_DIR, "tags.yaml"))
    for tags_file in all_tags_files:
        get_single_tags_config_file(repos, tags_file)
        
    # also identify untagged / unsorted repos that have been starred
    for [full_name, repo] in repos.items():
        # if repo["in_stars"] and len(repo["config_tags"]) == 0:
        if len(repo["config_tags"]) == 0:
            # repo["unsorted"] = True
            repo["config_tags"].append("unsorted")

    return repos

def get_tag_syms(repos):
    """gets all symlinked repos under REPO_TAG_DIR"""
    for sym_abs in run_sh(["cd " + REPO_TAG_DIR + " && fd -a --type=l"]):
        if sym_abs == "" or "/dotfiles_sym/" in sym_abs:
            continue
        full_name = os.path.basename(sym_abs).replace("#", "/")
        tag = os.path.relpath(os.path.dirname(sym_abs), REPO_TAG_DIR)
        # if a repo has been added to tags.yaml but has not been starred 
        # (starring creates a key under repos) a key error will occur here 
        if full_name not in repos.keys():
            repos[full_name] = copy.deepcopy(new_repo_template)
            repos[full_name]["name"] = full_name
        repos[full_name]["config_syms"].append(tag)

    return repos



def get_sourcegraph_repos(repos):
    print("getting sourcegraph repos...")
    query = """
        {
        repositories() {
            nodes {
            name
            id
            keyValuePairs { key, value }
            }
        }
        }
    """

    try:
        res = client.execute(query=query)
    except:
        print("sourcegraph server not running..")
        return repos

    for sourcegraph_repo in res["data"]["repositories"]["nodes"]:
        full_name = re.search(r"/.*$", sourcegraph_repo["name"]).group()[1:].lower()
        # intentionally do not create new repos for sourcegraph repos here
        # as I want a one way sync: stars tags -> sourcegraph
        if full_name in repos:
            repos[full_name]["sourcegraph_id"] = sourcegraph_repo["id"]
            for tag in sourcegraph_repo["keyValuePairs"]:
                repos[full_name]["sourcegraph_tags"].append(tag["key"])
        
    return repos

def get_sourcegraph_repos_config():
    """as I cant get the sourcegraph : merge / combine syntax working for repos json files"""
    """this reads the repos config template from dotfiles, appends the sourcegraph token from pass before the repos are written"""
    with open(os.path.join(CONFIG_DIR, "repos.json"), "r") as f: 
        print(SOURCEGRAPH_REPOS_JSON)
        try:
            config = json.loads(f.read())
        except json.decoder.JSONDecodeError as e:
            print("ERROR: loading config - check for additional commas or validate json")
            print(e)
            exit()

    config["GITHUB"][0]["token"] = GITHUB_TOKEN
    return config

def get_repos():
    # make sure get_tag_syms is last - as it iterates all repos to find repos that dont have tags (unsorted)
    return get_tag_syms(get_sourcegraph_repos(get_tags_config(get_github_stars({}))))


