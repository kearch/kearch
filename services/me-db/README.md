# me-db service

## Prerequisites

You need to run the following commands first.

```sh
cd path/to/kearch
cd services
kubectl create -f kearch-namespace.yaml
kubectl config set-context kearch-minikube \
  --namespace=kearch \
  --cluster=minikube \
  --user=minikube
kubectl config use-context kearch-minikube
kubectl config current-context # => should display `kearch-minikube`
```

## Usage

Create kubernetes resources from yaml files.

```sh
cd path/to/kearch
cd services/me-db

kubectl apply -f me-db-pv.yaml
kubectl apply -f me-mysql-pvc.yaml
kubectl apply -f me-db-deployment.yaml
kubectl apply -f me-db-service.yaml
```

Create tables.

```sh
cd path/to/kearch
cd services/me-db

me_db_pod_name=$(kubectl get po -l engine=me,app=db -o go-template --template '{{(index .items 0).metadata.name}}')
kubectl exec $me_db_pod_name -- bash -c 'echo "CREATE DATABASE kearch_me_dev;" | mysql -uroot -ppassword'
kubectl cp $(pwd)/sql/sp_servers.sql $me_db_pod_name:/tmp/sp_servers.sql
kubectl exec $me_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_me_dev < /tmp/sp_servers.sql'
```

`me-db` service can be resolved as `me-db.kearch.svc.cluster.local` .
