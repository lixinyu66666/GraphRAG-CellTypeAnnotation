from pipeline import run_pipeline

if __name__ == "__main__":

    run_pipeline(
        file_path="datasets/dataset_init.csv",
        method="deepseek-r1-rag",
        species="human",
        dataset="Azimuth",
        tissue="PBMC",
        default_rag_k=3,
        weight=0.8,
        init_result_path="results/results.csv",
        save_path="results/results_temp.csv"
    )