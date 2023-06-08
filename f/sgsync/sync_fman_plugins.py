import sys, json, os, yaml
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from globals import CONFIG_DIR

# from fman core source code

def _get(url):
	try:
		return urlopen(url).read()
	except HTTPError:
		raise
	except URLError:
		# Fallback: Some users get "SSL: CERTIFICATE_VERIFY_FAILED" for urlopen.
		try:
			response = requests.get(url)
		except RequestException as e:
			raise URLError(e.__class__.__name__)
		if response.status_code != 200:
			raise HTTPError(
				url, response.status_code, response.reason, response.headers,
				None
			)
		return response.content


def _get_json(url):
	return json.loads(_get(url).decode('utf-8'))

def find_repos(topics):
    query = '+'.join('topic:' + topic for topic in topics)
    url = "https://api.github.com/search/repositories?q=" + query
    repos = []
    for repo in fetch_all_pages(url):
        if repo is not None:
            repos.append(repo["full_name"].lower())
    return repos
    # list(map(repo["full_name"], fetch_all_pages(url)))

def fetch_all_pages(json_url, page_size=100):
	for page in range(1, sys.maxsize):
		data = _get_json(json_url + '&per_page=%d&page=%d' % (page_size, page))
		yield from data['items']
		has_more = page * page_size < data['total_count']
		if not has_more:
			break


repos = find_repos(["fman", "plugin"])
print(repos)
output = { "python/fman/plugins": repos }
destination = os.path.join(CONFIG_DIR, "tags.d", "fman_plugins.yaml")
print(f"writing fman plugins to {destination}")
# TODO: WRITE THE SAME As TAGS.YAML WITH DIRECTORY KEY
with open(destination, "w") as f: 
    f.write(f'# Do not edit this file.. it is automatically generated\n{yaml.dump(output)}')
    # f.seek(1)
    # f.write(yaml.dump(output))