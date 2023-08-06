def readcsv_poc(fileadress,poc=True,samplesize=0.01,**csv_prm):
    """This is my a csv file reading function. It included POC and reduce memory
    usageself.

    Parameters
    ----------
    fileadress : str
        The path and name of the CSV file.
    poc : type
        Indicater of wether this importing is prove of concept.
    samplesize : type
        Indicate how much of the protion of imprting data sampled.
    **csv_prm : type
        Other parameters for Pandas read_csv function.

    Returns
    -------
    type
        The function returns a Pandas DataFrame.

    Example
    -------
    csv_prm = {
        "parse_dates":['purchase_date']
        }
    m=readcsv_poc('input/new_merchant_transactions.csv', **csv_prm)
    m.head()


    """
    import pandas as pd
    import random
    if poc is True:
        n = sum(1 for line in open(fileadress)) - 1
        # number of records in file (excludes header)
        s = samplesize
        # desired sample size
        skip = sorted(random.sample(range(1,n+1), int(n*(1-s))))
        # the 0-indexed header will not be included in the skip list
        df = pd.read_csv(fileadress, **csv_prm, skiprows=skip)
        print('Read {} out of {} rows of the dataset.'.format(int(s*n),n))
    else:
        df = pd.read_csv(fileadress, **csv_prm)
    reduce_mem_usage(df)
    return df


def reduce_mem_usage(df, verbose=True):
    import numpy as np
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage().sum() / 1024**2
    if verbose: print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df
