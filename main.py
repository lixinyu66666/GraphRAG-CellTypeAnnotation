from pipeline import run_pipeline

if __name__ == "__main__":

    run_pipeline(
        file_path="datasets/dataset_init.csv",
        method="llama3:70b-kg-graph-rag",
        species="human",
        dataset="TS",
        tissue="Eye",
        default_rag_k=3,
        weight=0.8,
        init_result_path="results/results.csv",
        save_path="results/results.csv"
    )   

    run_pipeline(
        file_path="datasets/dataset_init.csv",
        method="llama3:70b-kg-graph-rag",
        species="human",
        dataset="TS",
        tissue="Liver",
        default_rag_k=3,
        weight=0.8,
        init_result_path="results/results.csv",
        save_path="results/results.csv"
    )   

    run_pipeline(
        file_path="datasets/dataset_init.csv",
        method="llama3:70b-kg-graph-rag",
        species="human",
        dataset="TS",
        tissue="Thymus",
        default_rag_k=3,
        weight=0.8,
        init_result_path="results/results.csv",
        save_path="results/results.csv"
    )   