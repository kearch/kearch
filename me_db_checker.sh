#! /bin/sh

me_db_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=db -o go-template --template '{{(index .items 0).metadata.name}}')
echo "----- Show database status. -----"
kubectl --namespace=kearch exec $me_db_pod_name -- bash -c 'echo "show databases;" | mysql -uroot -ppassword' 2>/dev/null
echo "----- Show table status. -----"
echo "----- Tables in kearch_me_dev -----"
kubectl --namespace=kearch exec $me_db_pod_name -- bash -c 'echo "use kearch_me_dev; show tables;" | mysql -uroot -ppassword' 2>/dev/null
tables=$(kubectl --namespace=kearch exec $me_db_pod_name -- bash -c 'echo "use kearch_me_dev; show tables;" | mysql -uroot -ppassword' 2>/dev/null)
echo "----- Detailed information of tables -----"
for t in ${tables};
do
    kubectl exec --namespace=kearch $me_db_pod_name -- bash -c "mysql -uroot -ppassword kearch_me_dev -e'show create table $t' " 2>/dev/null
done
echo "---- hosts in sp_servers -----"
kubectl exec --namespace=kearch $me_db_pod_name -- bash -c 'echo "use kearch_me_dev; select distinct host from sp_servers;" | mysql -uroot -ppassword' 2>/dev/null
