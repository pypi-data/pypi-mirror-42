import os
import pandas as pd
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from ..map import df_map


def add_1_to_col2(row: pd.DataFrame):
    row['col2'] += 1
    return row


def test_df_map(monkeypatch):
    df = pd.DataFrame.from_dict({'col1': ['row1', 'row2'], 'col2': [1, 2]})
    try:
        monkeypatch.setattr(os, 'sched_getaffinity', lambda _: range(2))
    except AttributeError:
        monkeypatch.setattr(multiprocessing, 'cpu_count', lambda: 2)
    df = df_map(add_1_to_col2, df)
    row = df[df['col1'] == 'row1']
    assert row.iloc[0]['col2'] == 2
    row = df[df['col1'] == 'row2']
    assert row.iloc[0]['col2'] == 3


def test_df_map_unix(monkeypatch):
    def raise_attribute_error(nr: int):
        raise AttributeError()

    df = pd.DataFrame.from_dict({'col1': ['row1', 'row2'], 'col2': [1, 2]})
    try:
        monkeypatch.setattr(os, 'sched_getaffinity', raise_attribute_error)
    except AttributeError:
        monkeypatch.setattr(multiprocessing, 'cpu_count', lambda: 2)
    df = df_map(add_1_to_col2, df)
    row = df[df['col1'] == 'row1']
    assert row.iloc[0]['col2'] == 2
    row = df[df['col1'] == 'row2']
    assert row.iloc[0]['col2'] == 3


def test_df_map_correct_no_of_cores(monkeypatch):
    df = pd.DataFrame.from_dict({'col1': ['row1', 'row2'], 'col2': [1, 2]})
    try:
        monkeypatch.setattr(os, 'sched_getaffinity', lambda _: range(100))
    except AttributeError:
        monkeypatch.setattr(multiprocessing, 'cpu_count', lambda: 100)

    def ex_map(_self, _func, list_df):
        assert len(list_df) == 2
        return list_df
    monkeypatch.setattr(ProcessPoolExecutor, 'map', ex_map)
    df_map(add_1_to_col2, df)

    list_for_df = [(i, i) for i in range(150)]
    df = pd.DataFrame.from_records(list_for_df)

    def ex_map(_self, _func, list_df):
        assert len(list_df) == 99
        return list_df
    monkeypatch.setattr(ProcessPoolExecutor, 'map', ex_map)
    df_map(add_1_to_col2, df)


def test_df_map_param_no_of_cores(monkeypatch):
    list_for_df = [(i, i) for i in range(150)]
    df = pd.DataFrame.from_records(list_for_df)

    def ex_map(_self, _func, list_df):
        assert len(list_df) == 100
        return list_df
    monkeypatch.setattr(ProcessPoolExecutor, 'map', ex_map)
    df = df_map(add_1_to_col2, df, 100)
    assert df.shape[0] == 150
    assert df.shape[1] == 2
    assert df[0].nunique() == 150


def test_df_map_correct_no_of_cores_perc(monkeypatch):
    df = pd.DataFrame.from_dict({'col1': ['row1', 'row2'], 'col2': [1, 2]})
    try:
        monkeypatch.setattr(os, 'sched_getaffinity', lambda _: range(100))
    except AttributeError:
        monkeypatch.setattr(multiprocessing, 'cpu_count', lambda: 100)

    def ex_map(_self, _func, list_df):
        assert len(list_df) == 2
        return list_df
    monkeypatch.setattr(ProcessPoolExecutor, 'map', ex_map)
    df_map(add_1_to_col2, df, no_of_cores_perc=0.41)

    list_for_df = [(i, i) for i in range(150)]
    df = pd.DataFrame.from_records(list_for_df)

    def ex_map(_self, _func, list_df):
        assert len(list_df) == 42
        return list_df
    monkeypatch.setattr(ProcessPoolExecutor, 'map', ex_map)
    df_map(add_1_to_col2, df, no_of_cores_perc=0.415)
