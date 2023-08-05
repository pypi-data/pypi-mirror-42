# What is this?

This is a set of utilities used by https://Layer7.Solutions for the software tools we create. It includes a logger with default configuration information we setup as well as an oAuth wrapper to be able to pull login information from a custom database.

To create the oAuth database, the following creation SQL can be used:

```sql
create table oauth_data
(
  username    text not null
    constraint oauth_pkey
      primary key,
  password    text,
  app_id      text,
  app_secret  text,
  app_refresh text,
  agent_of    text
);
```
# How To Build And Install

1. Be inside the root of the folder
2. Run `python3 setup.py sdist`
3. Run `pip install .`

---

# How To Use:

### Logger:

This creates a custom logger using default file handler, sentry.io integration, and log rotation. A default logspath is set to '/opt/skynet/RedditBots/logs/' however you can override that to your own location.
Initialization and configuration:

```Python
import logging
import logging.config
from layer7_utilities import LoggerConfig

__botname__     = 'Short_Name_For_The_Bot'
__description__ = 'Description of the bot'
__author__      = 'Authors Name/Info'
__version__     = '1.2.3'
__dsn__         = 'Get from Sentry.io'

# Create the logger
logspath = 'Path/To/The/Logs/Folder/'  # With trailing backslash.
loggerconfig = LoggerConfig(__dsn__, __botname__, __version__, logspath)
logging.config.dictConfig(loggerconfig.get_config())
logger = logging.getLogger('root')
logger.info(u"/*********Starting App*********\\")
logger.info(u"App Name: {} | Version: {}".format(__botname__, __version__))
```


### Auth

Auth relies on a custom table housing the Reddit application ID, Secret, Username, Password, etc. This is not intended to be setup by anyone else. However if you have access to our database, or are writing a bot that will take advantage, then it can be setup as such.

In the Layer 7 environment the Auth Database Table is 'TheTraveler'.

```Python
from layer7_utilities import oAuth

__botname__     = 'Short_Name_For_The_Bot'
__description__ = 'Description of the bot'
__author__      = 'Authors Name/Info'
__version__     = '1.2.3'
__dsn__         = 'Get from Sentry.io'
__agent_of__    = 'category value'

auth = oAuth()
auth.get_accounts(__agent_of__, __description__, __version__, __author__, __botname__, DB_USERNAME, DB_PASSWORD, DB_HOST, DatabaseTableName)

for account in auth.accounts:
    r = account.login()
    me = r.user.me()
    print('Started Reddit Instance: u/%s' % me)
```