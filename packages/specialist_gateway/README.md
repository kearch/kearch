# Specialist Gateway
This container should export on 10080 port of host.  
This container have following two APIs.
## Register DB Information to Meta
The Admin container in specialist search engine register specialist DB to a meta search engine.  
In registeration, the specialist must send the summary of DB to the meta.  
This API takes the summary and send it to the meta.  

URL (POST)
```
$(ip adress of meta query processor)/send_DB_summary (POST)
```
Scheme of Posted JSON
```
{
    'ip':ip address of this specialist server
    'data':
    {
        word:the number of documents in the DB which contains the word.
    }
}
```
Posted JSON example
```
{
    'ip':'10.229.55.117',
    'data':
    {
        'google':1050,
        'facebook':10022
    }
}
```
## Process Search Query from Meta
Meta search engine issues search queries and throw them to specialist search engines.  
This API cathes their queries and returns the result.  

URL (GET)
```
$(ip adress of meta query processor)/retrieve_gateway?queries=facebook+yahoo&max_urls=100
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
