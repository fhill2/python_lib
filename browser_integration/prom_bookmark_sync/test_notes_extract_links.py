from notes_links import remove_yt_links, list_to_dict, extract_yt_id_time


links = [
        {"url": "youtube.com/watch?v=UBGhSB16X9MXhzSFe_H7XAAA"},
        {"url": "youtube.com/watch?v=UCfhSB16X9MXhzSFe_H7XbHg?t=2"},
        {"url": "youtube.com/watch?v=UCfhSB16X9MXhzSFe_H7XbHg?t=240"},
        {"url": "youtube.com/watch?v=UCfhSB16X9MXhzSFe_H7XbHg?t=360"},
        ]

def get_yt_links_from_file():
    links = {}
    with open("test_notes_extract_links_data.txt") as f:
        text = f.read()
        links_list = text.split("\n")
        f.close()
    for url in links_list:
        if url != '':
            links[url] = {"url": url}
    return links
    # return [x for x in links if x != ''] # remove empty strings

links = remove_yt_links(get_yt_links_from_file())
for link in links.values():
    print(link["url"])
    
    # id, time = extract_yt_id_time(url)

# print(remove_yt_links(list_to_dict(links)))


#https://youtu.be/HmbeM4fHxQk?t=2
