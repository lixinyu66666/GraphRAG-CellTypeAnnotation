from method import annotate_cell_type_with_deepseek
import metric
import pandas as pd

def deepseek_annotation(df_file, species, df_full, model_name="deepseek-reasoner") -> pd.DataFrame:

    if model_name == "deepseek-reasoner":
        new_col = "DeepSeek-R1 annotation"
    else:
        new_col = "DeepSeek-V3 annotation"

    key_cols = ["dataset", "tissue", "marker"]

    if new_col not in df_full.columns:
        df_full[new_col] = pd.NA
    
    for _, row in df_file.iterrows():
        markers = [row["marker"]]
        tissue = row["tissue"]
        is_tissue = (tissue != "NA")

        _, response = annotate_cell_type_with_deepseek(
            marker_genes=markers,
            species=species,
            is_tissue=is_tissue,
            tissue=tissue if is_tissue else None,
            model_name=model_name
        )

        pred = response.choices[0].message.content.strip()

        mask = True
        for kc in key_cols:
            mask &= (df_full[kc].astype(str) == str(row[kc]))
        df_full.loc[mask, new_col] = pred
        print(f"Predicted cell type for {row['dataset']} {row['tissue']} {row['marker']}: {pred}")
    
    data = df_full.pop(new_col)
    df_full[new_col] = data

    return df_full

def get_bleu_scores(df: pd.DataFrame, method: str, df_full: pd.DataFrame) -> pd.DataFrame:

    bleu1_col = f"{method} BLEU-1"
    bleu2_col = f"{method} BLEU-2"
    bleu_avg_col = f"{method} BLEU-avg"

    if bleu1_col not in df_full.columns:
        df_full[bleu1_col] = pd.NA
    if bleu2_col not in df_full.columns:
        df_full[bleu2_col] = pd.NA
    if bleu_avg_col not in df_full.columns:
        df_full[bleu_avg_col] = pd.NA
    
    for _, row in df.iterrows():
        ref_manual_annotation = row["manual annotation"]
        ref_manual_clname = row["manual CLname"]
        refs = [ref_manual_annotation, ref_manual_clname]

        pred = row[f"{method} annotation"]
        if pd.isna(pred):
            continue

        bleu_score = metric.evalute_bleu_score(refs, pred)
        mask = (df_full["dataset"] == row["dataset"]) & (df_full["tissue"] == row["tissue"]) & (df_full["marker"] == row["marker"])
        df_full.loc[mask, bleu1_col] = bleu_score["BLEU-1"]
        df_full.loc[mask, bleu2_col] = bleu_score["BLEU-2"]
        df_full.loc[mask, bleu_avg_col] = bleu_score["BLEU-avg"]

        return df_full


        


