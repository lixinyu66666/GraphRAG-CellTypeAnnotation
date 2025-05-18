from method import (
    annotate_cell_type_with_deepseek,
    annotation_cell_type_with_deepseek_rag,
    annotation_cell_type_with_deepseek_kg_graph_rag,
)

ANNOTATION_METHODS = {
    "deepseek-r1": {
        "func": annotate_cell_type_with_deepseek,
        "model_name": "deepseek-reasoner",
        "prefix": "DeepSeek-R1",
    },
    "deepseek-v3": {
        "func": annotate_cell_type_with_deepseek,
        "model_name": "deepseek-chat",
        "prefix": "DeepSeek-V3",
    },
    "deepseek-r1-rag": {
        "func": annotation_cell_type_with_deepseek_rag,
        "model_name": "deepseek-reasoner",
        "prefix": "DeepSeek-R1-RAG",
    },
    "deepseek-v3-rag": {
        "func": annotation_cell_type_with_deepseek_rag,
        "model_name": "deepseek-chat",
        "prefix": "DeepSeek-V3-RAG",
    },
    "deepseek-r1-kg-graph-rag": {
        "func": annotation_cell_type_with_deepseek_kg_graph_rag,
        "model_name": "deepseek-reasoner",
        "prefix": "DeepSeek-R1-KG-Graph-RAG",
    },
    "deepseek-v3-kg-graph-rag": {
        "func": annotation_cell_type_with_deepseek_kg_graph_rag,
        "model_name": "deepseek-chat",
        "prefix": "DeepSeek-V3-KG-Graph-RAG",
    },
}