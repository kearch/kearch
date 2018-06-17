# Specialist Crawler Parent
This is a controller of crawler children.
## APIs used in this package
### Database
- Push urls to FIFO queue in database
Example
```
$(ip adress of the database server)/api/push_links_to_queue
```
- Fetch urls from FIFO queue in database
Example
```
$(ip adress of the database server)/api/get_next_urls?max_urls=100
```
- Push datum of webpage to database
Example
```
$(ip adress of the database server)/api/push_webpage_to_database
```
### Crawler Children
- Get infomation of a given url
```
$(ip adress of the load blancer of crawler children)/crawl_a__page
```
