# Bomer

**Bomer** is a small, deterministic Bill of Materials (BoM) analysis and optimization engine.

It is designed for electronics and component teams who need repeatable, automation-friendly analysis on real BoMs – not just one-off LLM chat sessions.

Bomer is currently in an early CLI-focused phase (`v0.1.x`) and lives inside this repository (originally named **BOMnet**).

---

## Features

Current capabilities (v0.1):

- **CLI-first workflow**  
  `bomer analyze` takes a BoM CSV and supplier JSON and produces structured outputs.

- **Canonical BoM normalization**  
  Maps common column variations (e.g. `mpn`, `Mfr Part #`) into canonical fields like `PartNumber`, `Manufacturer`, `Description`, `Quantity`.

- **Deterministic optimization**  
  Aggregates duplicate parts, sums quantities, and produces a clean `optimized_bom.csv`.

- **Cost analysis**  
  Joins the BoM with supplier pricing data and computes:
  - per-line `UnitPrice` and `LineCost`
  - `total_cost`
  - list of parts with missing prices

- **Basic risk scoring**  
  Simple risk model based on:
  - single-sourced parts
  - missing prices
  - lifecycle status (e.g. `Obsolete` / `EOL`)

- **Structured outputs**  
  Generates machine- and human-readable artifacts:
  - `normalized_bom.csv`
  - `optimized_bom.csv`
  - `analysis.json`
  - `issues.json`
  - `summary.txt`

LLM-assisted normalization and alternative component suggestions are planned for later versions.

---

## Installation

Bomer is a Python package located inside this repo.

Prerequisites:

- Python **3.9+**
- `pip` available
- Optional: a virtual environment (recommended)

```bash
git clone https://github.com/emreyesilyurt/BOMnet.git
cd BOMnet

# Optional: create a virtualenv
python3 -m venv .venv
source .venv/bin/activate  # on macOS / Linux
# .venv\Scripts\activate   # on Windows

# Install in editable (dev) mode
pip install -e .
```

If installation succeeds, you should have a `bomer` CLI on your PATH:

```bash
which bomer     # or: where bomer on Windows
```

---

## Quick Start

### 1. Project layout (relevant parts)

```text
.
├── bomer.yaml             # Optional configuration (cost/risk weights, supplier path)
├── data/
│   ├── sample_bom.csv     # Example BoM
│   └── suppliers.json     # Example supplier price data
├── src/
│   └── bomer/
│       ├── cli.py         # CLI entrypoint: `bomer analyze`
│       ├── core/          # Config, loading, schema/validation
│       ├── engines/       # Cost, risk, optimization
│       └── reporting/     # Writers for CSV/JSON/text outputs
└── output/                # Created when you run analyses (ignored by git)
```

### 2. Basic usage

```bash
bomer analyze   --bom data/sample_bom.csv   --suppliers data/suppliers.json   --output-dir output
```

Arguments:

- `--bom`: path to a BoM CSV  
- `--suppliers`: path to suppliers JSON  
- `--output-dir`: directory for generated artifacts (default: `./output`)

---

## Inputs

### BoM CSV

Expected columns:

- `PartNumber` / `MPN` / `Mfr Part #`
- `Quantity` / `Qty`

Optional:

- `Manufacturer`
- `Description`
- `LifecycleStatus`
- `RoHS`

---

## Outputs

Generated artifacts:

- `normalized_bom.csv`
- `optimized_bom.csv`
- `analysis.json`
- `issues.json`
- `summary.txt`

---

## Configuration (`bomer.yaml`)

```yaml
suppliers:
  path: data/suppliers.json

cost:
  currency: USD
  default_volume: 1000

risk:
  single_source_weight: 0.4
  missing_price_weight: 0.3
  lifecycle_weight: 0.3
```

---

## Contributing

1. Clone repo  
2. Create virtual env  
3. Install with `pip install -e .`  
4. Run tests with `pytest`  

Guidelines:

- Keep functions modular and testable  
- Deterministic engines should stay deterministic  
- Update documentation when adding new commands or outputs  

---


