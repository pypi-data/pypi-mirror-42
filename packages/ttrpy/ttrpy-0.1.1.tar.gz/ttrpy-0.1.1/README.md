# ttrpy

[![Build Status](https://travis-ci.com/joelowj/ttrpy.svg?token=zM8uDnAP2GXz8Hagm4hw&branch=master)](https://travis-ci.com/joelowj/ttrpy)

Technical Trading Rule Python is an open source library for popular technical analysis function for financial time series data.

## Installation

To install the current release:

```
$ pip install ttrpy
```

## Usage

```python
import pandas as pd
import ttrpy.trend.sma import sma

# read your own price data into pandas either from .csv or API
df = pd.read_csv("weekly_MSFT.csv").sort_values(by="timestamp").reset_index(drop=True)

df.head(3)

  timestamp    open     high     low     close   volume
0 1998-01-09  131.25   133.63   125.87   127.00   ...
1 1998-01-16  124.62   135.38   124.37   135.25   ...
2 1998-01-23  134.13   139.88   134.00   138.25   ...

df = sma(df, "close", "sma", 200)

```

## Contribution Guidelines

**If you want to contribute to ttrpy, be sure to review the [contribution
guidelines](CONTRIBUTING.md). This project adheres to ttrpy's
[code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.**

To get the local repository set up for development,

```
$ pip install virtualenv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
