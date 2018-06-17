# Specialist Crawler Parent
This is a controller of crawler children.
## APIs used in this package
### Database
#### Push urls to FIFO queue in database
Access URL
```
$(ip adress of the database server)/push_links_to_queue
```
JSON for POST method
```
{'datum':[
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

#### Fetch urls from FIFO queue in database
Access URL
```
$(ip adress of the database server)/get_next_urls?max_urls=100
```
#### Push datum of webpage to database
Access URL
```
$(ip adress of the database server)/push_webpage_to_database
```
JSON for POST method
```
{'urls':[
    'http://www.google.com',
    'http://www.facebook.com']
}
```
### Crawler Children
- Get infomation of a given url
```
$(ip adress of the load blancer of crawler children)/crawl_a__page
```
