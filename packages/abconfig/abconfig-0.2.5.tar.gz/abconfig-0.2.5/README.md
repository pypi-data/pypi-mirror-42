## Easy-to-use abstract base class with hierarchical loading


### How to use:

```
from abconfig import ABConfig


class YourConfig(ABConfig):
    """ My config."""

    # Define sections and default values
    postgres = dict(
        host='127.0.0.1',
        port='5432',
        user='your_user',
        password='your_pass'
    )

    redis = dict(
        host='127.0.0.1',
        port='6379',
        db='0'
    )


config = YourConfig()

# Get section like a dict
dbconfig = config['postgres'])

# Get all:
print(config.get())
```

### File loader

> Values from this loader will be overwritten with values from Environment loader

The default is to search for a file called _config/config.json/config.yaml_ in the directory from which the application is started, you can force a file path by adding an attribute **filepath** to the class

```
class MainConf(ABConfig):
    file_path = '/etc/main.conf'
    ...
```
or by define a variable **CONFIG_PATH**, but the attribute has the highest priority and is preferred.


### Environment loader

> This loader has the highest priority

The variable name make up of the section name + '\_' character and the parameter name (is key in the default values dictionary) in upper case, for example, if exist class:

```
class LogConfig(ABConfig):
    logging = dict(
        file='/var/log/my.log'
    )
    ...
```
environment variable will be: **LOGGING_FILE**.
