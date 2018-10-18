# Meta Gateway
This container should export on 10080 port of host.  
This container have following two APIs.
## Register DB Information to Database
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
$(ip adress of meta gateway)/retrieve?queries=facebook+yahoo&max_urls=100&ip_sp=10.229.55.44
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
