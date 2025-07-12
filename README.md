# Streaming Pattern Matching Optimization

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

High-performance streaming pattern matching algorithms (Naive vs KMP) with comprehensive benchmarking and visualization. Applied to network flow anomaly detection for cybersecurity applications. It analyzes IP flow data to detect potential compromises by matching patterns in traffic sequences. The project includes performance benchmarks, visualizations, and data augmentation for large-scale testing.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Results and Visualizations](#results-and-visualizations)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview
This project demonstrates streaming pattern matching using Naive and KMP algorithms to process network flow data in real-time. It preprocesses IP flow logs into character sequences and compares algorithm performance on metrics like execution time, comparisons, and speedup ratios. Ideal for security applications like detecting botnet activity.

Key components:
- Streaming implementations in `functions.py`.
- Main execution in `main.py` and `main2.py`.
- Visualizations generated via `generate_all_visualizations.py`.

## Features
- **Streaming Pattern Matching**: Processes data character-by-character with Naive and KMP.
- **Performance Analysis**: Compares time, memory, and comparisons with visualizations (boxplots, line charts, heatmaps).
- **Data Augmentation**: Generates large datasets for scalability testing.
- **Network Anomaly Detection**: Applies algorithms to real IP flow data to spot compromise patterns.

## Dataset
### Context
Computer Network Traffic Data - A ~500K CSV with summary of some real network traffic data from the past. The dataset has ~21K rows and covers 10 local workstation IPs over a three month period. Half of these local IPs were compromised at some point during this period and became members of various botnets.

### Content
Each row consists of four columns:
- `date`: yyyy-mm-dd (from 2006-07-01 through 2006-09-30)
- `l_ipn`: local IP (coded as an integer from 0-9)
- `r_asn`: remote ASN (an integer which identifies the remote ISP)
- `f`: flows (count of connections for that day)

Reports of "odd" activity or suspicions about a machine's behavior triggered investigations on the following days (although the machine might have been compromised earlier):

Date : IP  
08-24 : 1  
09-04 : 5  
09-18 : 4  
09-26 : 3 6  

### Acknowledgements
This public dataset was found on http://statweb.stanford.edu/~sabatti/data.html

### Inspiration
Can you discover when a compromise has occurred by a change in the pattern of communication?

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/sahelmain/streaming-pattern-matching-optimization.git
   cd streaming-pattern-matching-optimization
   ```

2. Install dependencies (Python 3.8+):
   ```
   pip install -r requirements.txt
   ```

## Usage
### Run Pattern Matching Tests
- For real dataset tests: `python main.py`
- For custom patterns on augmented data: `python main2.py`

### Generate Visualizations
- Run `python generate_all_visualizations.py` to create charts in `visualizations/`.

### Generate Augmented Data
- Run `python generate_augmented_flows.py` to create large flow sequence files.

Example output: CSVs with results (e.g., `flow_pattern_matching_streaming_results.csv`) and PNG visualizations.

## Results and Visualizations
The project generates various charts comparing Naive vs. KMP:
- **Execution Time**: Bar and line charts showing scaling.
- **Comparisons**: Log-scale plots and heatmaps.
- **Speedup Ratios**: Violin plots and boxplots highlighting KMP's efficiency on long texts.

Sample:  
![Execution Time Comparison](visualizations/bar_chart_execution_time.png)

See `visualizations/` for all outputs.

## Contributing
Contributions welcome! Fork the repo and submit a pull request. For major changes, open an issue first.

## License
MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgements
- Dataset from Stanford University.
- Built for CS5381 course project.