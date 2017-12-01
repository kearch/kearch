#! /bin/bash

rm keach.db
python3 ./setup_database.py
python3 ./average_document.py ./seed_url_list
