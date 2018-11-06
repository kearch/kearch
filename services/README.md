# kearch kubernets services

## kubernetes single-node cluster setup

```sh
#! /bin/bash
set -e
set -x

sudo useradd kearch
sudo usermod -aG sudo kearch
sudo passwd kearch

mkdir -p ~/tmp
cd ~/tmp

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y curl gnupg dstat htop tmux vim wget zsh

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

cat <<EOF > kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo mv kubernetes.list /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y apt-transport-https
sudo apt-get install -y docker.io
sudo apt-get install -y kubelet kubeadm

sudo usermod -aG docker kearch

sudo systemctl enable docker.service

sudo vim /etc/default/kubelet
# edit as follows: KUBELET_EXTRA_ARGS=--fail-swap-on=false

sudo systemctl daemon-reload
sudo systemctl restart kubelet

sudo kubeadm init --ignore-preflight-errors Swap --pod-network-cidr=192.168.0.0/16

sudo mkdir /home/kearch
sudo chown -R kearch:kearch /home/kearch

sudo su -l kearch
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

sudo chmod 644 /etc/kubernetes/admin.conf

kubectl taint nodes --all node-role.kubernetes.io/master- \
  --kubeconfig /etc/kubernetes/admin.conf

kubectl apply \
  -f http://docs.projectcalico.org/v2.4/getting-started/kubernetes/installation/hosted/kubeadm/1.6/calico.yaml \
  --kubeconfig /etc/kubernetes/admin.conf

# On a node where you want PersistentVolumes to be hosted
kubectl label nodes <your-node-name> storage=sp-es
sudo mkdir /data
sudo mkdir /data/sp-es-data-00
sudo mkdir /data/sp-es-master-00
sudo mkdir /data/sp-es-master-01
```
