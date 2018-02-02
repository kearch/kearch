#! /bin/bash

d=keach`date +"%Y%m%d%k%M%S"`.db
mv keach.db ${d}

python3 ./setup_database.py
python3 ./average_document.py ./random_url_list
python3 topic_detect.py computer_science_url_list random_url_list
