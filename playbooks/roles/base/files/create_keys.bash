#!/bin/bash

set -ex
internal=`whoami`-internal-`date +%Y-%m-%d`
echo "Generating internal key... $internal"
ssh-keygen -t rsa -b 2048 -C "$internal" -f ~/.ssh/keys/$internal
internalfprint=$(ssh-keygen -l -E md5 -f ~/.ssh/keys/$internal)
echo "Fingerprint: ${internalfprint}"
external=`whoami`-external-`date +%Y-%m-%d`
echo "Generating external key... ${external}"
ssh-keygen -t rsa -b 2048 -C "$external" -f ~/.ssh/keys/$external
externalfprint=$(ssh-keygen -l -E md5 -f ~/.ssh/keys/$external)
echo "Fingerprint: ${externalfprint}"
deployed=`whoami`-deployed-`date +%Y-%m-%d`
echo "Generating deployed key... ${deployed}"
ssh-keygen -t rsa -b 2048 -C "$deployed" -f ~/.ssh/keys/$deployed
deployedfprint=$(ssh-keygen -l -E md5 -f ~/.ssh/keys/$deployed)
echo "Fingerprint: ${deployedfprint}"
