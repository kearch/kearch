#! /bin/bash
# If you don't use minikube, please comment in 'not minikube'.

MINIKUBE=''
# MINIKUBE='not minikube'

me_eval_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=evaluator -o go-template --template '{{(index .items 0).metadata.name}}')
echo $me_eval_pod_name
kubectl --namespace=kearch exec ${me_eval_pod_name} -- pytest -m "${MINIKUBE}" flask_main.py

me_gateway_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=gateway -o go-template --template '{{(index .items 0).metadata.name}}')
echo $me_gateway_pod_name
kubectl --namespace=kearch exec ${me_gateway_pod_name} -- pytest -m "${MINIKUBE}" meta_gateway.py

me_query_processor_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=query-processor -o go-template --template '{{(index .items 0).metadata.name}}')
echo $me_query_processor_pod_name
kubectl --namespace=kearch exec ${me_query_processor_pod_name} -- pytest -m "${MINIKUBE}" meta_query_processor.py

me_summary_updater_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=summary-updater -o go-template --template '{{(index .items 0).metadata.name}}')
echo $me_summary_updater_pod_name
kubectl --namespace=kearch exec ${me_summary_updater_pod_name} -- pytest -m "${MINIKUBE}" main.py

