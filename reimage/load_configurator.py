#!/usr/bin/python3
import os
import shutil
import logging
import hashlib
import tarfile
import io
from reimage.shell import run_oneline
from reimage.metascript import metascript
from reimage.utils import true_user_path

logger = logging.getLogger(__name__)

# Removes existing working_directory (if exists) and creates new layout
# Creates /tmp/working_dir/user & # /tmp/working_dir/system
# @returns 3-tuple of paths
def init_load_dir():
    working_dir = "/tmp/reimage_work_dir"
    if os.path.exists(working_dir):
        shutil.rmtree(working_dir)
    os.mkdir(working_dir)
    user_dir = os.path.join(working_dir, "user")
    os.mkdir(user_dir)
    system_dir = os.path.join(working_dir, "system")
    os.mkdir(system_dir)
    return (working_dir, user_dir, system_dir)


# Returns destination of file within /tmp/working_dir/user(or system)
# If switch is enabled directories along the way are created, if DNE
def mapped_config_path(config_dir, destination_dir, create_dirs=True):
    if config_dir.startswith("$HOME"):
        subpath = "/".join(config_dir.split("/")[1:])
    elif config_dir.startswith("/"):
        subpath = config_dir[1:]
    else:
        raise Exception("Invalid path: " + config_dir)
    destination = os.path.join(destination_dir, subpath)
    if not os.path.exists(destination) and create_dirs is True:
        os.makedirs(destination)
    return destination


def perform_system_fetch(user_home, configuration_files, configuration_dirs, config):
    user_configs = [x for x in configuration_files if x.startswith("$HOME")]
    system_configs = [x for x in configuration_files if x.startswith('/')]
    logger.info("Detected user configs: %s" % user_configs)
    logger.info("Detected system configs: %s" % system_configs)
    working_dir, user_dir, system_dir = init_load_dir()
    for config_file in user_configs:
        config_dir = os.path.dirname(config_file)
        shutil.copy(true_user_path(config_file), mapped_config_path(config_dir, user_dir))

    for system_config_file in system_configs:
        system_config_dir = os.path.dirname(system_config_file)
        shutil.copy(system_config_file,
                    mapped_config_path(system_config_dir, system_dir))

    for item in configuration_dirs:
        true_location = true_user_path(item["location"])
        recurse = item["recurse"]
        ignore_list = item["ignore_patterns"] if 'ignore_patterns' in item else []
        if recurse is True:
            mapped = mapped_config_path(item["location"], user_dir, False)
            shutil.copytree(true_location,
                            mapped,
                            symlinks=True,
                            ignore=shutil.ignore_patterns(*ignore_list))
        else:
            raise Exception("Not yet implemented error")

    # Aquire in memory binary representation of the tarred contents
    tar_binary = None
    output_filename = os.path.join(os.getcwd(), "reimage.tar.gz")
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(working_dir)
    with open(output_filename, 'rb') as tarred_binary:
        tar_binary = tarred_binary.read()

    # ... and of THIS program itself (in pex format)
    pexified = os.path.join(os.getcwd(), "reimage.pex")
    if not os.path.exists(pexified):
        run_oneline("pex . -r requirements.txt -v -m reimage.reimage:main -o reimage.pex")
    pexfile = None
    with open(pexified, 'rb') as pexrfile:
        pexfile = pexrfile.read()

    # Finally pass this information onto the metascript to create a run once anywhere
    # installer file, all the client needs is python3
    script_name = 'reimage.run'
    with open(os.path.join(os.getcwd(), script_name), 'w') as meta:
        meta.write(metascript(script_name, pexfile, tar_binary, config))

    # Perform cleanup
    os.remove(output_filename)
    os.remove(pexified)
