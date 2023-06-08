
# def write_tags():
#     """adds tags_fs tags to the note"""
#     """always overwrites the previous tag_fs (reproducible)"""
#     post, text = get_frontmatter(fp)
#     if "tags_fs" not in post:
#         post["tags_fs"] = []

#     post["tags_fs"] = post["tags_fs"] if isinstance(post["tags_fs"], list) else [ post["tags_fs"] ]
#     unmodified_post_tags = post["tags_fs"].copy()

#     for subdir in subdirs:
#         if subdir not in post["tags_fs"]:
#             post["tags_fs"].append(subdir)

#     if post["tags_fs"] != unmodified_post_tags:
#         with open(fp, "w") as f:
#             print(fp + " -> found tags to add .. writing " + str(post["tags_fs"]))
#             f.write(frontmatter.dumps(post))   


    # def tags_exist(self, fp):
    #     """returns true if note contains tags (are not empty)"""
    #     # TODO: add tags_fs
    #     post, text = get_frontmatter(fp)
    #     if "tags" in post:
    #         if post["tags"] == "" or len(post["tags"]) == 0:
    #             return False
    #         else:
    #             return True
    #     else:
    #         return False

    # def get_tags_from_frontmatter(self, post):
    #     """retrieves all tags from the frontmatter post object"""
    #     """as tags are in tags and tags_fs keys in frontmatter"""
    #     tags = []

    #     def append(key):
    #         if isinstance(post[key], list):
    #             for tag in post[key]:
    #                 tags.append(tag)
    #         elif post[key] != "": 
    #             tags.append(post[key])
            
    #     if "tags" in post.keys():
    #         append("tags")
    #     if "tags_fs" in post.keys():
    #         append("tags_fs")

    #     # return tags list unduplicated
    #     return list(dict.fromkeys(tags))
    


    # def write_file(self, body):
    #     """oneshot to overwrite the content portion of a file - leaving existing frontmatter untouched"""
    #     post = self.get_frontmatter(fp)[0]
    #     post.content = body
    #     with open(fp, "w") as f:
    #         f.write(frontmatter.dumps(post))






    # def _get_frontmatter(self, abs):
    #     with open(abs, "r") as f:
    #         text = f.read()
    #         post = frontmatter.loads(text)
    #         f.close()
    #     return post, text


    # def add_frontmatter_boilerplate_if_not_exist(self, abs):
    #     """if frontmatter exists already - it wont write"""
    #     """if file does not contain any frontmatter, write a frontmatter boilerplate"""
    #     # post, text = get_frontmatter(abs)
    #     # if a handler wasnt matched - then no frontmatter exists
    #     if not post.handler:
    #         with open(abs, "w") as f:
    #             f.write(frontmatter.dumps(post))




# INPUT:
# absolute path to a subfolder under NOTES_DIR (~/notes)
# eg /Users/f1/notes/1


# def batch_ensure_subdir_tags(fp):
#     """for every note, ensures an empty frontmatter YAML exists"""
#     """then adds tags to the frontmatter, with tag name as subdirectory names all the way up to root (NOTES_DIR)"""
#     """e.g root/subdir1/subdir2 -> tags: subdir1, subdir2"""


    #print(subdirs[0], approved_subdirs)
# approved_subdirs = [filename for filename in os.listdir(NOTES_ROOT) if os.path.isdir(os.path.join(NOTES_ROOT,filename))]

    
    # if subdirs[0] not in approved_subdirs:
    #     print("note has to be within subfolder of notes_dir - 1,2,3,sort etc - not processing")
    #     return
    
    # remove the top level subdir folder
   
    
    # exit()
