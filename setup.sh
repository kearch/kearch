#! /bin/bash

rm keach.db
python3 ./setup_database.py
python3 ./average_document.py ./random_url_list
python3 lda_topic_detect.py computer_science_url_list random_url_list
