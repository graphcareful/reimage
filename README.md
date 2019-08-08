# Reborn

### A simple way to install my personal configuration onto a RedHat or Debian machine

---

### How to perform systemwide installation
```
$ ./bootstrap.sh
$ ansible-playbook -i hosts -K playbooks/install.yml
```

### What gets installed...

- tmux
- zsh
- oh-my-zsh
- emacs/spacemacs
- kraken x61 driver (if kraken x61 is detected)
- My personal tmux / emacs and ssh config files
