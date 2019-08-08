#!/bin/bash
set -ex
root=$(git rev-parse --show-toplevel)
roles=$root/playbooks/roles

# 1. spacemacs stuff
cp ~/.spacemacs $roles/emacs/files/spacemacs
# 2. ssh stuff
cp ~/.ssh/keys/create_keys.bash $roles/base/files
cp ~/.ssh/keys/create_links.bash $roles/base/files
cp ~/.ssh/config $roles/base/files/ssh_config
# 3. tmux stuff
cp ~/.tmux.conf $roles/shell/files/tmux.conf
cp ~/.tmux.agnoster-theme $roles/shell/files/tmux.agnoster-theme
# 4. zsh stuff
cp ~/.zshrc $roles/shell/files/zshrc
cp ~/.zshrc.pre-oh-my-zsh $roles/shell/files/zshrc.pre-oh-my-zsh
