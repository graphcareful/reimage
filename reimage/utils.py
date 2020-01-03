#!/usr/bin/python3
import os
import platform
import distro
import urllib.request
import shutil

def get_os_version():
    name, version, _ = distro.linux_distribution()
    if platform.system() != "Linux" or name != "Fedora":
        raise Exception("Unsupport platform exception")
    return version


# Converts $HOME/workspace/item/b/c => /home/robert/workspace/item/b/c
def true_user_path(path):
    if path.startswith("$HOME"):
        return os.path.join(os.environ["HOME"], path.split("$HOME/")[1])
    return path

# downloads item into a directory or returns data as string
def download_file(url, directory=None):
    print("Downloading file: %s and unpacking: %s" % (url, directory))
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    if directory is None:
        return data
    with open(os.path.join(directory, os.path.basename(url)), 'w') as f:
        f.write(data)

def download_resource(url, file_name, out_file):
    print("Downloading resource: %s and unpacking: %s" % (url, out_file))
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

