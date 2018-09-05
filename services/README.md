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
```


```sh
# sudo iptables -I INPUT -p tcp --dport 8080 -j ACCEPT

sudo su -l kearch

mkdir -p ~/dev/src/github.com/kearch
cd ~/dev/src/github.com/kearch
git clone https://github.com/kearch/kearch.git
cd kearch
git checkout dev

# you need to run `docker build` here

kubectl config set-context kearch-dev --namespace=kearch --cluster=kubernetes --user=kubernetes-admin
kubectl config use-context kearch-dev

sudo mkdir /data

kubectl apply -f services/kearch-namespace.yaml
for yaml in `ls services/sp-*/*.yaml`; do
    kubectl apply -f $yaml
done

cd services/sp-db
sp_db_pod_name=$(kubectl get po -l engine=sp,app=db -o go-template --template '{{(index .items 0).metadata.name}}')
kubectl exec $sp_db_pod_name -- bash -c 'echo "CREATE DATABASE kearch_sp_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" | mysql -uroot -ppassword'
kubectl cp $(pwd)/sql/webpages_schema.sql $sp_db_pod_name:/tmp/webpages_schema.sql
kubectl cp $(pwd)/sql/url_queue_schema.sql $sp_db_pod_name:/tmp/url_queue_schema.sql
kubectl exec $sp_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_sp_dev < /tmp/webpages_schema.sql'
kubectl exec $sp_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_sp_dev < /tmp/url_queue_schema.sql'

mkdir -p ~/tmp && cd ~/tmp
cat <<"EOF" > insert_initial_urls.sql
INSERT INTO `url_queue` (`url`)
VALUES
("https://www.deviantart.com/shedopen"),
("https://en.wikipedia.org/wiki/Haskell_(programming_language)");
EOF
kubectl cp insert_initial_urls.sql $sp_db_pod_name:/tmp/insert_initial_urls.sql
kubectl exec $sp_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_sp_dev < /tmp/insert_initial_urls.sql'
kubectl exec $sp_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_sp_dev < /tmp/insert_initial_urls.sql'

# check number of webpages crawled
kubectl exec $sp_db_pod_name -- mysql -uroot -ppassword kearch_sp_dev -e 'SELECT COUNT(*) FROM `webpages`;'
```

```sql
INSERT INTO `url_queue` (`url`)
VALUES
("https://www.deviantart.com/shedopen"),
("https://en.wikipedia.org/wiki/Haskell_(programming_language)");
```

```sql
INSERT INTO `url_queue` (`url`)
VALUES
("https://en.wikipedia.org/wiki/World_history");
```

```sql
INSERT INTO `url_queue` (`url`)
VALUES
("https://en.wikipedia.org/wiki/Kyoto");
```
