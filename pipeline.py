from config import ANNOTATION_METHODS
import metric
import pandas as pd
import inspect
import load_data
from logger import logger

def call_with_filtered_kwargs(func, **kwargs):
    """
    Call a function with filtered keyword arguments.
    Only include arguments that are present in the function's signature.
    """
    func_signature = inspect.signature(func)
    valid_keys = set(func_signature.parameters.keys())
    filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_keys}

    return func(**filtered_kwargs)


def cell_type_annotation(df_file, species, df_full, method, default_rag_k=3) -> pd.DataFrame:
    """
    General interface for cell type annotation methods.
    """

    if method not in ANNOTATION_METHODS:
        logger.error(f"Method {method} is not supported.")
        raise ValueError(f"Method {method} is not supported.")
    
    meta = ANNOTATION_METHODS[method]
    fn = meta["func"]
    model_name = meta["model_name"]
    prefix = meta["prefix"]
    k = meta.get("k", default_rag_k)

    ann_col = f"{prefix} annotation"
    broad_col = f"{prefix} broadtype"
    for col in [ann_col, broad_col]:
        if col not in df_full.columns:
            df_full[col] = pd.NA
    
    key_cols = ["dataset", "tissue", "marker"]

    for _, row in df_file.iterrows():
        markers = [row["marker"]]
        tissue = row["tissue"]
        is_tissue = (tissue != "NA")

        logger.info(f"Annotating: dataset={row['dataset']}, tissue={row['tissue']}, marker={row['marker']}")
        common_kwargs = dict(
            marker_genes=markers,
            species=species,
            is_tissue=is_tissue,
            tissue=tissue if is_tissue else None,
            model_name=model_name,
            k=k
        )

        try:
            _, response = call_with_filtered_kwargs(fn, **common_kwargs)
            pred = response.choices[0].message.content.strip()

            parts = [p.strip() for p in pred.split("|", 1)]
            annotation = parts[0] if len(parts) >= 1 else pd.NA
            broadtype = parts[1] if len(parts) == 2 else pd.NA

        except Exception as e:
            logger.error(f"Annotation failed for {row['dataset']} {row['tissue']} {row['marker']}: {e}")
            annotation = pd.NA
            broadtype = pd.NA

        logger.info(f"Predicted cell type: {annotation}, Broadtype: {broadtype}")

        mask = True
        for kc in key_cols:
            mask &= (df_full[kc].astype(str) == str(row[kc]))
        df_full.loc[mask, ann_col] = annotation
        df_full.loc[mask, broad_col] = broadtype

    return df_full

def get_bleu_scores(df: pd.DataFrame, method: str, df_full: pd.DataFrame, weight=0.8) -> pd.DataFrame:
    
    if method not in ANNOTATION_METHODS:
        logger.error(f"Method {method} is not supported.")
        raise ValueError(f"Method {method} is not supported.")
    
    meta = ANNOTATION_METHODS[method]
    prefix = meta["prefix"]

    cols_to_create = [
        "BLEU-1",
        "BLEU-2",
        "BLEU-avg",
        "broadtype BLEU-avg",
        "BLEU-avg-final",
    ]

    col_map = {c: f"{prefix} {c}" for c in cols_to_create}
    annotation_col = f"{prefix} annotation"
    broadtype_col = f"{prefix} broadtype"

    for name in list(col_map.values()) + [annotation_col, broadtype_col]:
        if name not in df_full.columns:
            df_full[name] = pd.NA
    
    for _, row in df.iterrows():
        refs_anno = [
            v for v in (row.get("manual annotation"), row.get("manual CLname"))
            if isinstance(v, str) and v.strip()
        ]
        ref_broad = row.get("manual broadtype", "")
        refs_broad = [ref_broad] if isinstance(ref_broad, str) and ref_broad.strip() else []

        pred_anno = row.get(annotation_col)
        pred_broad = row.get(broadtype_col)

        if pd.isna(pred_anno) or not refs_anno:
            continue

        logger.info(f"{prefix} Evaluating BLEU scores for: dataset={row['dataset']}, tissue={row['tissue']}, marker={row['marker']}, pred={pred_anno}, broad={pred_broad}")

        try:
            score_anno = metric.evalute_bleu_score(refs_anno, pred_anno)
            if refs_broad and isinstance(pred_broad, str):
                score_broad = metric.evalute_bleu_score(refs_broad, pred_broad)
            else:
                score_broad = {"BLEU-1": 0.0, "BLEU-2": 0.0, "BLEU-avg": 0.0}

            bleu_avg_final = round(
                weight * score_anno["BLEU-avg"] + (1 - weight) * score_broad["BLEU-avg"], 2
            )

        except Exception as e:
            logger.error(f"{prefix} BLEU score calculation failed for {row['dataset']} {row['tissue']} {row['marker']}: {e}")
            continue

        logger.info(f"{prefix} BLEU scores: annotation={score_anno['BLEU-avg']}, broadtype={score_broad['BLEU-avg']}, final_avg={bleu_avg_final}")  

        mask = (df_full["dataset"] == row["dataset"]) & (df_full["tissue"] == row["tissue"]) & (df_full["marker"] == row["marker"])

        df_full.loc[mask, col_map["BLEU-1"]] = score_anno["BLEU-1"]
        df_full.loc[mask, col_map["BLEU-2"]] = score_anno["BLEU-2"]
        df_full.loc[mask, col_map["BLEU-avg"]] = score_anno["BLEU-avg"]
        df_full.loc[mask, col_map["broadtype BLEU-avg"]] = score_broad["BLEU-avg"]
        df_full.loc[mask, col_map["BLEU-avg-final"]] = bleu_avg_final

    return df_full
        
def run_pipeline(
        file_path: str, 
        method: str, 
        species: str, 
        dataset: str = None,
        tissue: str = None,
        default_rag_k: int = 3,
        weight: float = 0.8,
        init_result_path: str = None,
        save_path: str = None
        ) -> pd.DataFrame:
    """
    Run the entire pipeline for cell type annotation and evaluation.
    Args:
        file_path (str): Path to the input dataset.
        method (str): Annotation method to use.
        species (str): Species for annotation.
        df_results (pd.DataFrame): DataFrame to store results.
        dataset (str, optional): Specific dataset to filter. Defaults to None.
        tissue (str, optional): Specific tissue to filter. Defaults to None.
        default_rag_k (int, optional): Default k value for RAG methods. Defaults to 3.
        weight (float, optional): Weight for BLEU score calculation. Defaults to 0.8.
    """

    # Load the dataframe need to be annotated
    if tissue and dataset:
        df_file = load_data.load_benchmark_specified_dataset_tissue(
            filepath=file_path,
            dataset=dataset,
            tissue=tissue
        )
    elif dataset:
        df_file = load_data.load_benchmark_specified_dataset(
            filepath=file_path,
            dataset=dataset
        )
    else:
        df_file = load_data.load_benchmark(filepath=file_path)
    
    # Load the initial results dataframe
    df_results = pd.read_csv(init_result_path)
    
    df_annotated = cell_type_annotation(
        df_file=df_file,
        species=species,
        df_full=df_results,
        method=method,
        default_rag_k=default_rag_k
    )

    # Save the annotated dataframe (temporary)
    df_annotated.to_csv(save_path, index=False)

    # Load the annotated dataframe to calculate BLEU scores
    if tissue and dataset:
        df_annotated_filter = load_data.load_benchmark_specified_dataset_tissue(
            filepath=save_path,
            dataset=dataset,
            tissue=tissue
        )
    elif dataset:
        df_annotated_filter = load_data.load_benchmark_specified_dataset(
            filepath=save_path,
            dataset=dataset
        )
    else:
        df_annotated_filter = load_data.load_benchmark(filepath=save_path)

    df_results = get_bleu_scores(
        df=df_annotated_filter,
        method=method,
        df_full=df_annotated,
        weight=weight
    )

    # Save the final results
    df_results.to_csv(save_path, index=False)


    

