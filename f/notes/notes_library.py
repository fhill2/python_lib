import os

from notes.globals import NOTES_DIR, NOTES_TAG_DIR
from notes.note import Note

from f.util import pp

def _find_difference(a, b):
    # returns everything in a that isnt in b
    diffs = {}
    for tag in a.keys():
        if tag in a and tag in b:
            diff = list(set(a[tag]).difference(set(b[tag])))
            if diff:
                diffs[tag] = diff
        else:
            diffs[tag] = a[tag]
    return diffs


class FSTree():
    """a simple tree structure that represents a filesystem"""
    """all links and subdirectories of notes go in here"""
    """this is then passed to raindrop to generate the nested folder structure"""
    def insert():
        # check if the "directories" exist, if they dont, create the objects

class NoteLibrary():
    """collection of methods that operate over the entire notes collection/library"""
    def __init__(self):
        self.notes = []
        # for every absolute path under NOTES_DIR, instantiate a Note() class for it.
        for note in self.get_all_notes():
            self.notes.append(Note(abs=note))

        # pre checks
        self.make_subdirs_lowercase(NOTES_DIR)


    def make_subdirs_lowercase(self, directory):
        """Makes all subdirectories within NOTES_DIR lowercase."""

        def contains_upper(str):
            """if string contains an uppercase character"""
            for character in str:
                if character.isupper():
                    return True
            return False

        for subdir in os.listdir(directory):
            # Check if the subdirectory is a directory.
            if os.path.isdir(os.path.join(directory, subdir)):
                # if the subdirectory contains an uppercase character
                if contains_upper(subdir):
                    # Make the subdirectory lowercase.
                    new_subdir = subdir.lower()
                    source = os.path.join(directory, subdir)
                    target = os.path.join(directory, new_subdir)
                    print("ENFORCE LOWERCASE NOTE DIRS: Renaming: {} --> {}".format(source, target))
                    os.rename(source, target)
                    # recurse into the subdirectories directories
                    self.make_subdirs_lowercase(os.path.join(directory, new_subdir))
                else:
                    self.make_subdirs_lowercase(os.path.join(directory, subdir))
    
    def remove_empty_directories(self, directory):
        dirs = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
        for dir in dirs:
            sub = os.path.join(directory, dir)
            if not os.listdir(sub):
                os.rmdir(sub)

    def get_all_notes(self, filter_subdir=None):
        """gets all notes within NOTES_DIR"""
        return self._get_all_notes(NOTES_DIR, filter_subdir)

    def _get_all_note_syms_from_filesystem(self):
        """gets all note symlinks within NOTES_TAG_DIR"""
        """this is used to compare the generated symlink targets with, to determine what notes need to be added/removed"""
        return self._get_all_notes(NOTES_TAG_DIR)


    def _get_all_notes(self, dir, filter_subdir=None):
        """gets all notes within NOTES_DIR or NOTES_TAG_DIR"""
        """optionally pass a root directory of NOTES_DIR -> 1,2,3,4,sort"""
        """this retrieves all notes only within that sub directory"""
        notes = []
        searchpath = os.path.join(dir, filter_subdir) if filter_subdir else dir
        for root, dirnames, filenames in os.walk(searchpath):
            for filename in filenames:
                if filename.endswith(".norg") or filename.endswith(".md"):
                    notes.append(os.path.join(root, filename))
        return notes

    def create_note_syms(self):
        # gather all symlink targets for the note
        targets = []
        for note in self.notes:
            list.extend(targets, note._generate_sym_targets())
            note._symlink_targets()

        # get note sym on filesystem to compare to generated targets
        # for every note sym in NOTES_TAG_DIR, check if the path exists in generated target
        for sym in self._get_all_note_syms_from_filesystem():
            if sym not in targets:
                print("REMOVING: {}".format(sym))
        
        # there might be empty directories left in NOTES_TAG_DIR
        self.remove_empty_directories(NOTES_TAG_DIR)
    
    # LinkExtractor Methods Below Here
    def _remove_yt_links(self, links):
        """because promnesia canonify does not remove timestamps so getting links from notes creates a lot of duplicate links"""
        """for every unique URl string (identified by the unique code in the URL) - it only keeps 1 bookmark for each"""
        """- with no timestamp"""
        """- with the lowest time stamp"""
        """this only works as links dict is sorted alphabetically putting time urls in order from lowest to highest"""
        """input: links {}"""

        def extract_yt_id_time(url):
            # extract id and time from youtube url
            id_time = url.split("?v=")[1].split("&t=")
            id = id_time[0]
            try:
                time = int(id_time[1])
            except:
                time = None
            return id, time

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

    def get_all_links(self):
        """get all links / urls from every notes files in the notes library"""
        """structure the data like a filesystem (nested tree structure)"""
        """this is so the result (links object) can be passed to raindrop API and can be easily iterated over to create the links there"""
        links = {}
        for note in self.notes:
            tags = note.post.metadata["tags_fs"]
            # for url in note._get_links():
            #     links[url] = { "tags" : [], "url": url, "path": note.abs, "subpath": note.relative_subdir_paths }
                
            #     # if tags already exist from a pre existing duplicate link, then append to the existing list of tags
            #     if "tags" in links[url]:
            #         for tag in tags:
            #             if tag not in links[url]["tags"]:
            #                 links[url]["tags"].append(tag)
            #     else:
            #         # otherwise overwrite the tags of the link object
            #         links[url]["tags"] = tags
            
            # create the objects ("directories") on the links object if they do not exist
            for subpath in note.relative_subdir_paths:
                try:
                    cwd = links[subpath]
                except KeyError as e:
                    cwd = {}
            #for url in note._get_links():
                
        links = self._remove_yt_links(links)
        pp(links)


# DEPRECATED
# def write_all_subdir_tags(self):
#     """adds all subdir tags"""
#     for note in self.notes:
#         note.write_subdir_tags()