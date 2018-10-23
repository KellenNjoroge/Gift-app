#!/usr/bin/env bash
export SECRET_KEY=gift
export DATABASE_URL=postgresql+psycopg2://kellen:kellen@localhost/gift
export MAIL_USERNAME=muthonkel@gmail.com
export MAIL_PASSWORD=bulgaria36
python3.6 manage.py server

