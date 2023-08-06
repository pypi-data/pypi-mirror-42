```
pip install microlog
```
# microlog
Simple and lightweight logging

## Getting started
```
from microlog import Logger
my_logs = Logger()
my_logs.log("Hello World!")
```
* Logs can be created with the following methods
  * `log()`
  * `debug()`
  * `info()`
  * `warning()`
  * `error()`
  * `critical()`
* Logs from a current session are saved in memory and can be viewed with the `logs()` method.

## Options
There are four options available when creating a new Logger instance.
### 1. Filename
When creating a new Logger, a file will be created in your current directory. By default, the name will be the current time with the format _yyyy-mm-dd hh:mm:ss_. You may provide a custom name for the log file with the `filename` parameter.
```
Logger(filename = "my_logs")
```
Logs are written using the append option so they can be added to existing log files.
### 2. File
By default, a log file will be created when creating a new Logger. Set the `file` parameter to `False` to prevent a log file from being created.
```
Logger(file = False)
```
### 3. Console
Log messages will not be written to the console by default. Set the `console` parameter to `True` to see log messages in the console.
```
Logger(console = True)
```
### 4. Time format
All references to time will be local date-time by default. To use a UTC timestamp, set the `format` parameter to `"ts"`.  This will apply to default log file names and times in the log files.
```
Logger(format = "ts")
```
