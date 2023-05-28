# https://github.com/ant-arctica/rofi-bookmarks/blob/main/rofi-bookmarks.py
import sqlite3
from contextlib import closing, contextmanager 
from tempfile import NamedTemporaryFile
from pathlib import Path
from shutil import copyfile
firefox_dir = Path.home() / '.mozilla/firefox'

from configparser import ConfigParser

def find_firefox_config():
    installs = ConfigParser()
    installs.read(firefox_dir / 'installs.ini')
    return firefox_dir / installs["6BA5C87ECB35E12F"]['Default']

@contextmanager
def temp_sqlite(path):
    with NamedTemporaryFile() as temp_loc:
        copyfile(path, temp_loc.name)
        with closing(sqlite3.connect(temp_loc.name)) as conn:
            yield conn

# def read_bookmarks():
#     with temp_sqlite(find_firefox_config() / 'places.sqlite') as places:
#             res = places.execute("""SELECT moz_bookmarks.id, moz_bookmarks.parent, moz_bookmarks.fk, moz_bookmarks.type, moz_bookmarks.title, moz_places.url FROM moz_bookmarks LEFT JOIN moz_places ON moz_bookmarks.fk=moz_places.id""").fetchall()
#     bookmarks = []
#     for mark in res:
#         bookmarks.append({ 
#             "id": mark[0], 
#             "parent": mark[1], 
#             "fk": mark[2],
#             "type": mark[3],
#             "title": mark[4],
#             "url": mark[5]
#         }) 
#     return bookmarks

def read_bookmarks():
    moz_places = {}
    moz_bookmarks = []
    with temp_sqlite(find_firefox_config() / 'places.sqlite') as places:
                # res = places.execute("""SELECT moz_bookmarks.id, moz_bookmarks.parent, moz_bookmarks.fk, moz_bookmarks.type, moz_bookmarks.title, moz_places.url FROM moz_bookmarks LEFT JOIN moz_places ON moz_bookmarks.fk=moz_places.id""").fetchall()
                res = places.execute("""SELECT moz_places.id, moz_places.url, moz_places.title FROM moz_places""").fetchall()
                for mark in res:
                    moz_places[mark[0]] = {"url": mark[1], "title": mark[2]}
                res = places.execute("""SELECT moz_bookmarks.id, moz_bookmarks.guid, moz_bookmarks.parent, moz_bookmarks.fk, moz_bookmarks.type, moz_bookmarks.title FROM moz_bookmarks""").fetchall()
                for mark in res:
                    moz_bookmarks.append({ 
                        "id": mark[0], 
                        "guid" : mark[1],
                        "parent": mark[2], 
                        "fk": mark[3],
                        "type": mark[4],
                        "title": mark[5],
                    })
    return moz_places, moz_bookmarks

moz_places, moz_bookmarks = read_bookmarks()

def get_bookmarks():
    """gets all bookmarks that exist"""
    """builds on read bookmarks"""
    """merges tags + bookmarks from both moz_places and moz_bookmarks table in sqlite"""
    global moz_places, moz_bookmarks


    # differences between entries in moz_bookmarks table of places.sqlite
    # # type=2, parent=4 -> a tag
    tags = {
       # id: title
    }
    # # type=1, title=NOT None -> a regular bookmark
    bookmarks = {
        # fk: {}
    }
    # # type=1, title=None -> an entry that links a tag entry to a bookmark entry

    # parentId or Id in firefox API docs = GUID
    # it is not the ID used in the firefox database

    for mark in moz_bookmarks:
        if mark["type"] == 2 and mark["parent"] == 4:
            tags[mark["id"]] = mark["title"]

        if mark['type'] == 1 and mark["title"] is not None:
            print("added bookmark")
            bookmarks[mark["fk"]] = {
                "parent": mark["parent"],
                "title" : moz_places[mark["fk"]]["title"],
                "url" : moz_places[mark["fk"]]["url"],
                "tags" : [],
                "guid": mark["guid"]
            }

        # if mark["type"] == 2 and mark["title"] == "promnesia":
        #     promnesia_folder_id = mark[""]

    for mark in moz_bookmarks:
        if mark["parent"] in tags.keys():
            # print(mark["fk"])
            if mark["fk"] not in bookmarks:
                # because bookmarks on bookmarks tolbar arent in moz_bookmarks (i think)
                bookmarks[mark["fk"]] = {
                    "parent" : None, # bookmarks on toolbar therefore have no parent 
                    # as parent column only exists in moz_bookmarks table
                    "title" : moz_places[mark["fk"]]["title"],
                    "url" : moz_places[mark["fk"]]["url"],
                    "tags" : [],
                    "guid": mark["guid"]
                }
            
            bookmarks[mark["fk"]]["tags"].append(tags[mark["parent"]])

    for mark in bookmarks.values():
        print(mark)
        # if mark["parent"] == 718:
            # print(mark)
           
    return bookmarks


def list_to_dict(list, key):
    dict = {}
    for item in list:
        dict[item[key]] = item
    return dict

def get_promnesia_folder(bookmarks):
    """gets bookmarks menu > promnesia folder in moz_bookmarks"""
    for mark in moz_bookmarks:
        if mark["type"] == 2 and mark["title"] == "promnesia":
            return mark

# get_bookmarks( using old database)


def get_bookmarks_folder():
    """gets all bookmarks under a folder existing in bookmarks menu"""
    global moz_bookmarks
    prom_folder = get_promnesia_folder(moz_bookmarks)
    prom_id, prom_guid = prom_folder["id"], prom_folder["guid"]
    bookmarks = get_bookmarks()
    # print(bookmarks.values())
    # print(bookmarks)
    
    # if a bookmark is in a folder, the parent of the bookmark entry will be set to the id of the folder entry
   
    # for mark in bookmarks.values():
        # print(mark)
        # if mark["parent"] == prom_id:
            # print(mark)
    # prom_folder_bookmarks_list = [mark for mark in bookmarks.values() if mark["parent"] == prom_id]
    # print(prom_folder_bookmarks_list)
    # print(prom_id)
    # prom_folder_bookmarks = list_to_dict(prom_folder_bookmarks_list, "url"),
    # return prom_folder_bookmarks, prom_guid


if __name__ == "__main__":
    read_bookmarks()

    
