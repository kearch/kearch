# Meta Query Processor
## Retrieve
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
