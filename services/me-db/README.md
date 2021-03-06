# me-db service

## Prerequisites

You need to run the following commands first.

```sh
cd path/to/kearch
cd services
kubectl create -f kearch-namespace.yaml
kubectl config set-context kearch-minikube \
  --namespace=kearch \
  --cluster=minikube \
  --user=minikube
kubectl config use-context kearch-minikube
kubectl config current-context # => should display `kearch-minikube`
```

## Usage

Create kubernetes resources from yaml files.

```sh
cd path/to/kearch
cd services/me-db

kubectl apply -f me-db-pv.yaml
kubectl apply -f me-mysql-pvc.yaml
kubectl apply -f me-db-deployment.yaml
kubectl apply -f me-db-service.yaml
```

Create tables.

```sh
cd path/to/kearch
cd services/me-db

me_db_pod_name=$(kubectl get po -l engine=me,app=db -o go-template --template '{{(index .items 0).metadata.name}}')
kubectl exec $me_db_pod_name -- bash -c 'echo "CREATE DATABASE kearch_me_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" | mysql -uroot -ppassword'
kubectl cp $(pwd)/sql/sp_servers_schema.sql $me_db_pod_name:/tmp/sp_servers_schema.sql
kubectl exec $me_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_me_dev < /tmp/sp_servers_schema.sql'
```

`me-db` service can be resolved as `me-db.kearch.svc.cluster.local` .



# APIs of Meta DB
## Get summaries
Access URL (GET)
```
$(ip adress of the database server)/me/db/get_sp_summaries
```
Return JSON
```
{
    '192.168.99.100':{
        'google': 10,
        'facebook': 20
    },
    '192.168.99.101':{
        'lisp':10
    }
}
```
## Get connection requests
Access URL (GET)
```
$(ip adress of the database server)/me/db/get_connection_requests
```
Return JSON
```
{
    'in':{
        '192.168.99.100':true
    },
    'out':{
        '192.168.99.123':false
    }
}
```
## Add a connection request
Access URL (POST)
```
$(ip adress of the database server)/me/db/add_a_connection_request
```
JSON for POST
```
{
    {
        'in_or_out':'in',
        'sp_host':'192.168.99.100'
    }
}
```
## Approve a connection request
Access URL (PUT)
```
$(ip adress of the database server)/me/db/approve_a_connection_request
```
JSON for PUT
```
{
    {
        'in_or_out':'in',
        'sp_host':'192.168.99.100'
    }
}
```
## Add new sp server to meta DB
This API is accessed using KearchRequester.   
So the acutual JSON is wrapped by KearchRequester.
Access URL (POST)
```
$(ip address of meta DB)/add_new_sp_server
```
Given JSON Example
```
{
    'host':'10.229.55.110',
    'summary':{
        'google':100,
        'facebook':20,
        'yahoo':120
    }
}
```
Structure of JSON
```
{
    'ip':ip adress of the sp server,
    'database_dump':{
        word1:the number of documents containing word1,
        word2:the number of documents containing word2,
        word3:the number of documents containing word3
    }
}
```
## Select sp server for queries
Access URL (GET)
```
$(ip address of meta DB)/add_new_sp_server?queries=haskell+language
```
Example of returned JSON
```
{
    'haskell':{
        '192.168.99.100':1.00
    },
    'language':{
        '192.168.99.100':1.00
    }
}
```
## List up sp servers in me DB
This API returns sp servers and their short description in me DB.
Access URL(GET)
```
$(ip address of meta DB)/list_up_sp_servers
```
Example of returned JSON
```
{
    '192.168.99.100':'computer',
    'hogehoge.example.com':'kyoto'
}
```
## Set Config Variables
This API could be used to set public/protected status.
Access URL (POST)
```
$(ip address of meta DB)/me/db/set_config_variables
```
POSTed JSON Example
```
{
    'public_or_protected':'public'
}
```
## Get Config Variables
This API could be used to get public/protected status.
Access URL (POST)
```
$(ip address of meta DB)/me/db/get_config_variables
```
GETed JSON Example
```
{
    'public_or_protected':'public'
}
```

