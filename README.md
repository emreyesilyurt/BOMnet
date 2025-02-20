# BOMnet: Intelligent BOM Optimization

## Overview
BOMnet is an AI-powered **Bill of Materials (BOM) optimizer** that leverages **Large Language Models (LLMs)** to suggest cost-effective and supply chain-compliant electronic components. It helps businesses reduce costs, improve compliance, and optimize procurement decisions.

## Features
✅ Optimizes BOM using **AI-driven component selection**  
✅ Evaluates **cost-effectiveness** based on supplier pricing  
✅ Checks **supply chain compliance** for components  
✅ Generates structured **reports** for BOM analysis  
✅ Uses **modular architecture** for flexibility and scalability  

---
## File Structure
```
BOMnet/
│── src/
│   ├── __init__.py                 # Package initialization
│   ├── config.py                   # Configuration settings
│   ├── main.py                     # Entry point for the optimizer
│   ├── data_loader.py              # Loads BOM and supplier data
│   ├── llm_optimizer.py            # Uses LLM to optimize the BOM
│   ├── cost_analysis.py            # Evaluates cost-effectiveness
│   ├── compliance_checker.py       # Ensures supply chain compliance
│   ├── report_generator.py         # Generates reports for users
│── data/
│   ├── sample_bom.csv              # Example BOM dataset
│   ├── suppliers.json              # Example supplier info
│── tests/
│   ├── test_data_loader.py         # Unit tests for data loader
│   ├── test_llm_optimizer.py       # Unit tests for LLM optimizer
│   ├── test_cost_analysis.py       # Unit tests for cost analysis
│── notebooks/
│   ├── exploratory_analysis.ipynb  # Jupyter notebook for analysis
│── models/
│   ├── saved_model.pkl             # Pretrained optimization model
│── requirements.txt                 # Dependencies
│── README.md                        # Documentation
│── .gitignore                        # Ignore unnecessary files
│── Dockerfile                        # Containerization setup
│── Makefile                          # Automation commands
│── config.yaml                        # Configuration settings
```

---
## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/BOMnet.git
cd BOMnet
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set OpenAI API Key
Export your OpenAI API key to enable the LLM optimizer:
```bash
export OPEN_AI_KEY="your-api-key-here"
```

---
## Usage
Run the optimizer using:
```bash
python src/main.py
```
This will:
1. Load the BOM and supplier data
2. Optimize the BOM using LLM
3. Evaluate cost-effectiveness
4. Check compliance
5. Generate a summary report

---
## Example Output
```
Optimized BOM:
{Updated BOM list}
Total Cost: $1200.50
Compliance Status: Compliant ✅
```

---
## Contributing
Feel free to fork this repository, create a new branch, and submit a pull request for any improvements or feature additions.

---
## License
This project is licensed under the MIT License.

