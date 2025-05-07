import metric
import pipeline
import load_data
import pandas as pd

if __name__ == "__main__":

    df_results = pd.read_csv("GraphRAG-CellTypeAnnotaion/results/results.csv")

    df_Azimuth_PBMC = load_data.load_benchmark_specified_dataset_tissue(
        filepath="GraphRAG-CellTypeAnnotaion/datasets/dataset_init.csv",
        dataset="Azimuth",
        tissue="PBMC"
    )

    df_results = pipeline.deepseek_annotation(
        df_file=df_Azimuth_PBMC,
        species="human",
        df_full=df_results,
        model_name="deepseek-reasoner"
    )

    df_results.to_csv("GraphRAG-CellTypeAnnotaion/results/results_1.csv", index=False)

    df_results = pipeline.get_bleu_scores(
        df=df_Azimuth_PBMC,
        method="DeepSeek-R1",
        df_full=df_results
    )

    df_results.to_csv("GraphRAG-CellTypeAnnotaion/results/results_2.csv", index=False)