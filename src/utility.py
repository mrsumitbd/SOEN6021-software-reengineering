import pandas as pd
import os
from os import listdir
from os.path import isfile, join
from scipy import stats


def write_df(df, file_name, overwrite_if_existing=True):
    data_file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'output', file_name))

    if overwrite_if_existing:
        df.to_csv(data_file_path, index=False, header=True)
    else:
        existing_df = pd.read_csv(data_file_path)
        existing_df['Run'] = existing_df['Run'].astype(float)
        last_existing_run = max(existing_df['Run'].tolist())
        df['Run'] = [last_existing_run + float(run) for run in df['Run'].tolist()]
        df = pd.concat([existing_df, df], ignore_index=True)
        df.to_csv(data_file_path, index=False, header=True)


def list_files(folder_path, all=True, extension=None):
    if all:
        return [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    else:
        if extension is None:
            raise ValueError("Extension cannot be None if only a fixed type of files are to be listed.")
        else:
            return [f for f in listdir(folder_path) if (isfile(join(folder_path, f)) and f.endswith(f".{extension}"))]


def calculate_pct_diff(v1, v2):
    return ((v2 - v1) / abs(v1)) * 100


def extract_p_value(trt, ctrl):
    p_value = stats.ttest_ind(trt, ctrl).pvalue
    return p_value #float(str(stats.ttest_ind(trt, ctrl)).split('pvalue=')[1].split(')')[0])
