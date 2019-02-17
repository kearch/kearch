#! /bin/sh
# Please run this script just under kearch/

set -eu

if [ $# -lt 1 ]; then
    echo "Please specify services which you want to deploy or re-deploy."
    echo "You can specify like ./me_deploy.sh all or ./me_deploy medb mefront."
    echo "\"all\" : Deploy all deployment except me-db."
    echo "\"medb\" : Deploy me-db. !!THIS OPTION DELETE ALL DATABASE.!!"
    echo "\"mefront\": Deploy me-front."
    echo "\"meqproc\": Deploy me-query-processor."
    echo "\"megate\": Deploy me-gateway."
    echo "\"meadmin\": Deploy me-admin."
    echo "\"mesup\": Deploy me-summary-updater."
    echo "\"meeval\": Deploy me-evaluator."
    exit 1
fi

if [ -x "$(command -v minikube)" ]; then
    eval $(minikube docker-env)
fi

KEARCH_ROOT_DIR=$(cd $(dirname $0); pwd)
echo "KEARCH_ROOT_DIR = "${KEARCH_ROOT_DIR}
KEARCH_COMMON_BRANCH=${KEARCH_COMMON_BRANCH:-"dev"}
echo "KEARCH_COMMON_BRANCH = "$KEARCH_COMMON_BRANCH""
# CMD_DOCKER_BUILD="docker build --build-arg KEARCH_COMMON_BRANCH=$KEARCH_COMMON_BRANCH"
# use '--no-cache' to disable docker's cahce
CMD_DOCKER_BUILD="docker build --build-arg KEARCH_COMMON_BRANCH=$KEARCH_COMMON_BRANCH --no-cache"
echo "CMD_DOCKER_BUILD = "$CMD_DOCKER_BUILD


echo "----- Start to make namespace and configure context. -----"
cd $KEARCH_ROOT_DIR/services
kubectl --namespace=kearch apply -f kearch-namespace.yaml
kubectl --namespace=kearch apply -f local-storage-class.yaml
kubectl --namespace=kearch apply -f manual-storage-class.yaml
echo "----- Finish making namespace and configuring context. -----"

for arg in "$@"
do
    if [ $arg = medb ]; then
        # me-db
        echo
        read -p "Are you sure? This operation destroy all your database. (y/n)" yn
        if [ "$yn" != 'y' ]; then
            exit
        fi

        echo "----- Start to deploy meta DB. -----"
        cd $KEARCH_ROOT_DIR/services/me-db

        kubectl --namespace=kearch delete all -l engine=me,app=db
        kubectl --namespace=kearch apply --prune -l engine=me,app=db --recursive -f .

        # Wait until the pod is ready
        while ! kubectl rollout status statefulset me-db --namespace=kearch
        do
            sleep 1
        done
        sleep 30

        cd $KEARCH_ROOT_DIR/services/me-db

        me_db_pod_name=$(kubectl --namespace=kearch get po -l engine=me,app=db -o go-template --template '{{(index .items 0).metadata.name}}')
        echo "----- me_db_pod_name = "${me_db_pod_name}" -----"
        kubectl --namespace=kearch exec $me_db_pod_name -- mysql -uroot -ppassword -e 'DROP DATABASE IF EXISTS kearch_me_dev'
        kubectl --namespace=kearch exec $me_db_pod_name -- mysql -uroot -ppassword -e 'CREATE DATABASE kearch_me_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'

        kubectl --namespace=kearch cp $(pwd)/sql/sp_servers_schema.sql $me_db_pod_name:/tmp/sp_servers_schema.sql
        kubectl --namespace=kearch cp $(pwd)/sql/config_variables_schema.sql $me_db_pod_name:/tmp/config_variables_schema.sql
        kubectl --namespace=kearch cp $(pwd)/sql/sp_hosts_schema.sql $me_db_pod_name:/tmp/sp_hosts_schema.sql
        kubectl --namespace=kearch cp $(pwd)/sql/in_requests_schema.sql $me_db_pod_name:/tmp/in_requests_schema.sql
        kubectl --namespace=kearch cp $(pwd)/sql/out_requests_schema.sql $me_db_pod_name:/tmp/out_requests_schema.sql
        kubectl --namespace=kearch cp $(pwd)/sql/binary_files_schema.sql $me_db_pod_name:/tmp/binary_files_schema.sql
        kubectl --namespace=kearch cp $(pwd)/sql/authentication_schema.sql $me_db_pod_name:/tmp/authentication_schema.sql

        echo sp_servers_schema
        kubectl --namespace=kearch exec $me_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_me_dev < /tmp/sp_servers_schema.sql'
        echo config_variables_schema
        kubectl --namespace=kearch exec $me_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_me_dev < /tmp/config_variables_schema.sql'
        echo sp_hosts_schema
        kubectl --namespace=kearch exec $me_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_me_dev < /tmp/sp_hosts_schema.sql'
        echo in_requests_schema
        kubectl --namespace=kearch exec $me_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_me_dev < /tmp/in_requests_schema.sql'
        echo out_requests_schema
        kubectl --namespace=kearch exec $me_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_me_dev < /tmp/out_requests_schema.sql'
        echo binary_files_schema.sql
        kubectl --namespace=kearch exec $me_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_me_dev < /tmp/binary_files_schema.sql'
        echo authentication_schema
        kubectl --namespace=kearch exec $me_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_me_dev < /tmp/authentication_schema.sql'

        kubectl delete pods --namespace=kearch -l engine=me,app=db


        $KEARCH_ROOT_DIR/me_db_checker.sh
        echo "----- Finish deployment of meta DB. -----"
    fi

    if [ $arg = mefront ] || [ $arg = all ]; then
        # me-front
        echo
        echo "----- Start deployment of meta front. -----"
        cd $KEARCH_ROOT_DIR

        $CMD_DOCKER_BUILD -f packages/me-front/Dockerfile -t kearch/me-front .

        cd $KEARCH_ROOT_DIR/services/me-front

        kubectl --namespace=kearch apply --prune -l engine=me,app=front --recursive -f .

        kubectl delete pods --namespace=kearch -l engine=me,app=front

        echo "----- Finish deployment of meta front. -----"
    fi

    if [ $arg = meqproc ] || [ $arg = all ]; then
        # me-query-processor
        echo
        echo "----- Start deployment of meta query processor. -----"
        cd $KEARCH_ROOT_DIR/packages/me-query-processor

        $CMD_DOCKER_BUILD -t kearch/me-query-processor .

        cd $KEARCH_ROOT_DIR/services/me-query-processor

        kubectl --namespace=kearch apply --prune -l engine=me,app=query-processor --recursive -f .

        kubectl delete pods --namespace=kearch -l engine=me,app=query-processor

        echo "----- Finish deployment of meta query processor. -----"
    fi

    if [ $arg = megate ] || [ $arg = all ]; then
        # me-gateway
        echo
        echo "----- Start deployment of meta gateway. -----"
        cd $KEARCH_ROOT_DIR/packages/me-gateway

        $CMD_DOCKER_BUILD -t kearch/me-gateway .

        cd $KEARCH_ROOT_DIR/services/me-gateway

        kubectl --namespace=kearch apply --prune -l engine=me,app=gateway --recursive -f .

        kubectl delete pods --namespace=kearch -l engine=me,app=gateway

        echo "----- Finish deployment of meta gateway. -----"
    fi

    if [ $arg = meeval ] || [ $arg = all ]; then
        # me-eval
        echo
        echo "----- Start deployment of meta evaluator. -----"
        cd $KEARCH_ROOT_DIR

        $CMD_DOCKER_BUILD -f packages/me-evaluator/Dockerfile -t kearch/me-evaluator .

        cd $KEARCH_ROOT_DIR/services/me-evaluator

        kubectl --namespace=kearch apply --recursive -f .

        kubectl delete pods --namespace=kearch -l engine=me,app=evaluator

        echo "----- Finish deployment of meta evaluator. -----"
    fi

    if [ $arg = meadmin ] || [ $arg = all ]; then
        # me-admin
        echo
        echo "----- Start deployment of meta admin. -----"
        cd $KEARCH_ROOT_DIR

        $CMD_DOCKER_BUILD -f packages/me-admin/Dockerfile -t kearch/me-admin .

        cd $KEARCH_ROOT_DIR/services/me-admin

        kubectl --namespace=kearch apply --prune -l engine=me,app=admin --recursive -f .

        kubectl delete pods --namespace=kearch -l engine=me,app=admin

        echo "----- Finish deployment of meta admin. -----"
    fi

    if [ $arg = mesup ] || [ $arg = all ]; then
        # me-summary-updater
        echo
        echo "----- Start deployment of meta summary updater. -----"
        cd $KEARCH_ROOT_DIR

        $CMD_DOCKER_BUILD -f packages/me-summary-updater/Dockerfile -t kearch/me-summary-updater .

        cd $KEARCH_ROOT_DIR/services/me-summary-updater

        kubectl --namespace=kearch apply --prune -l engine=me,app=summary-updater --recursive -f .

        kubectl delete pods --namespace=kearch -l engine=me,app=summary-updater

        echo "----- Finish deployment of meta summary updater. -----"
    fi
done

echo
