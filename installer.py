# installer.py
#
# Creates a packaging tarball to bundle up important resources for installation
# onto a target machine
#
# Sample files & templates
# ['/home/robert/workspace/reimage/playbooks/roles/emacs/files/spacemacs',
#  '/home/robert/workspace/reimage/playbooks/roles/base/files/ssh_config',
#  '/home/robert/workspace/reimage/playbooks/roles/base/files/create_links.bash',
#  '/home/robert/workspace/reimage/playbooks/roles/base/files/create_keys.bash',
#  '/home/robert/workspace/reimage/playbooks/roles/shell/templates/zshrc',
#  '/home/robert/workspace/reimage/playbooks/roles/shell/files/tmux.agnoster-theme',
#  '/home/robert/workspace/reimage/playbooks/roles/shell/files/tmux.conf',
#  '/home/robert/workspace/reimage/playbooks/roles/shell/files/perforce',
#  '/home/robert/workspace/reimage/playbooks/roles/shell/files/id_rsa.pub']

import os
import argparse

# Packing
# 1. Copy all ssh keys
# 2. Refresh all configuration files
#  - emacs/spacemacs
#  - .zshrc
#  - .tmux.conf
#  -
# 3. Bootstrap script

# Unpacking
# 3. Generate links


def flat_map(fn, iterable):
    mapped = [fn(x) for x in iterable]
    return reduce(lambda acc, x: acc + x, mapped, [])


def run_oneline(cmd, quiet=False):
    def _cleanup_whitespace(s):
        return re.sub(r'\s+', '', s)

    ret = raw_check_output(cmd, quiet)
    if ret is None: return ret
    return _cleanup_whitespace(ret)


def get_git_root(relative="."):
    cmd = "cd %s && git rev-parse --show-toplevel" % relative
    return shell.run_oneline(cmd, True)


def listdirfull(abs_path):
    if os.path.isabs(abs_path) and os.path.exists(abs_path):
        return [os.path.join(abs_path, x) for x in os.listdir(abs_path)]
    return None


def find_config_files(root):
    config_dirs = [
        x[0] for x in os.walk(root) if os.path.basename(x[0]) == "files"
        or os.path.basename(x[0]) == "templates"
    ]
    return flat_map(lambda x: listdirfull(x), config_dirs)

def find_config_files_on_host(root, config_files, allowed_search_paths):
    for x, dirname, filename in os.walk(root):
        if filename == 


def generate_options():
    parser = argparse.ArgumentParser(description='Create reimage installer')
    parser.add_argument('--export_dir',
                        help='Media where installer tarball will go')

    return parser


def update_reimage(root):
    config_files = find_config_files(root)


def main():
    parser = generate_options()
    options, program_options = parser.parse_known_args()
    root = get_git_root()
    # if options.export_dir


if __name__ == '__main__':
    main()
