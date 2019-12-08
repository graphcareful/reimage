#/bin/sh
echo "Downloading dependencies..."
os_version=$(cat /etc/os-release | grep NAME | head -n 1 | tr -d NAME= | cut -d '"' -f 2)
if [ "$os_version" = "Fedora" ]; then
    sudo dnf update
    sudo dnf install -y \
         python-devel \
         python-pip \
         openssl-devel \
         libffi-devel \
         libselinux-python
    sudo pip install ansible
elif [ "$os_version" = "Ubuntu" ]; then
    # TODO: Complete
    sudo apt update
    sudo apt install -y python3-pip ansible
else
    echo "Unsupported OS, do it manually, sorry!"
    exit 1
fi

echo "Downloading source code..."
mkdir $HOME/workspace
git clone https://github.com/graphcareful/reimage.git $HOME/workspace/reimage

echo "Running bootstrap phase..."
ansible-playbook -i hosts -K playbooks/install.yml

