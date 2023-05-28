from notes_links import notes_get_links
from lib.native_client import send_message

def prettyprint(dict):
    for d in dict.values():
        print(d)

def notes_links_sync():
    links = notes_get_links()
    bookmarks = send_message("get_notes_bookmarks", "")
    firefox_bookmark_urls_to_remove = list(bookmarks.keys() - links.keys())
    print("removing bookmarks...")
    for url in firefox_bookmark_urls_to_remove:
        mark = bookmarks[url]
        res = send_message("remove_bookmark", {"id": mark["id"]})
        print(res)

    print("creating bookmarks...")
    firefox_bookmark_urls_to_create = list(links.keys() - bookmarks.keys())
    for url in firefox_bookmark_urls_to_create:
        link = links[url]
        del link["path"] # this key isnt needed anymore
        res = send_message("create_notes_bookmark", link)
        print(res)



    existing_firefox_bookmarks_urls = set(bookmarks.keys()).intersection(set(links.keys()))
    print("updating existing bookmarks...")
    for url in existing_firefox_bookmarks_urls:
        bookmark = bookmarks[url]
        link = links[url]

        update_opts = {}
        if "title" in link:
            if "title" not in bookmark or link["title"] != bookmark["title"]:
                update_opts["title"] = link["title"]

        if "tags" in link:
            if "tags" in bookmark:
                tagsToCreate = list(set(link["tags"]) - set(bookmark["tags"])) 
                if tagsToCreate: # if the list is empty, an empty list wont be added to update_opts
                    update_opts["tagsToCreate"] = tagsToCreate

                tagsToRemove = list(set(bookmark["tags"]) - set(link["tags"]))
                if tagsToRemove:
                    update_opts["tagsToRemove"] = tagsToRemove
            else:
                update_opts["tagsToCreate"] = link["tags"]
        
        if update_opts != {}:
            print(update_opts)
            update_opts["url"] = url
            update_opts["id"] = bookmark["id"]
            res = send_message("update_bookmark", update_opts)
            print(res)

def stars_sync():
    pass

# notes_links_sync()



