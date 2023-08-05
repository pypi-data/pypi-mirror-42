from .. import config
import hashlib
import pandas as pd
import feather
import dill
from glob import glob
import os
import numpy as np


def clear_storage():
    from .caching import cache
    cache.memory.clear()
    np.random.seed(int(__import__("time").time()))
    a, b = np.random.randint(5, 30, size=2)
    c = int(input(f"{a} + {b} = "))
    if a + b != c:
        print("You aren't smart enough to take such decisions")
        return
    for path in glob(config.storage_path + '*_*') + glob(config.source_path + '*'):
        print(f"deleting {path}")
        os.remove(path)


def get_hash_df(df):
    idx_hash = hashlib.sha256(train.index.values).hexdigest()

    sorted_cols = train.columns.sort_values().values
    col_hash = hashlib.sha256(sorted_cols).hexdigest()

    hash_first, hash_last = pd.util.hash_pandas_object(df.iloc[[0, -1]][sorted_cols]).values

    return hashlib.sha256(np.array([idx_hash, col_hash, hash_first, hash_last])).hexdigest()

    # return hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values).hexdigest()


def get_hash_slice(idxs):
    if isinstance(idxs, slice):
        idxs = (-1337, idxs.start, idxs.stop, idxs.step)
    return hex(hash(frozenset(idxs)))[2:]


def get_df_volume(df):
    return df.memory_usage(index=True).sum()


def get_path_df(name):
    return config.storage_path + name + '_df'


def save_df(df, path):
    """
    Saves a dataframe as feather binary file. Adds to df and additional column filled
    with index values and having a special name.
    """
    # print('saving df', path)
    # try:
    #     print('enc', df.encoders)
    # except:
    #     print('enc: no attr')
    not_trivial_index = type(df.index) != pd.RangeIndex
    if not_trivial_index:
        index_name = f'{config.index_prefix}{df.index.name}'
        df[index_name] = df.index.values
        df.reset_index(drop=True, inplace=True)
    feather.write_dataframe(df, path)
    if not_trivial_index:
        df.set_index(index_name, inplace=True)
        df.index.name = df.index.name[len(config.index_prefix):]


def load_df(path):
    """
    Loads a dataframe from feather format and sets as index that additional
    column added with saving by save_df. Restores original name of index column.
    """
    # print('loading df', path)
    tmp = feather.read_dataframe(path, use_threads=True)
    index_col = tmp.columns[tmp.columns.str.contains(config.index_prefix)]
    # print(index_col)
    if any(index_col):
        tmp.set_index(index_col.values[0], inplace=True)
        tmp.index.name = tmp.index.name[len(config.index_prefix):]
    return tmp


def get_path_obj(name):
    return config.storage_path + name + '_obj'


def save_obj(obj, path):
    """
    Saves object
    """
    dill.dump(obj, open(path, 'wb'))


def load_obj(path):
    """
    Loads object
    """
    return dill.load(open(path, 'rb'))


def get_path_info(name):
    return config.info_path + name + '_info'
