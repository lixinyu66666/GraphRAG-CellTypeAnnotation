import re
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import inflect

# nltk.download('punkt')

# try:
#     find('tokenizers/punkt_tab')
# except LookupError:
#     nltk.download('punkt', quiet=True)
    
p = inflect.engine()

def clean_and_normalize(pred):
    """
    Clean and normalize the predicted text.
    """
    if not isinstance(pred, str) or not pred.strip():

        return ""
    
    match = re.match(r"^[^\n,\.]*", pred.strip())
    if match:
        pred_clean = match.group().strip().lower()

        return p.singular_noun(pred_clean) or pred_clean
    
    return pred.strip().lower()

def compute_bleu_scores(reference_list, prediction, weights):
    """
    Compute BLEU scores for the given reference list and prediction.
    Args:
        reference_list (list): List of reference strings.
        prediction (str): The predicted string.
        weights (tuple): Weights for BLEU score calculation.
    """

    prediction = nltk.word_tokenize(prediction)
    references = [nltk.word_tokenize(ref) for ref in reference_list]
    smoothie = SmoothingFunction().method4

    return sentence_bleu(references, prediction, weights=weights, smoothing_function=smoothie)

def evaluate_bleu_score(reference_synonyms, prediction):
    """
    Evaluate the BLEU score for the given reference synonyms and prediction.
    Args:
        reference_synonyms (list): List of reference synonyms.
        prediction (str): The predicted string.
    """

    prediction = clean_and_normalize(prediction)

    refs = [clean_and_normalize(ref) for ref in reference_synonyms]
    bleu1 = compute_bleu_scores(refs, prediction, (1, 0))
    bleu2 = compute_bleu_scores(refs, prediction, (0.5, 0.5))
    bleu_avg = (bleu1 + bleu2) / 2

    return {
        "BLEU-1": round(bleu1 * 100, 2),
        "BLEU-2": round(bleu2 * 100, 2),
        "BLEU-avg": round(bleu_avg * 100, 2)
    }