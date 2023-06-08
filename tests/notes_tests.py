#####################################################
# the methods listed here are the only methods that should be called publicly

# from f.notes.notes_library import NoteLibrary
# note_library = NoteLibrary()

# note_library.get_all_links()

# writing all subdir tags
#note_library.write_all_subdir_tags() 

# creating note sym
#note_library.create_note_syms()


#####################################################
# from f.notes.note import Note

# note = Note("/Users/f1/notes/2/design/figma/design-systems.md")
# print(note._get_links())


from f.notes.notes_library import FSTree
fstree = FSTree()
fstree.insert(["apps", "zsh"], )