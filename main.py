import pipeline
import load_data
import pandas as pd

if __name__ == "__main__":

    df_results = pd.read_csv("results/results_init.csv")
    # df_results = pd.read_csv("results/results_1.csv")

    df_Azimuth_PBMC = load_data.load_benchmark_specified_dataset_tissue(
        filepath="datasets/dataset_init.csv",
        dataset="Azimuth",
        tissue="PBMC"
    )

    df_results = pipeline.deepseek_annotation(
        df_file=df_Azimuth_PBMC,
        species="human",
        df_full=df_results,
        model_name="deepseek-reasoner"
    )

    df_results.to_csv("results/results_1.csv", index=False)

    df_Azimuth_PBMC_results = load_data.load_benchmark_specified_dataset_tissue(
        filepath="results/results_1.csv",
        dataset="Azimuth",
        tissue="PBMC"
    )

    df_results = pipeline.get_bleu_scores(
        df=df_Azimuth_PBMC_results,
        method="DeepSeek-R1",
        df_full=df_results
    )

    df_results.to_csv("results/results_2.csv", index=False)