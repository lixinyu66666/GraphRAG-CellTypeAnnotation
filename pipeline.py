from method import annotate_cell_type_with_deepseek
import metric
import pandas as pd
from logger import logger

def deepseek_annotation(df_file, species, df_full, model_name="deepseek-reasoner") -> pd.DataFrame:

    if model_name == "deepseek-reasoner":
        annotation_col = "DeepSeek-R1 annotation"
        broadtype_col = "DeepSeek-R1 broadtype"
    else:
        annotation_col = "DeepSeek-V3 annotation"
        broadtype_col = "DeepSeek-V3 broadtype"

    key_cols = ["dataset", "tissue", "marker"]

    if annotation_col not in df_full.columns:
        df_full[annotation_col] = pd.NA
    if broadtype_col not in df_full.columns:
        df_full[broadtype_col] = pd.NA
    
    for _, row in df_file.iterrows():
        markers = [row["marker"]]
        tissue = row["tissue"]
        is_tissue = (tissue != "NA")

        logger.info(f"Annotating: dataset={row['dataset']}, tissue={row['tissue']}, marker={row['marker']}")

        try:
            _, response = annotate_cell_type_with_deepseek(
                marker_genes=markers,
                species=species,
                is_tissue=is_tissue,
                tissue=tissue if is_tissue else None,
                model_name=model_name
            )
            pred = response.choices[0].message.content.strip()

            parts = [p.strip() for p in pred.split(",", 1)]
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
        df_full.loc[mask, annotation_col] = annotation
        df_full.loc[mask, broadtype_col] = broadtype
    
    data_annot = df_full.pop(annotation_col)
    data_broad = df_full.pop(broadtype_col)
    df_full[annotation_col] = data_annot
    df_full[broadtype_col] = data_broad

    return df_full

def get_bleu_scores(df: pd.DataFrame, method: str, df_full: pd.DataFrame, weight=0.8) -> pd.DataFrame:

    bleu1_col = f"{method} BLEU-1"
    bleu2_col = f"{method} BLEU-2"
    bleu_avg_col = f"{method} BLEU-avg"
    bleu_broadtype_avg_col = f"{method} broadtype BLEU-avg"
    bleu_final_col = f"{method} BLEU-avg-final"

    if bleu1_col not in df_full.columns:
        df_full[bleu1_col] = pd.NA
    if bleu2_col not in df_full.columns:
        df_full[bleu2_col] = pd.NA
    if bleu_avg_col not in df_full.columns:
        df_full[bleu_avg_col] = pd.NA
    if bleu_broadtype_avg_col not in df_full.columns:
        df_full[bleu_broadtype_avg_col] = pd.NA
    if bleu_final_col not in df_full.columns:
        df_full[bleu_final_col] = pd.NA

    annotation_col = f"{method} annotation"
    broadtype_col = f"{method} broadtype"
    
    for _, row in df.iterrows():
        ref_anno = row["manual annotation"]
        ref_clname = row["manual CLname"]
        ref_broad = row.get("manual broadtype", None)

        refs_anno = [r for r in [ref_anno, ref_clname] if isinstance(r, str) and r.strip()]
        refs_broad = [ref_broad] if isinstance(ref_broad, str) and ref_broad.strip() else []


        pred_anno = row.get(annotation_col, None)
        pred_broad = row.get(broadtype_col, None)

        if pd.isna(pred_anno) or not refs_anno:
            continue

        logger.info(f"Evaluating BLEU scores for: dataset={row['dataset']}, tissue={row['tissue']}, marker={row['marker']}, pred={pred_anno}, broad={pred_broad}")

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
            logger.error(f"BLEU score calculation failed for {row['dataset']} {row['tissue']} {row['marker']}: {e}")
            continue

        logger.info(f"BLEU scores: annotation={score_anno['BLEU-avg']}, broadtype={score_broad['BLEU-avg']}, final_avg={bleu_avg_final}")  

        mask = (df_full["dataset"] == row["dataset"]) & (df_full["tissue"] == row["tissue"]) & (df_full["marker"] == row["marker"])
        df_full.loc[mask, bleu1_col] = score_anno["BLEU-1"]
        df_full.loc[mask, bleu2_col] = score_anno["BLEU-2"]
        df_full.loc[mask, bleu_avg_col] = score_anno["BLEU-avg"]
        df_full.loc[mask, bleu_broadtype_avg_col] = score_broad["BLEU-avg"]
        df_full.loc[mask, bleu_final_col] = bleu_avg_final

    return df_full


        


