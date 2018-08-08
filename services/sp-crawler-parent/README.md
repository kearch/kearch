# sp-crawler-parent service

## Prerequisites

Build docker images for kearch on minikube.

```sh
cd path/to/kearch
cd packages/specialist_crawler_parent

eval $(minikube docker-env)
docker build -t kearch/sp-crawler-parent .
```

## Usage

```sh
cd path/to/kearch
cd services/sp-crawler-parent

kubectl apply -f sp-crawler-parent-deployment.yaml
kubectl apply -f sp-crawler-parent-service.yaml
```
