#! /bin/sh

set -eu

sp_db_pod_name=$(kubectl --namespace=kearch get po -l engine=sp,app=db -o go-template --template '{{(index .items 0).metadata.name}}')

echo "----- Show database status. -----"
kubectl --namespace=kearch exec $sp_db_pod_name -- mysql -uroot -ppassword -sN -e 'show databases' 2>/dev/null

echo
echo "----- Show table status. -----"
echo "----- Tables in kearch_sp_dev -----"
kubectl --namespace=kearch exec $sp_db_pod_name -- mysql -uroot -ppassword kearch_sp_dev -sN -e 'show tables' 2>/dev/null
tables=$(kubectl --namespace=kearch exec $sp_db_pod_name -- mysql -uroot -ppassword kearch_sp_dev -sN -e 'show tables' 2>/dev/null)

echo
echo "----- Detailed information of tables -----"
for t in ${tables};
do
  kubectl --namespace=kearch exec $sp_db_pod_name -- mysql -uroot -ppassword kearch_sp_dev -sN -e "show create table $t" 2>/dev/null
done

echo
echo "---- Show record count in tables -----"
for t in ${tables};
do
  echo "count $t:"
  kubectl --namespace=kearch exec $sp_db_pod_name -- mysql -uroot -ppassword kearch_sp_dev -sN -e "SELECT COUNT(*) FROM $t" 2>/dev/null
done
