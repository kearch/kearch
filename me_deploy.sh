#! /bin/sh
# Please run this script just under kearch/


KEARCH_ROOT_DIR=$(cd $(dirname $0); pwd)
echo "KEARCH_ROOT_DIR = "${KEARCH_ROOT_DIR}

echo "----- Start to make namespace and configure context. -----"
cd $KEARCH_ROOT_DIR/services
kubectl create -f kearch-namespace.yaml
echo "----- Finish making namespace and configuring context. -----"

echo "----- Start deployment of meta front. -----"
cd $KEARCH_ROOT_DIR/packages/meta_front
eval $(minikube docker-env)
docker build -t kearch/me-front .

cd $KEARCH_ROOT_DIR/services/me-front

kubectl --namespace=kearch apply -f me-front-deployment.yaml
kubectl --namespace=kearch apply -f me-front-service.yaml
echo "----- Finish deployment of meta front. -----"

echo "----- Start deployment of meta gateway. -----"
cd $KEARCH_ROOT_DIR/packages/meta_gateway
eval $(minikube docker-env)
docker build -t kearch/me-gateway .

cd $KEARCH_ROOT_DIR/services/me-gateway

kubectl --namespace=kearch apply -f me-gateway-deployment.yaml
kubectl --namespace=kearch apply -f me-gateway-service.yaml
echo "----- Finish deployment of meta gateway. -----"

echo "----- Start deployment of meta query processor. -----"
cd $KEARCH_ROOT_DIR/packages/meta_query_processor
eval $(minikube docker-env)
docker build -t kearch/me-query-processor .

cd $KEARCH_ROOT_DIR/services/me-query-processor

kubectl --namespace=kearch apply -f me-query-processor-deployment.yaml
kubectl --namespace=kearch apply -f me-query-processor-service.yaml
echo "----- Finish deployment of meta gateway. -----"


echo "----- Start deployment of meta db. -----"
cd $KEARCH_ROOT_DIR/services/me-db

kubectl --namespace=kearch apply -f me-db-pv.yaml
kubectl --namespace=kearch apply -f me-mysql-pvc.yaml
kubectl --namespace=kearch apply -f me-db-configmap.yaml
kubectl --namespace=kearch apply -f me-db-deployment.yaml
kubectl --namespace=kearch apply -f me-db-service.yaml

me_db_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=db -o go-template --template '{{(index .items 0).metadata.name}}')
echo "----- me_db_pod_name = "${me_db_pod_name} "-----"
kubectl --namespace=kearch exec $me_db_pod_name -- bash -c 'echo "CREATE DATABASE kearch_me_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" | mysql -uroot -ppassword'
kubectl --namespace=kearch cp $(pwd)/sql/sp_servers_schema.sql $me_db_pod_name:/tmp/sp_servers_schema.sql
kubectl --namespace=kearch exec $me_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_me_dev < /tmp/sp_servers_schema.sql'

echo "----- Finish deployment of meta db. -----"

echo "----- Delete all pods -----"
kubectl --namespace=kearch delete pod --all
