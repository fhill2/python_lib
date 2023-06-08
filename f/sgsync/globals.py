
import os
from pathlib import Path
home = str(Path.home())
from f.password import get_pass

CONFIG_DIR = os.path.join(home, ".config", "sgsync")
PLUGIN_DIR = os.path.join(home, ".local/share/nvim/site/pack/packer")
REPO_TAG_DIR = os.path.join(home, "repos-tags")
# SCRIPT_DIR = Path( __file__ ).absolute().parent
SOURCEGRAPH_REPO_DIR = os.path.join(home, ".sourcegraph", "data", "repos", "github.com")
SOURCEGRAPH_DIR = os.path.join(home, ".sourcegraph")
SOURCEGRAPH_REPOS_JSON = os.path.join(SOURCEGRAPH_DIR, "data", "repos.json")
GITHUB_TOKEN = get_pass("gh/ghapi-pat")
SOURCEGRAPH_URL = "http://127.0.0.1:7080/.api/graphql"
SOURCEGRAPH_TOKEN = get_pass("src/graphql-pat")

