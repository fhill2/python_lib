#!/usr/bin/python

from frontmatter.default_handlers import YAMLHandler
import frontmatter
import os
from f.util import dump
from notes.globals import NOTES_DIR, NOTES_TAG_DIR

from pathlib import Path
from f.notes.note_link_extractor import LinkExtractor
from promnesia.cannon import canonify
import re

# This note class provides these features:
# reading/writing/modifying notes frontmatter
# creating a symlinked directory structure with sub directories as the tags of notes 

# ---
# tags: ''
# tags_fs: ''
# ---



class BaseNote():
    """provides reading, writing, and ensuring the frontmatter existing on a note file"""
    def __init__(self, abs):
        self.abs = abs

        self.link_extractor = LinkExtractor(Path(self.abs))

        # before we do anything, ensure the absolute path I have instantiated this class with is actually a note (damage mitigation)
        if NOTES_DIR not in self.abs:
            print("file {} - does not exist within notes folder - not processing".format(abs))
            exit()
        
        self._get_or_create_frontmatter()

 

    def _get_or_create_frontmatter(self):
        """always returns a frontmatter object from the file"""
        """ensures all files (notes have an empty frontmatter object"""
        """if parsed frontmatter is not empty, returns the post object from the file"""
        """if parsed frontmatter object does not exist (no metadata), writes a generated boilerplate to the file, and returns the post object with the existing file content/body"""
        print("loading frontmatter: {}".format(self.abs))
        try:
            existing_post = frontmatter.load(self.abs)
        except Exception as e:
            # Handle the exception.
            print("EXITING: Could not parse frontmatter for: {}".format(self.abs))
            print(" - This can be because of --- being added manually to the top of some note files. Fix manually for now...")
            print(e)
        # if frontmatter does not exist, creates it
        # self.post.content -> body/content as a string
        # self.post.metadata -> the actual frontmatter
        if not existing_post.handler:
            self.post = self._generate_frontmatter_boilerplate(existing_post)
            self.write_frontmatter()
        else:
            self.post = existing_post
        
    def _update_post(self, post):
        """updates the post object on the class"""
    
    def _generate_frontmatter_boilerplate(self, existing_post):
        """appends frontmatter data to a post.content text string (ie the contents/body of the existing file)"""
        """frontmatter.loads needs the original text content, this is passthrough and used for the content in the new post object"""
        """returns a post object that can be written to the file with _write_frontmatter"""
        return frontmatter.loads(existing_post.content, YAMLHandler(), tags="", tags_fs="")


    def write_frontmatter(self):
        """write new frontmatter to file, leaving body/content untouched"""
        print("{} - writing frontmatter: {}".format(self.abs, self.post.metadata))
        with open(self.abs, "w") as f:
            f.write(frontmatter.dumps(self.post))
        f.close()

class Note(BaseNote):
    """a note class with a collection of my helper methods"""
    """a note that can modify its tags based on its location on the filesystem"""
    """using this to add relative subdir tags to notes"""
    """all these methods act on a single note"""
    def __init__(self, abs):
        super().__init__(abs)

        # work our relative subdir paths
        # if abs, NOTE_DIR/1/coding/python/mynote.md
        # relative subdir paths = ["coding", "python"]
        # note, always removes root level subdir
        self.relative_subdir_paths = os.path.dirname(os.path.relpath(abs, NOTES_DIR)).split(os.sep)
        del self.relative_subdir_paths[0]

        # # pre checks
        # self.write_subdir_tags()


    def write_subdir_tags(self):
        # add relative subdir paths to tags_fs key of file frontmatter
        self.post.metadata["tags_fs"] = self.relative_subdir_paths.copy()
        self.write_frontmatter()

    def _generate_sym_targets(self):
        """generates a list of symlink targets (absolute filepaths) for NOTES_TAG_DIR using subpaths of NOTES_DIR"""
        targets = []
        filename = os.path.basename(self.abs)
        for subpath in self.relative_subdir_paths:
            targets.append(os.path.join(NOTES_TAG_DIR, subpath, filename))
        self.targets = targets
        return targets
    
    def _symlink_targets(self):
        for target in self.targets:
            self._symlink(target)

    def _symlink(self, target):
        """a symlink function that removes the target if it exists but does not link back to the source"""
        # Check if the target already exists.
        if os.path.exists(target):
            # Check if the target is a symlink to the source.
            if not os.path.islink(target) and os.readlink(target) == self.abs:
                os.remove(target)
        else:
            # Create the parent directories of the target.
            target_dir = os.path.dirname(target)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            # Create the symlink.
            try:
                print("Symlinking {} --> {}".format(self.abs, target))
                os.symlink(self.abs, target)
                return True
            except FileExistsError:
                return False
            
        # Link Extractor methods here
    def _validate_url(self, url):
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
            
    def _get_links(self):
        urls = []
        for visit in self.link_extractor.extract(self.abs):
            # as canonify outputs a normalized URL without the scheme prefixed
            scheme = re.match(r"^([\S]+):\/\/", visit.url)
            if scheme:
                url = scheme.group(1) + "://" + canonify(visit.url)
            else:
                url = canonify(visit.url)

            url = self._validate_url(url)
            if not url:
                break # if the url validator returned false, ignore the link (vlc links etc)
            urls.append(url)
        return urls


