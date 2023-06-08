from setuptools import setup, find_packages

# 

# Meta information
name = "f"
version = "0.1.0"
#author = "Frederick Hill"
author_email = "freddiehill000@gmail.com"
description = "Personal collection of python libraries."
url = "https://github.com/fhill2/python_lib"
license = "MIT"


# scans all the packages in the cwd
packages = find_packages()
install_requires = []


# Build
setup(
    name=name,
    version=version,
   # author=author,
    author_email=author_email,
    #description=description,
    # long_description=long_description,
    url=url,
    license=license,
    packages=packages,
    install_requires=install_requires,
    # package_data=package_data,
)