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

```sh
cd path/to/kearch
cd services/sp-db

kubectl apply -f sp-db-pv.yaml
kubectl apply -f mysql-pvc.yaml
kubectl apply -f sp-db-deployment.yaml
kubectl apply -f sp-db-service.yaml
```

`sp-db` service can be resolved as `sp-db.kearch.svc.cluster.local` .
