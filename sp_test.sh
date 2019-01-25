#! /bin/bash

MINIKUBE='not minikube'

sp_classifier_pod_name=$(kubectl --namespace=kearch get po -l engine=sp,app=classifier -o go-template --template '{{(index .items 0).metadata.name}}')
echo $sp_classifier_pod_name
kubectl --namespace=kearch exec ${sp_classifier_pod_name} -- pytest -m "${MINIKUBE}" flask_main.py

sp_gateway_pod_name=$(kubectl --namespace=kearch get po -l engine=sp,app=gateway -o go-template --template '{{(index .items 0).metadata.name}}')
echo $sp_gateway_pod_name
kubectl --namespace=kearch exec ${sp_gateway_pod_name} -- pytest -m "${MINIKUBE}" sp_gateway.py

sp_query_processor_pod_name=$(kubectl --namespace=kearch get po -l engine=sp,app=query-processor -o go-template --template '{{(index .items 0).metadata.name}}')
echo $sp_query_processor_pod_name
kubectl --namespace=kearch exec ${sp_query_processor_pod_name} -- pytest -m "${MINIKUBE}" sp_query_processor.py

