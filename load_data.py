import pandas as pd

def load_benchmark_specified_dataset_tissue(filepath: str, dataset: str, tissue: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df = df[(df["dataset"] == dataset) & (df["tissue"] == tissue)].reset_index(drop=True)
    return df

def load_benchmark_specified_dataset(filepath: str, dataset: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df = df[df["dataset"] == dataset].reset_index(drop=True)
    return df

def load_benchmark(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df