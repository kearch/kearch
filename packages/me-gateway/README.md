# Meta Gateway
This container should export on 10080 port of host.  
This container have following two APIs.

## Featch a dump from sp
URL (GET)
```
$(ip adress of meta gateway)/me/gateway/fetch_a_dump&sp_host=192.168.99.100 (GET)
```
Result
```
{
    'google':1050,
    'facebook':10022
}
```

## Add a dump of sp to me-db
URL (POST)
```
$(ip adress of meta gateway)/me/gateway/add_a_dump (POST)
```
Scheme of Posted JSON
```
{
    'data':{
        'ip':ip address of this specialist server,
        'summary':{
            word:the number of documents in the DB which contains the word.
        }
    }
}
```
Posted JSON example
```
{
    'data':{
        'ip':'10.229.55.117',
        'summary':
        {
            'google':1050,
            'facebook':10022
        }
    }
}
```

## [DEPRECATED] Register DB Information to Database
This API takes a summary of specialist DB and register it to meta DB.  
*CAUTION* Access this URL using KearchRequester.  

URL (POST)
    ```
$(ip adress of meta gateway)/add_new_sp_server (POST)
    ```
    Scheme of Posted JSON
    ```
{
    'ip':ip address of this specialist server,
        'summary':
        {
word:the number of documents in the DB which contains the word.
        }
}
```
Posted JSON example
```
{
    'ip':'10.229.55.117',
        'summary':
        {
            'google':1050,
            'facebook':10022
        }
}
```
## Process Search Query
Meta search engine issues search queries and throw them to specialist search engines.  
This API cathes their queries and returns the result.  

URL (GET)
    ```
    $(ip adress of meta gateway)/retrieve?queries=facebook+yahoo&max_urls=100&sp_host=10.229.55.44
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
