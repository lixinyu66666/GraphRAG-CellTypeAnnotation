from pipeline import run_pipeline

if __name__ == "__main__":

    # run_pipeline(
    #     file_path="datasets/dataset_init.csv",
    #     method="deepseek-r1",
    #     species="human",
    #     dataset="GTEx",
    #     # tissue="Breast",
    #     default_rag_k=3,
    #     weight=0.8,
    #     init_result_path="results/results.csv",
    #     save_path="results/results.csv"
    # )

    # run_pipeline(
    #     file_path="datasets/dataset_init.csv",
    #     method="deepseek-v3",
    #     species="human",
    #     dataset="GTEx",
    #     # tissue="Breast",
    #     default_rag_k=3,
    #     weight=0.8,
    #     init_result_path="results/results.csv",
    #     save_path="results/results.csv"
    # )

    # run_pipeline(
    #     file_path="datasets/dataset_init.csv",
    #     method="deepseek-r1-rag",
    #     species="human",
    #     dataset="GTEx",
    #     # tissue="Breast",
    #     default_rag_k=3,
    #     weight=0.8,
    #     init_result_path="results/results.csv",
    #     save_path="results/results.csv"
    # )

    # run_pipeline(
    #     file_path="datasets/dataset_init.csv",
    #     method="deepseek-v3-rag",
    #     species="human",
    #     dataset="GTEx",
    #     # tissue="Breast",
    #     default_rag_k=3,
    #     weight=0.8,
    #     init_result_path="results/results.csv",
    #     save_path="results/results.csv"
    # )

    run_pipeline(
        file_path="datasets/dataset_init.csv",
        method="deepseek-r1-kg-graph-rag",
        species="human",
        dataset="literature",
        tissue="Breast",
        default_rag_k=3,
        weight=0.8,
        init_result_path="results/results_init.csv",
        save_path="results/results_test.csv"
    )

    # run_pipeline(
    #     file_path="datasets/dataset_init.csv",
    #     method="deepseek-v3-kg-graph-rag",
    #     species="human",
    #     dataset="GTEx",
    #     # tissue="Breast",
    #     default_rag_k=3,
    #     weight=0.8,
    #     init_result_path="results/results.csv",
    #     save_path="results/results.csv"
    # )