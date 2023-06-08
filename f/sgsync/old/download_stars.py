import multiprocessing, subprocess
from shutil import which

def get_token():
    if which("pass") is not None:
        return subprocess.run(['pass', 'show', 'gh/starfarm-pat'], capture_output=True).stdout.decode('utf-8').strip()
    else:
        return "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

TOKEN = get_token()
from ghapi.all import GhApi, pages, paged
api = GhApi(token=TOKEN)
# ========== SCRIPT ==========


def download_stars_subprocess(stars):
    repos_first_page  = api.activity.list_repos_starred_by_authenticated_user()
    repos = pages(api.activity.list_repos_starred_by_authenticated_user, api.last_page()).concat()
    # for repo in repos:
        # if "full_name" in repo:
            # stars.append(repo["full_name"].lower())


manager = multiprocessing.Manager()
stars = manager.list()
def download_stars():
        p = multiprocessing.Process(target=download_stars_subprocess, args=([stars]))
        p.start()
        return p.join, stars
