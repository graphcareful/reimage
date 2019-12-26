# reimage

### A simple way to install my personal configuration onto a RedHat or Debian machine

Run `bootstrap.sh` to install, the git repo doesn't even need to exist on the host machine.

The `installer.py` script will update the config files in this repo to reflect their current
condition on the host machine, and will create an installer tarball that contains files that
are desired to exist on the host, but cannot be checked into a public repository 
(items like private keys)

### What gets installed...

- tmux
- oh-my-zsh + zsh
- emacs + spacemacs
- Common development packages (build tools, compilers, etc)
- levd kraken x61 driver (if NZXT cooler is detected)
- Personal tmux, emacs, ssh, zsh, and other config files
