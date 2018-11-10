#!/bin/sh

sp_admin_pod_name=$(kubectl --namespace=kearch get po -l engine=sp,app=admin -o go-template --template '{{(index .items 0).metadata.name}}')
kubectl exec -it --namespace=kearch ${sp_admin_pod_name} curl sp-es.kearch.svc.cluster.local:9200/sp/_count
