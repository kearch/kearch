# sp-db service

## Requirements

Before deploying this service, you need to mount an NFS volume to minikube.

```sh
# confifure exports on mac
sudo mkdir -p /kearchvol/sp-db-nfs
sudo chmod 777 /kearchvol
echo '/kearchvol -network 192.168.99.0 -mask 255.255.255.0 -alldirs -maproot=root:wheel' | sudo tee -a /etc/exports

# start NFS server on mac
sudo nfsd restart
sudo showmount -e # => /kearchvol 192.168.99.0

# mount NFS volume to minikube
# minikube ssh -- sudo mkdir /kearchvol
# minikube ssh -- sudo mount -t nfs 192.168.99.1:/kearchvol /kearchvol
```
