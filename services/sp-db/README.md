# sp-db service

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
cd services/sp-db

kubectl apply -f sp-db-pv.yaml
kubectl apply -f mysql-pvc.yaml
kubectl apply -f sp-db-configmap.yaml
kubectl apply -f sp-db-deployment.yaml
kubectl apply -f sp-db-service.yaml
```

Create tables.

```sh
cd path/to/kearch
cd services/sp-db

sp_db_pod_name=$(kubectl get po -l engine=sp,app=db -o go-template --template '{{(index .items 0).metadata.name}}')
kubectl exec $sp_db_pod_name -- bash -c 'echo "CREATE DATABASE kearch_sp_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" | mysql -uroot -ppassword'
kubectl cp $(pwd)/sql/webpages_schema.sql $sp_db_pod_name:/tmp/webpages_schema.sql
kubectl cp $(pwd)/sql/url_queue_schema.sql $sp_db_pod_name:/tmp/url_queue_schema.sql
kubectl exec $sp_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_sp_dev < /tmp/webpages_schema.sql'
kubectl exec $sp_db_pod_name -- bash -c 'mysql -uroot -ppassword kearch_sp_dev < /tmp/url_queue_schema.sql'
```

`sp-db` service can be resolved as `sp-db.kearch.svc.cluster.local` .



# APIs of Specialist Database Server
## Get connection requests
Access URL (GET)
```
$(ip adress of the database server)/sp/db/get_connection_requests
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
$(ip adress of the database server)/sp/db/add_a_connection_request
```
JSON for POST
```
{
    {
        'in_or_out':'in',
        'me_host':'192.168.99.100'
    }
}
```
## Approve a connection request
Access URL (PUT)
```
$(ip adress of the database server)/sp/db/approve_a_connection_request
```
JSON for PUT
```
{
    {
        'in_or_out':'in',
        'me_host':'192.168.99.100'
    }
}
```

## Dump the Content of Database
Access URL (GET)
```
$(ip adress of the database server)/dump_database
```
Return JSON
- Count how many urls exists in the database which contain each words
```
{
  'google':100,
  'facebook':20,
  'lisp':10
  ...
}
```
## [Deprecated] Retrieve documents with given queries
Access URL (GET)
- Multiple queries are connected by '+'.
```
$(ip adress of the database server)/retrieve?queries=facebook+google&max_urls=20
```
Return JSON
- Return top ${max_urls} pages for given queries
- Criterion for selecting top ${max_urls} urls is descending order of
((queries and title_words are overlapping)?1:0, sum of tfidf values corresponding to queries)
```
{
  'www.google.com':{
    'title_words':['google','usa'],
    'summary':'google is strong',
    'tfidf':{
      'google':1.0
    }
  }
}
```
## [Deperecated] Push data of webpage to database
Access URL (POST)
```
$(ip adress of the database server)/push_webpage_to_database
```
JSON for POST method
```
{'data':[
    {
        'url':'www.google.com',
        'title_words':['google','usa'],
        'summary':'google is strong',
        'tfidf':{
            'google':1.0,
            'facebook':2.0
        }
    },...
]}
```

## [TODO] Update dump of sp-db
Access URL (POST)
```
$(ip adress of the database server)/update_dump
```
JSON for POST method
```
{'data':
    {
        'haskell': 10,
        'lisp': 5
    }
}
```

## Fetch urls from FIFO queue in database
Access URL (GET)
```
$(ip adress of the database server)/get_next_urls?max_urls=100
```
Expected return page
```
{'urls':[
    'http://www.google.com',
    'http://www.facebook.com']
}
```
## Push urls to FIFO queue in database
Access URL (POST)
```
$(ip adress of the database server)/push_links_to_queue
```
JSON for POST method
```
{'urls':[
    'http://www.google.com',
    'http://www.facebook.com']
}
```

## Push crawled urls to database
Path
```
/push_crawled_urls
```
JSON
```
{'data':[
    {
        'url':'www.google.com',
    },...
]}
```

## [TODO] Push binary file to the database
This API is used to push configure data of crawlers.
Path
```
[POST] /push_binary_file
```
JSON
```
{'data':{
    'filename': 'hogefile',
    'contents': "binary contents"}
}
```

## [TODO] Check the timestamp of binary file
Path
```
[GET] /chec_binary_file_timestamp?filename=hogename
```
JSON
```
{
    'timestamp': "UNIX time when the file is uploaded"
}
```
## [TODO] Pull binary file from the database
This API is used to pull configure data of crawlers.
Path
```
[GET] /pull_binary_file?filename=hgoefile
```
JSON
```
{
    'timestamp': "UNIX time when the file is uploaded",
    'contents': "binary contents"
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
    'data':{
        'public_or_protected':'public'
    }
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

