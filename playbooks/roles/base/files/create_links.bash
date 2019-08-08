#!/bin/bash
set -ex
sudo chmod 600 $(ls rblaffor*)
sudo chmod 644 $(ls rblaffor*.pub)
rm -rf ~/.ssh/active/*
cd ~/.ssh/active
for i in $(ls ~/.ssh/keys/rblaffor*); do
    # ln -s $HOME/.ssh/keys/rblaffor-deployed-2018-01-02.pub current-deployed.pub
    key_type=$(echo $i | awk '{split($1,arr,"-"); print arr[2]}')
    public=$(echo $i | awk '{split($1,arr,"."); print arr[3]}')
    if [[ $public != "" ]]; then
        public=.$public
    fi
    key_name=current-$key_type$public
    ln -s $i $key_name
done
