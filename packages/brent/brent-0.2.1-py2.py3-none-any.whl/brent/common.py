"""
The `brent.common` module contains common functions that can be
used while working with dataframes and brent graphs. They are also
used internally by the library.
"""
import logging
from itertools import islice

import numpy as np
import pandas as pd


def make_fake_df(nodes=6, rows=100, values=2, seed=42):
    """
    Creates a fake and random dataframe that can be used for demos.

    ## Inputs:

    - **nodes**: the number of nodes/variables to be generated
    - **rows**: the number of rows of fake data to generate
    - **values**: the different values that the variables can take
    - **seed**: the seed value for the random numbers to be generated

    ## Example

    ```
    from brent.common import make_fake_df
    # let's start with a new dataset
    df = make_fake_df(nodes=4, rows=1000, values=4, seed=41)
    ```
    """
    letters = 'abcdefghijklmnopqrstuvwxyz'
    np.random.seed(seed)
    if nodes > 26:
        raise ValueError('only allow 26 letters in the alfabet')
    return pd.DataFrame({k: np.random.randint(0, values, rows) for k in letters[:nodes]})


def normalise(x):
    """
    Simply normalises a numpy-like array or pandas-series.

    ## Inputs
    - **x**: a numpy array of pandas series

    ## Example

    ```
    import numpy as np
    from brent.common import normalise
    normalise(np.array([1,2,3,4]))
    ```
    """
    return x / x.sum()


def quantize_column(column, parts=4):
    """
    Turns a continous dataset into a discrete one by splitting
    it into quantiles.

    ## Inputs
    - **column**: a numpy array of pandas series
    - **parts**: the number of parts to split the data into

    ## Example

    ```
    import numpy as np
    from brent.common import quantize_column
    quantize_column(np.array([1,2,3,4]), parts=2)
    ```
    """
    return pd.cut(column, parts, labels=range(1, parts+1))


def window(seq, n=2):
    """
    Calculates a moving window over an iterable.

    ## Inputs
    - **seq**: an iterable sequence
    - **n**: the size of the window, typically this is equal to 2

    ## Example

    ```
    from brent.common import window

    list(window([1,2,3,4), n=2))
    ```
    """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def check_node_blocking(arrow_before, arrow_after, name):
    given = "given" in name
    if (arrow_before == '<-') and (arrow_after == '->'):
        blocking = True if given else False
        logging.debug(f"checking: ... {arrow_before} {name} {arrow_after} ... type: `split` blocking: {blocking}")
    elif (arrow_before == '->') and (arrow_after == '<-'):
        blocking = False if given else True
        logging.debug(f"checking: ... {arrow_before} {name} {arrow_after} ... type: `collider` blocking: {blocking}")
    elif arrow_before == arrow_after:
        blocking = True if given else False
        logging.debug(f"checking: ... {arrow_before} {name} {arrow_after} ... type: `chain` blocking: {blocking}")
    else:
        raise ValueError(f"check arrow_before/arrow_after now:{arrow_before}, {arrow_after}")
    return blocking


def is_path_blocked(path_list):
    for idx, name in enumerate(path_list):
        if idx in [0, len(path_list) - 1]:
            pass
        elif name in ['<-', '->']:
            pass
        else:
            arrow_before = path_list[idx - 1]
            arrow_after = path_list[idx + 1]
            blocking = check_node_blocking(arrow_before, arrow_after, name)
            if blocking:
                logging.info("found blocking node, can skip path")
                return True
    return False
