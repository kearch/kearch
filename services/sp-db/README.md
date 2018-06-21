# sp-db service

## Usage

```sh
cd path/to/kearch
cd services/sp-db

kubectl apply -f sp-db-pv.yaml
kubectl apply -f mysql-pvc.yaml
kubectl apply -f sp-db-deployment.yaml
kubectl apply -f/sp-db-service.yaml
```
