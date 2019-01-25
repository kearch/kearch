#! /bin/bash

me_eval_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=evaluater -o go-template --template '{{(index .items 0).metadata.name}}')
echo $me_eval_pod_name
kubectl --namespace=kearch exec ${me_eval_pod_name} pytest flask_main.py

me_gateway_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=gateway -o go-template --template '{{(index .items 0).metadata.name}}')
echo $me_gateway_pod_name
kubectl --namespace=kearch exec ${me_gateway_pod_name} pytest meta_gateway.py

me_query_processor_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=query-processor -o go-template --template '{{(index .items 0).metadata.name}}')
echo $me_query_processor_pod_name
kubectl --namespace=kearch exec ${me_query_processor_pod_name} pytest meta_query_processor.py

me_summary_updater_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=summary-updater -o go-template --template '{{(index .items 0).metadata.name}}')
echo $me_summary_updater_pod_name
kubectl --namespace=kearch exec ${me_summary_updater_pod_name} pytest main.py


sp_classifier_pod_name=$(kubectl --namespace=kearch get po -l engine=sp,app=classifier -o go-template --template '{{(index .items 0).metadata.name}}')
echo $sp_classifier_pod_name
kubectl --namespace=kearch exec ${sp_classifier_pod_name} pytest flask_main.py


sp_gateway_pod_name=$(kubectl --namespace=kearch get po -l engine=sp,app=gateway -o go-template --template '{{(index .items 0).metadata.name}}')
echo $sp_gateway_pod_name
kubectl --namespace=kearch exec ${sp_gateway_pod_name} pytest sp_gateway.py

sp_query_processor_pod_name=$(kubectl --namespace=kearch get po -l engine=sp,app=query-processor -o go-template --template '{{(index .items 0).metadata.name}}')
echo $sp_query_processor_pod_name
kubectl --namespace=kearch exec ${sp_query_processor_pod_name} pytest sp_query_processor.py

