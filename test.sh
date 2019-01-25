#! /bin/bash

me_eval_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=evaluater -o go-template --template '{{(index .items 0).metadata.name}}')
echo $me_eval_pod_name
kubectl --namespace=kearch exec ${me_eval_pod_name} pytest flask_main.py

me_gateway_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=gateway -o go-template --template '{{(index .items 0).metadata.name}}')
echo $me_gateway_pod_name
kubectl --namespace=kearch exec ${me_gateway_pod_name} pytest meta_gateway.py
