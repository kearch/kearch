# Meta Query Processor
## Retrieve
This API takes queries and return the result of search in a specific search engine.  
The alogrithm of choose a specific search engine is following.  
It calcultes sum of frequency of queries for each specific search engine.  
And it takes most high frequent engine from them.  

Access URL (GET)
You can specify the sp server optionally.
```
$(ip adress of meta query processor)/retrieve?queries=facebook+yahoo&max_urls=100
$(ip adress of meta query processor)/retrieve?queries=facebook+yahoo&max_urls=100&sp=192.168.99.100
```
Return JSON
```
{'data':[
    {
        'url':'www.google.com',
        'title_words':['google','usa'],
        'title': 'google_in_usa',
        'summary':'google is strong',
        'score':11.0
    },...
  'sp_host':'192.168.99.100'
]}
```
