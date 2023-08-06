# jvstats, a commandline tool for retrieving stats

[![Build Status](https://travis-ci.com/jaimeviloria/jvstats.svg)](https://travis-ci.com/jaimeviloria/jvstats)
[![PyPI version](https://badge.fury.io/py/jvstats.svg)](https://badge.fury.io/py/jvstats)

## Development Requirements
* make
* python3
* virtualenv

## Package Requirements
* python3

## Installation

`pip install jvstats`

## Usage: 

Example for the module
```
>>> from jvstats import Delays
>>> d = Delays()
>>> d.delays
[]
>>> d.addDelay(100)
[100]
>>> d.medians
[-1]
>>> d.sliding_window
[100]
>>> d.addDelay(102)
[100, 102]
>>> d.medians
[-1, 101]
>>> d.sliding_window
[100, 102]
>>> d.addDelay([101,110,120])
[100, 102, 101, 110, 120]
>>> d.sliding_window
[101, 110, 120]
>>> d.medians
[-1, 101, 101, 102, 110]
>>> d.delays=[100,102]
>>> d.medians
[-1, 101]
```

When using the tool on commandline

1. piping from stdin (in this case using a file)
```
$ cat test1.csv 
100
102
101
110
120
115
$ cat test1.csv | jvstats delays medians
-1
101
101
102
110
115

```

2. from a file

```
$ cat test1.csv
100
102
101
110
120
115
$ jvstats delays medians --filename test1.csv 
-1
101
101
102
110
115
```

## Development

### Build your own specific version of python to test against:

The created project also contains a set of Makefiles which will build and run tests against your code. 

`make`  will build you the latest version of python and then proceed for testing

Or choose a specific python version to test against. 

`make PYTHON_VERSION=3.6`

Note that once built, you can easily swap between python versions just by executing the make command. If the python version you need was already built in the build directory, then we simply update the symlink of the virtualenv and ensure requirements.txt is installed.

## Testing

`make test`
creates the virtualenv and python binaries necessary for testing as well as running the unittests

