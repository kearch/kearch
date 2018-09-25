#! /bin/sh
# Please run this script just under kearch/


KEARCH_ROOT_DIR=$(cd $(dirname $0); pwd)
echo "KEARCH_ROOT_DIR = "${KEARCH_ROOT_DIR}

echo "----- Start to make namespace and configure context. -----"
cd $KEARCH_ROOT_DIR/services
kubectl create -f kearch-namespace.yaml
kubectl config set-context kearch-minikube \
  --namespace=kearch \
  --cluster=minikube \
  --user=minikube
kubectl config use-context kearch-minikube
kubectl config current-context
echo "----- Finish making namespace and configuring context. -----"

# sp-db
echo "----- Start to deploy specialist DB. -----"
cd $KEARCH_ROOT_DIR/services/sp-db

kubectl apply -f sp-db-pv.yaml
kubectl apply -f mysql-pvc.yaml
kubectl apply -f sp-db-configmap.yaml
kubectl apply -f sp-db-deployment.yaml
kubectl apply -f sp-db-service.yaml

cd $KEARCH_ROOT_DIR/services/sp-db

sp_db_pod_name=$(kubectl get po -l engine=sp,app=db -o go-template --template '{{(index .items 0).metadata.name}}')
echo "----- sp_db_pod_name = "${sp_db_pod_name}" -----"
# Comment out following 5 lines when you don't need to change DB.
# kubectl --namespace=kearch exec $sp_db_pod_name -- bash -c 'echo "CREATE DATABASE kearch_sp_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" | mysql -uroot -ppassword'
# kubectl --namespace=kearch cp $(pwd)/sql/webpages_schema.sql $sp_db_pod_name:/tmp/webpages_schema.sql
# kubectl --namespace=kearch cp $(pwd)/sql/url_queue_schema.sql $sp_db_pod_name:/tmp/url_queue_schema.sql
# kubectl --namespace=kearch exec $sp_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_sp_dev < /tmp/webpages_schema.sql'
# kubectl --namespace=kearch exec $sp_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_sp_dev < /tmp/url_queue_schema.sql'

echo "----- Show database status. -----"
kubectl exec $sp_db_pod_name -- bash -c 'echo "show databases;" | mysql -uroot -ppassword' 2>/dev/null
echo "----- Show table status. -----"
echo "----- Tables in kearch_sp_dev -----"
kubectl exec $sp_db_pod_name -- bash -c 'echo "use kearch_sp_dev; show tables;" | mysql -uroot -ppassword' 2>/dev/null
tables=$(kubectl exec $sp_db_pod_name -- bash -c 'echo "use kearch_sp_dev; show tables;" | mysql -uroot -ppassword' 2>/dev/null)
echo "----- Detailed information of tables -----"
for t in ${tables};
do
    kubectl exec $sp_db_pod_name -- bash -c "mysql -uroot -ppassword kearch_sp_dev -e'show create table $t' " 2>/dev/null
done
echo "----- Finish deployment of specialist DB. -----"

# sp-crawler-parent
echo "----- Start deployment of specialist crawler parent. -----"
cd $KEARCH_ROOT_DIR/packages/specialist_crawler_parent
kubectl --namespace=kearch apply -f sp-crawler-parent-service.yaml
eval $(minikube docker-env)
docker build -t kearch/sp-crawler-parent .

cd $KEARCH_ROOT_DIR/services/sp-crawler-parent

kubectl apply -f sp-crawler-parent-deployment.yaml
kubectl apply -f sp-crawler-parent-service.yaml
echo "----- Finish deployment of specialist crawler parent. -----"

# sp-crawler-child
echo "----- Start deployment of specialist crawler child. -----"
cd $KEARCH_ROOT_DIR/packages/specialist_crawler_child
rm -f $KEARCH_ROOT_DIR/packages/specialist_crawler_child/webpage_cache/*.pickle

eval $(minikube docker-env)
echo "----- Use cache file and skip model learning. -----"
echo "----- If you don't want to use cache file,  use -----"
echo "----- 'docker build -t kearch/sp-crawler-child .' instead -----"
docker build -t kearch/sp-crawler-child -f Dockerfile_cache .

cd $KEARCH_ROOT_DIR/services/sp-crawler-child

kubectl apply -f sp-crawler-child-deployment.yaml
kubectl apply -f sp-crawler-child-service.yaml
echo "----- Finish deployment of specialist crawler child. -----"


# sp-admin
echo "----- Start deployment of specialist admin. -----"
cd $KEARCH_ROOT_DIR/packages/specialist_admin

eval $(minikube docker-env)
docker build -t kearch/sp-admin .

cd $KEARCH_ROOT_DIR/services/sp-admin

kubectl apply -f sp-admin-deployment.yaml
kubectl apply -f sp-admin-service.yaml
echo "----- Finish deployment of specialist admin. -----"
