def batch_convert_norg_to_yaml_frontmatter(fp):
    """if the frontmatter detected is not in neorg format - it wont write"""
    post, text = get_frontmatter(fp)

    if "NORGHandler" in str(post.handler):
        # only continue if the frontmatter detected is NORG
        with open(fp, "w") as f:
            post.handler = YAMLHandler()
            f.write(frontmatter.dumps(post))
            print(fp + " -> converted NORG to YAML frontmatter")
    elif "YAMLHandler" in str(post.handler):
        print(fp + " -> already contains YAML frontmatter")
    else:
        print(fp + " -> did not write as frontmatter is " + str(post.handler))