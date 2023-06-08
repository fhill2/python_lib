#from raindropiopy import API, Collection, CollectionRef, Raindrop

from password import get_pass
raindrop_access_token = get_pass("raindrop/python-api-secret")

import requests
from f.util import pp
import os

class HTTPRequest():
    def __init__(self):
        pass

    def get(self, url):
        # Create a dictionary of headers
        headers = {'Authorization': 'Bearer {}'.format(raindrop_access_token)}
        # Make the GET request
        response = requests.get(url, headers=headers)
        # Check the status code
        if response.status_code == 200:
            # The request was successful, so return the JSON resul
            return response.json()["items"]
        else:
            # The request failed, so raise an exception
            raise Exception(f'Request failed with status code {response.status_code}')



# CHILD COLLECTION
# {
#             "_id": 34757300,
#             "title": "a-second-child-collection",
#             "description": "",
#             "user": {
#                 "$ref": "users",
#                 "$id": 568168
#             },
#             "public": false,
#             "view": "list",
#             "count": 0,
#             "cover": [],
#             "expanded": false,
#             "creatorRef": {
#                 "_id": 568168,
#                 "name": "freddiehill000",
#                 "email": ""
#             },
#             "lastAction": "2023-05-29T18:57:25.384Z",
#             "created": "2023-05-29T18:57:25.384Z",
#             "lastUpdate": "2023-05-29T20:50:38.231Z",
#             "sort": 0,
#             "slug": "a-second-child-collection",
#             "parent": {
#                 "$ref": "collections",
#                 "$id": 34757212
#             },
#             "access": {
#                 "for": 568168,
#                 "level": 4,
#                 "root": false,
#                 "draggable": true
#             },
#             "author": true
#         },

# ROOT COLLECTION
# {
#             "_id": 34757282,
#             "title": "Sample collection",
#             "description": "",
#             "user": {
#                 "$ref": "users",
#                 "$id": 568168
#             },
#             "public": false,
#             "view": "list",
#             "count": 0,
#             "cover": [],
#             "expanded": true,
#             "creatorRef": {
#                 "_id": 568168,
#                 "name": "freddiehill000",
#                 "email": ""
#             },
#             "lastAction": "2023-05-29T18:54:26.599Z",
#             "created": "2023-05-29T18:54:26.600Z",
#             "lastUpdate": "2023-05-29T18:54:26.600Z",
#             "sort": 34757282,
#             "slug": "sample-collection",
#             "access": {
#                 "for": 568168,
#                 "level": 4,
#                 "root": false,
#                 "draggable": true
#             },
#             "author": true
#         },


class RaindropCollections(HTTPRequest):
    def __init__(self):
        self.collectionsList = []
        self.collectionsMap = {}

    def _get_all_collections(self):
        """get all root and child collections"""
        """return as id: title map"""
        list.extend(self.collectionsList, self.get("https://api.raindrop.io/rest/v1/collections"))
        list.extend(self.collectionsList, self.get("https://api.raindrop.io/rest/v1/collections/childrens"))
        
        # generate map _id = {collection_dict}
        for collection in self.collectionsList:
            self.collectionsMap[collection["_id"]] = collection

        # we can generate a subpath here by recursively looking up parent collection id title
        for collection in self.collectionsMap.values():
            if "parent" not in collection:
                continue
                # then it is a root collection, ignore it
            subpath_arr = []
            c = collection
            while "parent" in c:
                subpath_arr.insert(0, c["title"])
                c = self.collectionsMap[c["parent"]["$id"]]
            subpath_arr.insert(0, c["title"])
            collection["subpath"] = os.sep.join(subpath_arr)
            collection["subpath_arr"] = subpath_arr
        
        pp(self.collectionsMap)




class RaindropBookmarks(HTTPRequest):
    """syncs obsidian/bookmarks within markdown files with raindrop"""
    def __init__(self):
        # {"tag1": ["bookmark1", "bookmark2"], "tag2": ["bookmark3", "bookmark4"]}
        self.raindrop_bookmarks = {}

    def _get_notes_collection(self):
        """cannot find a way to return only the notes root collection"""
        """gets all root collections of raindrop"""
        collections = self.get("https://api.raindrop.io/rest/v1/collections")
        pp(collections)
        for collection in collections:
            if collection["title"] == "notes":
                self.notes_collection = collection
                return
 

    def _get_all_bookmarks(self):
        """gets all bookmarks within raindrop notes collection"""
        self._get_notes_collection()
        self.get("https://api.raindrop.io/rest/v1/raindrops/{}".format(self.notes_collection["_id"]))




#raindrop = RaindropBookmarks()
raindrop_collections = RaindropCollections()
raindrop_collections._get_all_collections()
#raindrop._get_notes_collection()
#raindrop._get_all_bookmarks()



# post_variables := map[string]interface{}{
# 		"collection": struct {
# 			Ref string `json:"$ref"`
# 			Id  int    `json:"$id"`
# 		}{"collections", collection_id},
# 		"link":    selection_map["url"],
# 		"title":   selection_map["title"],
# 		"tags":    tag_array,
# 		"excerpt": get_meta_description(selection_map["url"]),
# 	}
# 	post_json, _ := json.Marshal(post_variables)

# 	request, _ := http.NewRequest("POST", "https://api.raindrop.io/rest/v1/raindrop", bytes.NewBuffer(post_json))