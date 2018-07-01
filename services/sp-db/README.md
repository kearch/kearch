# sp-db service

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
cd services/sp-db

kubectl apply -f sp-db-pv.yaml
kubectl apply -f mysql-pvc.yaml
kubectl apply -f sp-db-deployment.yaml
kubectl apply -f sp-db-service.yaml
```

Create tables.

```sh
cd path/to/kearch
cd services/sp-db

sp_db_pod_name=$(kubectl get po -l engine=sp,app=db -o go-template --template '{{(index .items 0).metadata.name}}')
kubectl exec $sp_db_pod_name -- bash -c 'echo "CREATE DATABASE kearch_sp_dev;" | mysql -uroot -ppassword'
kubectl cp $(pwd)/sql/webpages_schema.sql $sp_db_pod_name:/tmp/webpages_schema.sql
kubectl cp $(pwd)/sql/url_queue_schema.sql $sp_db_pod_name:/tmp/url_queue_schema.sql
kubectl exec $sp_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_sp_dev < /tmp/webpages_schema.sql'
kubectl exec $sp_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_sp_dev < /tmp/url_queue_schema.sql'
```

`sp-db` service can be resolved as `sp-db.kearch.svc.cluster.local` .
