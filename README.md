# GraphRAG-CellTypeAnnotation

A comprehensive framework for cell type annotation using Graph-enhanced Retrieval Augmented Generation (GraphRAG) and large language models. This project combines knowledge graphs, Neo4j databases, and state-of-the-art LLMs to perform accurate cell type annotation based on marker genes.

## Features

- **Multiple LLM Support**: Integration with DeepSeek, Llama3, and other large language models
- **Graph-Enhanced RAG**: Utilizes Neo4j knowledge graphs for enhanced retrieval
- **Multiple Annotation Methods**: Supports baseline LLM, RAG, and Knowledge Graph-enhanced RAG approaches
- **Comprehensive Evaluation**: Built-in metrics for evaluating annotation accuracy
- **Flexible Pipeline**: Configurable pipeline for different species, datasets, and tissues
- **Benchmark Dataset Support**: Works with GTEx and other genomics datasets

## Architecture

The system employs three main annotation strategies:

1. **Baseline LLM**: Direct cell type annotation using large language models
2. **RAG (Retrieval Augmented Generation)**: Enhanced with external knowledge retrieval (Conduct a network search)
3. **KG-Graph-RAG**: Knowledge graph-enhanced retrieval for improved accuracy. **Leveraging the existing Neo4j knowledge graph, we employ the open-source Neo4j GraphRAG toolkit to query the graph in response to a user’s question. After identifying the relevant marker-gene nodes, we traverse their relationships to retrieve the associated cell nodes and their connecting edges (papers). We then tally the cell nodes, extract the ten most frequent cell types along with their occurrence counts, and package this information—together with the supporting papers—as a prompt for the LLM, thereby enhancing its reasoning performance.**

## Installation

### Prerequisites

- Python 3.8+
- Neo4j Database
- Access to supported LLM APIs (DeepSeek, Ollama)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/lixinyu66666/GraphRAG-CellTypeAnnotation.git
cd GraphRAG-CellTypeAnnotation
```

2. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate markeragent
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```env
# DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Ollama Configuration
OLLAMA_API_KEY=your_ollama_api_key
OLLAMA_BASE_URL=http://localhost:11434/v1

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password

# Tavily Search API
TAVILY_API_KEY=your_tavily_api_key
```

4. Set up Neo4j database:
- Install and start Neo4j
- Configure connection parameters in your `.env` file

## Usage

### Basic Usage

Run the main pipeline with default settings:

```python
from pipeline import run_pipeline

# Basic LLM annotation
run_pipeline(
    file_path="datasets/dataset_init.csv",
    method="llama3:70b",
    species="human",
    dataset="GTEx",
    default_rag_k=3,
    weight=0.8,
    init_result_path="results/results.csv",
    save_path="results/results.csv"
)

# Knowledge Graph-enhanced annotation
run_pipeline(
    file_path="datasets/dataset_init.csv",
    method="llama3:70b-kg-graph-rag",
    species="human",
    dataset="GTEx",
    default_rag_k=3,
    weight=0.8,
    init_result_path="results/results.csv",
    save_path="results/results.csv"
)
```

### Available Methods

The framework supports multiple annotation methods:

- `deepseek-r1`: DeepSeek R1 baseline
- `deepseek-v3`: DeepSeek V3 baseline
- `deepseek-r1-rag`: DeepSeek R1 with RAG
- `deepseek-v3-rag`: DeepSeek V3 with RAG
- `deepseek-r1-kg-graph-rag`: DeepSeek R1 with Knowledge Graph RAG
- `deepseek-v3-kg-graph-rag`: DeepSeek V3 with Knowledge Graph RAG
- `llama3:70b`: Llama3 70B baseline
- `llama3:70b-kg-graph-rag`: Llama3 70B with Knowledge Graph RAG

### Custom Configuration

You can customize the annotation process by modifying the parameters:

```python
run_pipeline(
    file_path="path/to/your/dataset.csv",
    method="deepseek-v3-kg-graph-rag",
    species="mouse",  # or "human"
    dataset="your_dataset_name",
    tissue="specific_tissue",  # optional
    default_rag_k=5,  # number of retrieved documents
    weight=0.7,  # confidence weight
    init_result_path="path/to/initial/results.csv",
    save_path="path/to/save/results.csv"
)
```

## Dataset Format

Input datasets should be in CSV format with the following columns:

- `dataset`: Dataset name (e.g., "GTEx")
- `tissue`: Tissue type (or "NA" if not specified)
- `marker`: Marker genes (comma-separated)
- Additional metadata columns as needed

Example:
```csv
dataset,tissue,marker
GTEx,Bone Marrow,"CD34,CD38,CD45"
GTEx,Brain,"GFAP,S100B,ALDH1L1"
```

## Evaluation Metrics

The framework includes comprehensive evaluation metrics:

- **BLEU Score**: Measures similarity between predicted and ground truth annotations
- **Exact Match**: Binary accuracy for perfect matches
- **Normalized Matching**: Handles variations in cell type terminology
- **Broad Type Classification**: Groups cell types into broader categories

## Project Structure

```
GraphRAG-CellTypeAnnotation/
├── main.py                 # Main execution script
├── pipeline.py             # Core pipeline implementation
├── config.py              # Configuration and method definitions
├── method.py              # Annotation method implementations
├── metric.py              # Evaluation metrics
├── load_data.py           # Data loading utilities
├── logger.py              # Logging configuration
├── neo4j_tools.py         # Neo4j database utilities
├── datasets/              # Input datasets
├── results/               # Output results
└── logs/                  # Log files
```

## Configuration

The system is highly configurable through the `config.py` file. You can:

- Add new annotation methods
- Modify model parameters
- Adjust retrieval settings
- Configure evaluation metrics

## Logging

The framework provides comprehensive logging for debugging and monitoring:

- Execution logs are saved in the `logs/` directory
- Different log levels for various components
- Timestamped log entries for tracking progress

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Additionnal Information

1. The dataset employed in this project is sourced from the Supplementary Tables of the paper titled [**“Assessing GPT-4 for Cell Type Annotation in Single-Cell RNA-seq Analysis.”**](https://www.nature.com/articles/s41592-024-02235-4#Sec14)
2. The evaluation metric adopted in this project is inspired by the paper [**“Single-Cell Omics Arena: A Benchmark Study for Large Language Models on Cell Type Annotation Using Single-Cell Data.”**](https://arxiv.org/abs/2412.02915) That study employs the BLEU score, which does capture annotation accuracy, but it is coarse-grained and cannot faithfully reflect the underlying biological relationships between predictions and labels. Because no reliable automated tool yet exists to map annotation results to the correct biological concepts—and thereby capture those relationships—using BLEU in this project is a pragmatic compromise. We hope future work will overcome this limitation.


## Results

### BLEU Score Performance Comparison

The following table shows the BLEU-avg-final scores for different models and methods across various datasets and tissues:

<!--
<style>
  .triple-line { border-collapse: collapse; }
  .triple-line thead tr:first-child th { border-top: 2px solid #fff; }
  .triple-line thead tr:nth-child(2) th,
  .triple-line thead tr:first-child th[rowspan] {
      border-bottom: 2px solid #fff;
  }
  .triple-line tbody tr:last-child td { border-bottom: 2px solid #fff; }
  .triple-line th, .triple-line td { padding: 6px 10px; text-align: center; }
</style>
-->

<table class="triple-line" style="font-size:0.8em;">
  <thead>
    <tr>
      <th rowspan="2" style="text-align:left;">Method</th>
      <th colspan="1">Azimuth</th>
      <th colspan="7">GTEx</th>
      <th colspan="1">literature</th>
      <th colspan="3">TS</th>
      <th colspan="5">mammal</th>
      <th rowspan="2">Average</th>
    </tr>
    <tr>
      <th>PBMC</th>
      <th>Breast</th>
      <th>Esophagus</th>
      <th>Heart</th>
      <th>Lung</th>
      <th>Prostate</th>
      <th>Skeletal muscle</th>
      <th>Skin</th>
      <th>Breast</th>
      <th>Eye</th>    
      <th>Liver</th>    
      <th>Thymus</th>
      <th>Kidney</th>
      <th>Heart</th>
      <th>Liver</th>
      <th>Spleen</th>
      <th>Duodenum</th>    
    </tr>
  </thead>
  <tbody>
    <tr><td style="text-align:left;">DeepSeek-R1</td>             <td>55.704</td><td><strong>43.550</strong></td><td><strong>47.798</strong></td><td>63.742</td><td><strong>60.575</strong></td><td>54.828</td><td>60.852</td><td>63.338</td><td>77.044</td><td><strong>48.557</strong></td><td><strong>66.275</strong></td><td><strong>61.189</strong></td><td><strong>75.662</strong></td><td><strong>71.629</strong></td><td><strong>74.950</strong></td><td><strong>73.113</strong></td><td><strong>57.923</strong></td><td><strong>60.116</strong></td></tr>
    <tr><td style="text-align:left;">DeepSeek-R1-RAG</td>         <td><strong>72.383</strong></td><td>32.376</td><td>37.178</td><td><strong>72.278</strong></td><td>52.234</td><td>46.073</td><td><strong>62.911</strong></td><td><strong>64.592</strong></td><td><strong>79.051</strong></td><td>47.853</td><td>44.501</td><td>56.299</td><td>69.466</td><td>66.394</td><td>68.327</td><td>53.456</td><td>57.828</td><td>58.670</td></tr>
    <tr style="border-bottom:2px solid #fff;"><td style="text-align:left;">DeepSeek-R1-KG-Graph-RAG</td><td>60.453</td><td>42.773</td><td>39.884</td><td>52.517</td><td>55.125</td><td><strong>56.05</strong></td><td>55.200</td><td>62.629</td><td>76.009</td><td>38.788</td><td>58.464</td><td>41.803</td><td>66.757</td><td>66.464</td><td>67.389</td><td>55.832</td><td><strong>57.923</strong></td><td>54.440</td></tr>
    <tr><td style="text-align:left;">DeepSeek-V3</td>             <td>56.248</td><td>39.220</td><td>41.527</td><td>66.148</td><td><strong>61.613</strong></td><td>44.699</td><td>50.825</td><td>46.156</td><td>80.038</td><td><strong>61.524</strong></td><td>51.526</td><td><strong>60.144</strong></td><td>71.334</td><td><strong>72.282</strong></td><td><strong>73.045</strong></td><td><strong>83.390</strong></td><td>53.953</td><td><strong>57.635</strong></td></tr>
    <tr><td style="text-align:left;">DeepSeek-V3-RAG</td>         <td><strong>77.031</strong></td><td>38.508</td><td><strong>44.429</strong></td><td>56.458</td><td>50.575</td><td>35.433</td><td>49.516</td><td>47.932</td><td><strong>82.575</strong></td><td>40.880</td><td><strong>57.977</strong></td><td>52.024</td><td>70.536</td><td>68.569</td><td>72.956</td><td>65.508</td><td><strong>62.603</strong></td><td>56.370</td></tr>
    <tr style="border-bottom:2px solid #fff;"><td style="text-align:left;">DeepSeek-V3-KG-Graph-RAG</td><td>55.839</td><td><strong>50.541</strong></td><td>39.644</td><td><strong>66.832</strong></td><td>59.07</td><td><strong>57.203</strong></td><td><strong>51.590</strong></td><td><strong>60.968</strong></td><td>56.010</td><td>40.765</td><td>41.382</td><td>42.477</td><td><strong>74.341</strong></td><td>71.718</td><td>70.134</td><td>72.683</td><td>53.953</td><td>55.839</td></tr>
    <tr><td style="text-align:left;">Llama-3 70B</td>             <td>38.176</td><td>33.655</td><td>35.384</td><td>54.201</td><td>46.629</td><td><strong>40.189</strong></td><td>31.299</td><td>42.772</td><td>54.587</td><td><strong>35.923</strong></td><td><strong>45.141</strong></td><td>38.849</td><td><strong>58.580</strong></td><td><strong>55.171</strong></td><td><strong>53.293</strong></td><td>50.947</td><td><strong>51.378</strong></td><td>40.271</td></tr>
    <tr><td style="text-align:left;">Llama-3 70B-KG-Graph-RAG</td><td><strong>46.285</strong></td><td><strong>38.630</strong></td><td><strong>37.417</strong></td><td><strong>68.417</strong></td><td><strong>49.073</strong></td><td>38.376</td><td><strong>40.139</strong></td><td><strong>55.118</strong></td><td><strong>72.210</strong></td><td>34.000</td><td>43.850</td><td><strong>47.979</strong></td><td>57.410</td><td>54.902</td><td>51.698</td><td><strong>62.453</strong></td><td><strong>51.378</strong></td><td><strong>46.501</strong></td></tr>
  </tbody>
</table>

*Note: Values represent BLEU-avg-final scores. Higher scores indicate better performance.*

For both DeepSeek-R1 and DeepSeek-V3, adding standard RAG or knowledge-graph-based GraphRAG yields little benefit—and can even reduce performance. The likely explanation is that these 671-billion-parameter models are already exceptionally strong at cell-type annotation; the remaining gap from the gold standard lies mainly in slight differences of phrasing. Supplying extra RAG context therefore does not help them excel further and may instead dilute their native strengths by lengthening the input. Moreover, the current evaluation metric is too coarse-grained to detect such subtle performance differences.


By contrast, knowledge-graph-based GraphRAG delivers a clear boost for **smaller-parameter models**. For instance, with the 70-billion-parameter LLaMA-3—whose baseline performance in cell-type annotation is still sub-optimal—GraphRAG substantially improves prediction accuracy across nearly every dataset and tissue we tested, **the BLEU score improved by 15.47%**. The only notable exception is a few tissues in the mammal dataset; there, the dataset provides too few markers to retrieve sufficient information from the knowledge graph, rendering GraphRAG ineffective. Although we have not yet run experiments with other lightweight models such as Qwen or Gemini, we can reasonably expect **GraphRAG to yield similarly significant gains for them as well**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this work in your research, please cite:

```bibtex
@software{graphrag_celltypeannotation,
  title={GraphRAG-CellTypeAnnotation: Graph-Enhanced Cell Type Annotation with Large Language Models},
  author={Li, Xinyu},
  year={2025},
  url={https://github.com/lixinyu66666/GraphRAG-CellTypeAnnotation}
}
```

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/lixinyu66666/GraphRAG-CellTypeAnnotation/issues) page
2. Create a new issue with detailed information about your problem
3. Provide relevant logs and configuration details

## Related Projects

- [Neo4j GraphRAG](https://github.com/neo4j/neo4j-graphrag-python)
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [DeepSeek API](https://platform.deepseek.com/)

---

**Note**: This project is actively under development. Features and APIs may change in future versions.
