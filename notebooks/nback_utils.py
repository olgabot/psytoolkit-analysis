
import pandas as pd

columns = [
    # column 1
    'run', 
    
    # column 2
    'trsummarize_nbackl', 
    
    # column 3
    'condition', 
    
    # column 4
    'correct', 
    
    # column 5
    'key_press',
    
    # column 6
    'false_alarm',

    # column 7
    'col7',
    
    # column 8
    'milliseconds',

    'col9', 'col10', 'col11', 'col12',
]

col_order = [
    # "date",
    "2bk0_mean_ms",
    "2bk0_median_ms",
    "2bk0_min_ms",
    "2bk0_max_ms",
    "2bk0_pct_error",
    "2bk1_mean_ms",
    "2bk1_median_ms",
    "2bk1_min_ms",
    "2bk1_max_ms",
    "2bk1_pct_error",
]


def read_nback_results(filename, names=columns):
    return pd.read_csv(filename, sep='\s', header=None, names=names)

def rename_index(series, prefix, suffix):
    return prefix + series.index.astype(str) + suffix


def summarize_nback(nback_results, prefix="2bk"):
    error_rates = (
        1
        - nback_results.groupby("condition").correct.sum()
        / nback_results.condition.value_counts()
    )
    error_rates.index = rename_index(error_rates, prefix, "_pct_error")

    correct = nback_results.query("correct == 1")
    mean_ms = correct.groupby(["condition"]).milliseconds.mean()
    mean_ms.index = rename_index(mean_ms, prefix, "_mean_ms")

    median_ms = correct.groupby(["condition"]).milliseconds.median()
    median_ms.index = rename_index(median_ms, prefix, "_median_ms")

    min_ms = correct.groupby(["condition"]).milliseconds.min()
    min_ms.index = rename_index(min_ms, prefix, "_min_ms")

    max_ms = correct.groupby(["condition"]).milliseconds.max()
    max_ms.index = rename_index(max_ms, prefix, "_max_ms")

    summary = pd.concat([mean_ms, median_ms, min_ms, max_ms, error_rates])
    
    # Reorder columns for easy copying into notion
    summary = summary[col_order]
    return summary
