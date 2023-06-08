from sync_syms import get_packer

plugins = get_packer()
plugins_lower = [plug["full_name"].lower() for plug in plugins.values()]
print(plugins_lower)
