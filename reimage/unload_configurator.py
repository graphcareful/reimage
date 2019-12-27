#!/usr/bin/python3
import os
import subprocess
import shutil
import distutils.dir_util
import tarfile
import multiprocessing
from reimage.shell import run_oneline, run_oneline_sudo
from functools import reduce
from reimage.utils import get_os_version, true_user_path, download_file, download_resource
from reimage.DnfPackageInstaller import DnfPackageInstaller

def unpack(resource):
    if not os.path.exists(resource):
        raise Exception("Resource DNE error: %s" % resource)
    resource_name = os.path.basename(resource)
    resource_type = resource_name.split(".")
    if len(resource_type) == 2:
        if resource_type[1] == 'zip':
            pass
        else:
            raise Exception("Unsupported resource_type encountered: %s" % resource_type)
    else:
        resource_type = ".".join(resource_type[-2:])
        if resource_type == 'tar.gz':
            print("Resource: " + resource)
            tf = tarfile.open(resource, "r:gz")
            current_dir = os.getcwd()
            os.chdir(os.path.dirname(resource))
            tf.extractall()
            os.chdir(current_dir)
        elif resource_type == 'tar.xz':
            pass
        else:
            raise Exception("Unsupported resource_type encountered: %s" % resource_type)


def configure_scripts(item_meta):
    def evaluate_predicate(predicate):
        if 'predicate' not in predicate or 'item' not in predicate:
            raise Exception("Misconfigured predicate: %s" % item_meta)
        method = predicate["predicate"]
        if method == "exists":
            return os.path.exists(true_user_path(predicate['item']))
        elif method == "not_exists":
            return not os.path.exists(true_user_path(predicate['item']))
        elif method == "is_empty":
            return len(os.listdir(true_user_path(predicate['item']))) == 0
        elif method == "not_empty":
            return len(os.listdir(true_user_path(predicate['item']))) > 0

        raise Exception("Unimplemented predicate: %s" % method)

    url = item_meta["url"]
    can_run = evaluate_predicate(item_meta["run_when"])
    if can_run is True:
        if url.startswith("http"):
            run_oneline(download_file(url))
        else:
            script = true_user_path(url)
            run_oneline(script)


def configure_source_builder(dnfinstaller, item_meta, workspace):
    if 'package_dependencies' in item_meta:
        dnfinstaller.install_packages(item_meta["package_dependencies"])
    resource = os.path.join(workspace, os.path.basename(item_meta['package_location']))
    resource_dir = os.path.join(workspace, item_meta['package_name'])
    download_resource(item_meta["package_location"], resource, resource_dir)
    unpack(resource)
    cd = os.getcwd()
    os.chdir(resource_dir)
    nprocs = multiprocessing.cpu_count()
    asRoot = None
    if "package_install_as_root" in item_meta:
        root = item_meta["package_install_as_root"]
        asRoot = "sudo" if root is True else ""
    run_oneline("./configure && make -j%s" % nprocs)
    if asRoot:
        run_oneline_sudo("%s make install" % asRoot)
    else:
        run_oneline("make install")
    os.chdir(cd)

def configure_git_repo_syncer(item_meta, workspace):
    try:
        repo = None
        location = workspace
        if type(item_meta) == type(""):
            repo = item_meta
            name = (os.path.basename(repo)).split(".")
            if len(name) == 1:
                name = name[0]
            elif len(name) == 2:
                if name[1] != "git":
                    raise Exception("Not a git repository")
                name = name[0]
            location = os.path.join(workspace, name)
        elif type(item_meta) == type({}):
            repo = item_meta["repo"]
            location = true_user_path(item_meta["at"])
        print("git clone %s %s" % (repo, location))
        run_oneline("git clone %s %s" % (repo, location))
    except subprocess.CalledProcessError as e:
        # If git clone fails, most likely case is that the repo already exists
        pass


def unpack_reimage_tar(data_tar):
    cd = os.getcwd()
    work_dir = '/tmp/reimage_work_dir'
    if os.path.exists(work_dir):
        shutil.rmtree('/tmp/reimage_work_dir')
    os.chdir('/')
    with tarfile.open(os.path.join(cd, data_tar)) as tf:
        tf.extractall()
    # TODO: this must be handled better
    # distutils.dir_util.copy_tree(os.path.join(work_dir, 'system'), '/')
    distutils.dir_util.copy_tree(os.path.join(work_dir, 'user'), os.environ['HOME'], preserve_symlinks=True)
    shutil.rmtree(work_dir)
    os.chdir(cd)

def perform_system_restore(config, data_tar):
    workspace = true_user_path(config["meta_workspace_dir"])
    if not os.path.exists(workspace):
        os.mkdir(workspace)

    # 1. Ensure all base system deps and repos exist and are configured on the host
    fedora_os_version = get_os_version()
    packageInstaller = DnfPackageInstaller(
        fedora_os_version, config["meta_enable_fedora_workstation_repos"],
        config["meta_enable_rpm_fusion"])

    packageInstaller.install_packages(config["meta_package_dependencies"])
    if 'meta_python_pip_package_dependencies' in config:
        str_list = reduce(lambda acc, x: acc + " " + x, config['meta_python_pip_package_dependencies'], "")
        print("Installing pip packages: " + str_list)
        run_oneline_sudo("pip install %s" % str_list)

    # 2. Run any init scripts
    if 'configuration_init_scripts' in config:
        for item in config["configuration_init_scripts"]:
            configure_scripts(item)

    # 3. Untar and unpack configurations
    unpack_reimage_tar(data_tar)

    # 2. Run any post install scripts
    if 'configuration_post_scripts' in config:
        for item in config["configuration_post_scripts"]:
            configure_scripts(item)

    # 4. Download and build any projects from source
    if 'configuration_build_from_source' in config:
        for item in config["configuration_build_from_source"]:
            configure_source_builder(packageInstaller, item, workspace)

    # 5. Download git repos we like
    if 'configuration_git_repos' in config:
        for item in config["configuration_git_repos"]:
            configure_git_repo_syncer(item, workspace)

    # TODO: This portion
    # 6. Optionally install fonts
    # 7. Optionally start services
