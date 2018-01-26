#! /bin/bash

echo "Registered webpages:"
sqlite3 keach.db "SELECT COUNT(*) FROM date_to_link where 10 < last_date"

echo "Webpages in crawler queue:"
sqlite3 keach.db "SELECT COUNT(*) FROM date_to_link"

echo "Unique url in pagerank_now:"
sqlite3 keach.db "SELECT COUNT(DISTINCT link) FROM pagerank_now"

echo "All url in pagerank_now:"
sqlite3 keach.db "SELECT COUNT(*) FROM pagerank_now"

# echo "Unique url in pagerank_next:"
# sqlite3 keach.db "SELECT COUNT(DISTINCT link) FROM pagerank_next"
echo "All url in pagerank_next:"
sqlite3 keach.db "SELECT COUNT(*) FROM pagerank_next"
echo "New arrived pages:"
sqlite3 keach.db "select link from date_to_link where 10 < last_date order by last_date desc limit 5"
echo "Database size:"
du -h keach.db
