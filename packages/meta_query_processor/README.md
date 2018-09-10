# Meta Query Processor
## Retrieve
This API takes queries and return the result of search in a specific search engine.  
The alogrithm of choose a specific search engine is following.  
It calcultes sum of frequency of queries for each specific search engine.  
And it takes most high frequent engine from them.  

Access URL (GET)
```
$(ip adress of meta query processor)/retrieve?queries=facebook+yahoo&max_urls=100
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
]}
```
