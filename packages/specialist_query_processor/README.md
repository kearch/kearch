# Specialist Query Processor
This directory is made for specialist_query_processor.
## API of specialist_query_processor
URL
```
$(ip adress of specialist_query_processor):10080/retrieve?queries=google+facebook&max_urls=100
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
