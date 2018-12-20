# Specialist Crawler Parent
This is a controller of crawler children.
## APIs used in this package
### Database
#### Fetch urls from FIFO queue in database
Access URL
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
#### Push urls to FIFO queue in database
Access URL
```
$(ip adress of the database server)/push_urls_to_queue
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
$(ip adress of the load blancer of crawler children)/crawl_a_page
```
Expected return page  
abbreviated
