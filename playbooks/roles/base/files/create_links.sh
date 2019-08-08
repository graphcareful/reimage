#!/bin/bash
set -ex

# Define constants
sshdir=~/.ssh
realdir=$sshdir/keys
linkdir=$sshdir/active

# Prepare
cd $realdir
sudo chmod 600 $(ls *)
rm -rf $linkdir
mkdir $linkdir
cd $linkdir

# Iterate over keys and make symlnks
for i in $(ls $realdir); do
    keytype=$(echo $i | awk '{split($1,arr,"-"); print arr[2]}')
    ispub=$(echo $i | awk '{split($1,arr,"."); print arr[2]}')
    if [ "$ispub" != "" ]; then
        ispub=.$ispub
    fi
    ln -s $realdir/$i current-$keytype$ispub
done
