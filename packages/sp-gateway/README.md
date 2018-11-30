# Specialist Gateway
This container should export on 10080 port of host.  
This container have following two APIs.
## Add a connection request
URL (POST)
```
$(ip adress of sp gateway)/sp/gateway/add_a_connection_request (POST)
```
JSON to POST
```
{
    'me_host':'192.168.99.100'
}
```
## Sebd a connection request
URL (POST)
```
$(ip adress of sp gateway)/sp/gateway/send_a_connection_request (POST)
```
JSON to POST
```
{
    'me_host':'192.168.99.100'
}
```
## [DEPRECATED] Register DB Information to Meta
The Admin container in specialist search engine register specialist DB to a meta search engine.  
In registeration, the specialist must send the summary of DB to the meta.  
This API takes the summary and send it to the meta.  
*CAUTION* Access this URL using KearchRequester.  

URL (POST)
```
$(ip adress of specialist gateway)/send_DB_summary (POST)
```
Scheme of Posted JSON
```
{
    'ip_sp':ip address of this specialist server,
    'ip_me':ip address of meta server to register,
    'summary':
    {
        word:the number of documents in the DB which contains the word.
    }
}
```
Posted JSON example
```
{
    'ip_sp':'10.229.55.117',
    'ip_me':'10.229.55.114',
    'summary':
    {
        'google':1050,
        'facebook':10022
    }
}
```
## Send a database summary from sp to me
URL (POST)
```
$(ip adress of specialist gateway)/sp/gateway/send_a_dump (POST)
```
Scheme of Posted JSON
```
{
    'data':{
        'ip_sp':ip address of this specialist server,
        'ip_me':ip address of meta server to register,
        'summary':
        {
word:theber of documents in the DB which contains the word.
        }
    }
}
```
Posted JSON example
```
{
    'data':{
        'ip_sp':'10.229.55.117',
        'ip_me':'10.229.55.114',
        'summary':
        {
            'google':1050,
            'facebook':10022
        }
    }
}
```

## Get a database summary
Access URL (GET)
```
$(ip adress of the database server)/sp/gateway/get_a_dump&me_host=192.168.99.100
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

## Process Search Query from Meta
Meta search engine issues search queries and throw them to specialist search engines.  
This API cathes their queries and returns the result.  

URL (GET)
    ```
    $(ip adress of specialist gateway)/retrieve?queries=facebook+yahoo&max_urls=100
    ```
    Return JSON
    ```
{'data':[
    {
        'url':'www.google.com',
        'title_words':['google','usa'],
        'summary':'google is strong',
        'score':11.0
    },...
]}
```
