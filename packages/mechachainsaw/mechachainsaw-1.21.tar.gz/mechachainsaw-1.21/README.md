# Mecha Chainsaw

This project is under current development, and is intended as a logging library for [mechasqueak3](https://github.com/FuelRats/pipsqueak3).

However, it does have applications as a standalone logging tool.

This project is currently in *pre-release*.  Use at your own risk!

### Requirements
* Python 3.7+
* coloredlogs library

### Installation
This is python library.  Install using pip/pipenv
and import mechachainsaw with ``import mechachainsaw``


### Usage

```py
from mechachainsaw import Logger``
log = Logger("Namespace", "Logfile.txt")
log.info("This is an info-level entry!")
```


will get you:
```
<2019-01-12 15:17:40,572 Namespace> [INFO] This is an info-level entry!
```


### License

*Mecha Chainsaw* is licensed under the BSD 3-Clause License.

