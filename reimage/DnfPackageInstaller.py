#!/usr/bin/python3
from reimage.shell import run_oneline, run_oneline_sudo
from functools import reduce


class DnfPackageInstaller(object):
    def __init__(self, os_version, enable_workstation_repos,
                 enable_rpm_fusion):
        int(os_version)
        self.fedora_version = os_version
        if enable_workstation_repos is True:
            print("Installing fedora-workstation-repos.rpm.....")
            run_oneline_sudo("dnf install -y fedora-workstation-repositories")
        if enable_rpm_fusion is True:
            print("Installing/Enabling RPM fusion.....")
            rpmfusion_url = "https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-%s.noarch.rpm" % self.fedora_version
            run_oneline_sudo("dnf install -y %s" % rpmfusion_url)

    def install_packages(self, package_list):
        package_list_str = reduce(lambda acc, x: acc + " " + x, package_list,
                                  "")
        if 'google-chrome-stable' in package_list:
            run_oneline_sudo("dnf config-manager --set-enable google-chrome")
        print("Installing packages: " + package_list_str)
        run_oneline_sudo("dnf install -y %s" % package_list_str)
