[![Build Status](https://travis-ci.org/stavrakidis/pd_multiprocessing.png)](https://travis-ci.org/stavrakidis/pd_multiprocessing)
[![Coverage Status](https://coveralls.io/repos/github/stavrakidis/pd_multiprocessing/badge.svg?branch=master)](https://coveralls.io/github/stavrakidis/pd_multiprocessing?branch=master)
[![Documentation Status](https://readthedocs.org/projects/pd-multiprocessing/badge/?version=latest)](https://pd-multiprocessing.readthedocs.io/en/latest/?badge=latest)

# pd_multiprocessing

pd_multiprocessing provides a simple, parallelized function to apply a user defined function rowwise on a Pandas Dataframe.

## Requirements

- [pandas](https://pandas.pydata.org/) 0.22.0+
- [pytest](ttps://docs.pytest.org/en/latest/) 3.4.1+

### Documentation

If you want to build the documentation, you need the following packages:

- Sphinx
- sphinx_rtd_theme
- m2r

## Installation

You can easily install pd_multiprocessing via
```python
pip install pd-multiprocessing
```

## Usage

A typical usage looks like this

```python
import pandas as pd
from pd_multiprocessing.map import df_map


def twotimes(row):
    row['col2'] = row['col1']*2
    return row


if __name__ == '__main__':
    df = pd.DataFrame.from_dict({'col1': range(100)})
    print(df_map(twotimes, df))
```
