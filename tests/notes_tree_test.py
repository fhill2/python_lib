notes = [{"relative_subdir_paths": ["apps", "zsh"]}]
from f.util import pp

links = {}



for note in notes:
    for subpath in note["relative_subdir_paths"]:
        try:
            cwd = links[subpath]
        except KeyError as e:
            print("KeyError")
            cwd = { "dirs": [], "links": []}
        links[subpath] = cwd

pp(links)