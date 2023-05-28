
# notes_get_links
# import sys
# sys.path.append("/home/f1/dev/bin")
from notes_frontmatter import get_all_notes, get_frontmatter, get_tags_from_frontmatter
# from promnesia.sources.markdown import extract_from_file
from notes_extract_links import extract_from_file
from promnesia.cannon import canonify
import re


def extract_yt_id_time(url):
    # extract id and time from youtube url
    id_time = url.split("?v=")[1].split("&t=")
    id = id_time[0]
    try:
        time = int(id_time[1])
    except:
        time = None
    return id, time

def list_to_dict(links):
    dict = {}
    for link in links.values():
        dict[link["url"]] = link
    return dict

yt = {}
def remove_yt_links(links):
    """because promnesia canonify does not remove timestamps so getting links from notes creates a lot of duplicate links"""
    """for every unique URl string (identified by the unique code in the URL) - it only keeps 1 bookmark for each"""
    """- with no timestamp"""
    """- with the lowest time stamp"""
    """this only works as links dict is sorted alphabetically putting time urls in order from lowest to highest"""
    """input: links {}"""
    last_id = ""
    urls_to_remove = []
    for url in links.keys():
        if "youtube.com/watch?v=" in url and not "&list=PL" in url:
            id, time = extract_yt_id_time(url)
            if id == last_id:
                urls_to_remove.append(url)
            last_id = id

    for url in urls_to_remove:
        del links[url]

    return links

def validate_url(url):
    """links from notes have to be manipulated for sync to successfuly compare urls"""
    """when a bookmark is saved in firefox: """
    """Google.com/ -> google.com"""

    # ignore local only / non web links
    if "ytlink" in url:
        return False

    # split the url so I can manipulate scheme/address/tail individually
    url_sections = re.split('(\/)', url) # string split keep delimiter
    url_sections = list(filter(None, url_sections)) # because above can create empty strings

    # firefox forces lowercase on the address portion of the bookmark
    url_sections[3] = url_sections[3].lower()

    # firefox appends / to every bookmark in format https://google.com
    if len(url_sections) == 4:
        url_sections.append("/")
    return "".join(url_sections)


def validate_tags(tags):
    """there is an issue with adding a tag AA or aa"""
    """the case kept switching when firefox added the tag - cba to fix and dont need this tag anyway"""
    for tag in tags:
        if tag == "AA" or tag == "aa":
            tags.remove(tag)

    return tags


def notes_get_links():
    links = {}
    for note in get_all_notes():
        frontmatter = get_frontmatter(note)[0]
        tags = get_tags_from_frontmatter(frontmatter)

        for visit in extract_from_file(note):
            # as canonify outputs a normalized URL without the scheme prefixed
            scheme = re.match(r"^([\S]+):\/\/", visit.url)
            if scheme:
                url = scheme.group(1) + "://" + canonify(visit.url)
            else:
                url = canonify(visit.url)

            url = validate_url(url)
            if not url:
                break # if the url validator returned false, ignore the link (vlc links etc)
            
            # if url not in links:
            links[url] = { "tags" : [], "url": url, "path": note }

            # if tags already exist from a pre existing duplicate link, then append to the existing list
            if "tags" in links[url]:
                for tag in tags:
                    if tag not in links[url]["tags"]:
                        links[url]["tags"].append(tag)
            else:
                links[url]["tags"] = tags

            if "tags" in links[url]:
                links[url]["tags"] = validate_tags(links[url]["tags"])

    links = remove_yt_links(links)
    # for link in links:
    #     if "youtube.com/watch?v=" in link:
    #         print(link)

    return links

