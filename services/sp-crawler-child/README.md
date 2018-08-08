# sp-crawler-child service

## Prerequisites

Build docker images for kearch on minikube.

```sh
cd path/to/kearch
cd services/sp-crawler-child

eval $(minikube docker-env)
docker build -t kearch/sp-crawler-child .
```

## Usage

```sh
cd path/to/kearch
cd services/sp-crawler-child

kubectl apply -f sp-crawler-child-deployment.yaml
kubectl apply -f sp-crawler-child-service.yaml
```
