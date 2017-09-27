import os
import sys
import site

os.environ["DATABASE"] = "docs/summarybot.db"
os.environ["SLACK_BOT_NAME"] = "reverte"
os.environ["SLACK_CLIENT_ID"] = "73314827649.243504314342"
os.environ["SLACK_CLIENT_SECRET"] = "f6a00ebab0d708643dec0328fb5ae112"
os.environ["SLACK_VERIFICATION_TOKEN"] = "EpMyFd45hPDhPe3Gj8QNTS9u"
os.environ["PRIVATE_KEY"] = "/etc/letsencrypt/archive/bot.myshortreport.com/privkey1.pem"
os.environ["FULL_CHAIN"] = "/etc/letsencrypt/archive/bot.myshortreport.com/fullchain1.pem"
os.environ["CERT"] = "/etc/letsencrypt/archive/bot.myshortreport.com/cert1.pem"

base_path       = '/srv/summarybot'
packages        = '%s/venv/lib/python3.5/dist-packages' % base_path
packages64      = '%s/venv/lib64/python3.5/dist-packages' % base_path
venv_start      = '%s/venv/bin/activate_this.py' % base_path

# Add virtualenv site packages
site.addsitedir(packages)
site.addsitedir(packages64)

# Fired up virtualenv before include application
exec(open(venv_start).read(), dict(__file__=venv_start))

# Path of execution
sys.path.append(base_path)

# import app as application
from api import api as application