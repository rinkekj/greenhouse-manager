#!/usr/bin/env sh

python3 manage.py recreate_db
python3 manage.py setup_dev
echo "Not performing 'mysql < populate_database.sh'"
echo "Not performing 'python3 manage.py add_fake_data'"
python3 manage.py restore
