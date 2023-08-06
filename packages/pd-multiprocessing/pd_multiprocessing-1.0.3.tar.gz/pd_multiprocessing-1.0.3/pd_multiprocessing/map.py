import os
import math
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
import logging
import pandas as pd


def df_map(func, df: pd.DataFrame, no_of_cores: int = None, no_of_cores_perc: float = None) -> pd.DataFrame:
    """
    Maps function func to DataFrame df using multithreading

    :param func: Function to be mapped to a single row. Has to take one parameter of type pandas.DataFrame
    :param df: Dataframe of type pandas.DataFrame
    :param no_of_cores: Number of cores to use. If it is None maximal number cores minus one will be used
    :param no_of_cores_perc: Number of cores to use in relation to all available cores. no_of_cores must be None.
    :type func: function, no lambda expression
    :type df: pandas.DataFrame
    :type no_of_cores: int
    :type no_of_cores_perc: float
    :return: transformed Dataframe of type pandas.DataFrame
    """
    logger = logging.getLogger('pd_multithreading.map')
    if no_of_cores is None:
        try:
            no_of_cores = len(os.sched_getaffinity(0))
        except AttributeError:
            no_of_cores = mp.cpu_count()
        if no_of_cores_perc is not None:
            no_of_cores = math.ceil(no_of_cores*no_of_cores_perc)
        elif no_of_cores > 1:
            no_of_cores -= 1
    len_df = len(df)
    if no_of_cores > len_df:
        no_of_cores = len_df
    logger.debug('Number of cores: %i', no_of_cores)

    list_df = []
    for i in range(no_of_cores):
        start = math.ceil(len_df*i/no_of_cores)
        end = math.ceil(len_df*(i+1)/no_of_cores) - 1
        df_block = df.iloc[start:end+1, :]
        list_df.append(df_block)
    with ProcessPoolExecutor() as ex:
        df_res_list = list(ex.map(func, list_df))
    res = None
    for df_res_element in df_res_list:
        if res is None:
            res = df_res_element
        else:
            res = res.append(df_res_element)
    return res
