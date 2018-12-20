#!/bin/bash

cat <(echo "yes") - | python ~/projects/staging/ballet_app/ballet/backend/manage.py collectstatic
sudo supervisorctl restart stagingballet
