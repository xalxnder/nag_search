#!usr/local/bin/python3.8

import sys
import site

activate_this = '/var/www/html/nag_search/.venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

site.addsitedir('/var/www/html/nag_search/lib/python3.6/site-packages')

sys.path.insert(0, '/var/www/html/nag_search')

from app import app as application

