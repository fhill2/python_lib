# https://xplr.dev/en/awesome-plugins
# syncs all plugins from this page and stars them

import requests
from bs4 import BeautifulSoup
from f.github import star


def get_xplr_plugins():
    """gets all xplr plugins from xplr.dev/en/awesome-plugins"""
    url = 'https://xplr.dev/en/awesome-plugins'
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    xplr_plugins = []
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if "//github.com/" not in href:
            continue
        if href.endswith(".xplr"):
            xplr_plugins.append(href.replace("https://github.com/", "").lower())
    return xplr_plugins


def sync_xplr_plugins(repos):
    xplr_plugins = get_xplr_plugins()
    for xplr_plug in xplr_plugins:
        if xplr_plug not in repos.keys():
            star(xplr_plug)
            


