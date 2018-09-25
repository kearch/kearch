#! /bin/sh

sp_db_pod_name=$(kubectl --namespace=kearch get po -l engine=sp,app=db -o go-template --template '{{(index .items 0).metadata.name}}')
echo "----- Show database status. -----"
kubectl --namespace=kearch exec $sp_db_pod_name -- bash -c 'echo "show databases;" | mysql -uroot -ppassword' 2>/dev/null
echo "----- Show table status. -----"
echo "----- Tables in kearch_sp_dev -----"
kubectl --namespace=kearch exec $sp_db_pod_name -- bash -c 'echo "use kearch_sp_dev; show tables;" | mysql -uroot -ppassword' 2>/dev/null
tables=$(kubectl --namespace=kearch exec $sp_db_pod_name -- bash -c 'echo "use kearch_sp_dev; show tables;" | mysql -uroot -ppassword' 2>/dev/null)
echo "----- Detailed information of tables -----"
for t in ${tables};
do
    kubectl --namespace=kearch  exec $sp_db_pod_name -- bash -c "mysql -uroot -ppassword kearch_sp_dev -e'show create table $t' " 2>/dev/null
done
echo "---- URLs in queue -----"
kubectl --namespace=kearch exec $sp_db_pod_name -- bash -c 'echo "use kearch_sp_dev; select count(*) from url_queue;" | mysql -uroot -ppassword' 2>/dev/null
echo "---- webpages in DB -----"
kubectl --namespace=kearch exec $sp_db_pod_name -- bash -c 'echo "use kearch_sp_dev; select count(*) from webpages;" | mysql -uroot -ppassword' 2>/dev/null
