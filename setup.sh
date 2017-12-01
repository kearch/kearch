#! /bin/bash

rm keach.db
python3 ./setup_database.py
python3 ./average_document.py ./random_url_list
