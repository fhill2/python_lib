
from f.util import pp

links = {
    "links": [],
    "dirs": {
        "zsh": {
            "links": [],
            "dirs": {}
        },
    },
}



class FSTree():
    """Access and Insert Into a Nested File Structure"""
    def __init__():
        self.obj = {}


    def _insert_recur(self, obj, path): 
        if not path:
            return obj

        key = path.pop(0)

        # create the dict if it does not exist
        if key not in obj:
            obj[key] = {
                "links": [],
                "dirs": {}
            }

        self._insert_recur(obj[key], path)
        
    
    def insert(self, path):
        """insert into nested file structure, recreate directory if it does not exist"""
        return self.insert_recur(self.obj, path)


    def _get_recur(self, obj, path):
        key = path.pop(0)
        # raise KeyError("The object at path {} does not exist.".format(path))
        return self._get_recur(obj[key], path)
    
    def get(self, path):
        return self._get_recur(self.obj, path)


notes = [
    {"relative_subdir_paths": ["apps", "zsh"]}]

for note in notes:
    print(note)
    tree = FSTree()
    tree.insert(note["relative_subdir_paths"])
    
    cwd = get_value_recursively(links, )
    print(cwd)

pp(links)






###################################


# def get_value_recursively(obj, path):
#     """
#     Get the value of a nested object using dot notation.
#     Args:
#         obj: The object to access.
#         path: A list of subpaths to the value to get.

#     Returns:
#         The value of the nested object.
#     """

#     if not path:
#         return obj

#     key = path.pop(0)

#     # create the dict if it does not exist
#     if key not in obj:
#         obj[key] = {
#             "links": [],
#             "dirs": {}
#         }

#     return get_value_recursively(obj[key], path)

#     # if isinstance(obj, dict):
#     #     return get_value_recursively(obj[key], path)
#     # elif isinstance(obj, list):
#     #     return get_value_recursively(obj[int(key)], path)
#     # else:
#     #     raise ValueError("The object at path {} is not a dict or list.".format(path))

# links = [
# {
#    type = "link"
# },
# {
#    type = "directory"
# }
# ]