from f.github import get_raw_stars
from f.native_client import send_message

def prepare_stars(raw_stars):
    """as browser extension needs to receive message in a dict like format"""
    """also adds stars tag onto every stars bookmark"""
    stars = {}
    for raw_star in raw_stars:
        url = raw_star["html_url"]
        starred_at = raw_star["starred_at"]
        description = raw_star["description"]
        title = "[" + starred_at + "]"
        if description:
            title = title + " " + description


        stars[url] = { 
            "url" : url,
            "title": title,
            "tags" : ["stars"]
        }
    return stars

def stars_firefox_sync():
    # stars = get_star_urls() # list
    # stars = get_raw_stars()
    stars = prepare_stars(get_raw_stars())
    bookmarks = send_message("get_stars_bookmarks", "") # dict
    starsToCreate = list(set(stars) - set(bookmarks.keys()))
    starsToRemove = list(set(bookmarks.keys()) - set(stars))
    print("creating bookmarks...")
    for url in starsToCreate:
        send_message("create_stars_bookmark", stars[url])
    print("removing bookmarks...")
    for url in starsToRemove:
        send_message("remove_bookmark", {"id": bookmarks[url]["id"]})



stars_firefox_sync()
