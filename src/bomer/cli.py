import argparse
from pathlib import Path
from typing import Optional, List

from bomer.core.config import load_config
from bomer.core.loader import load_bom, load_suppliers
from bomer.core.schema import normalize_bom_columns, validate_bom
from bomer.engines.cost import analyze_costs
from bomer.engines.optimizer import optimize_bom
from bomer.engines.risk import analyze_risk
from bomer.reporting.report_writer import (
    write_normalized_bom,
    write_optimized_bom,
    write_analysis_json,
    write_issues_json,
    write_summary_text,
)
from bomer.core.exceptions import BomerError  # ⬅️ new


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bomer",
        description="Bomer – deterministic BoM analysis and optimization engine",
    )
    parser.add_argument(
        "command",
        choices=["analyze"],
        help="Command to run. Currently only 'analyze' is implemented.",
    )
    parser.add_argument(
        "--bom",
        required=True,
        help="Path to BOM CSV file.",
    )
    parser.add_argument(
        "--suppliers",
        help="Path to suppliers JSON file. If omitted, taken from config.",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to write reports and artifacts (default: ./output).",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to bomer YAML config file (default: ./bomer.yaml if exists).",
    )
    return parser


def _run_analyze(
    bom_path: Path,
    suppliers_path: Path,
    output_dir: Path,
    config_path: Optional[Path] = None,
) -> None:
    """
    Core 'analyze' pipeline.

    Raises BomerError (or subclasses) for domain-level problems so that
    main() can handle them cleanly.
    """
    config = load_config(str(config_path) if config_path is not None else None)

    output_dir.mkdir(parents=True, exist_ok=True)

    # 1) Load BOM
    bom_df = load_bom(bom_path)

    # 2) Normalize columns
    normalized_bom = normalize_bom_columns(bom_df)

    # 3) Validate
    issues = validate_bom(normalized_bom)

    # 4) Load suppliers
    suppliers_data = load_suppliers(suppliers_path)

    # 5) Optimize BOM (dedupe, etc.)
    optimized_bom = optimize_bom(normalized_bom)

    # 6) Cost & Risk
    cost_summary = analyze_costs(optimized_bom, suppliers_data)
    risk_summary = analyze_risk(optimized_bom, suppliers_data, config=config)

    # 7) Write artifacts
    write_normalized_bom(normalized_bom, output_dir / "normalized_bom.csv")
    write_optimized_bom(optimized_bom, output_dir / "optimized_bom.csv")
    write_analysis_json(
        optimized_bom,
        cost_summary,
        risk_summary,
        bom_path,
        suppliers_path,
        output_dir / "analysis.json",
    )
    write_issues_json(issues, output_dir / "issues.json")
    write_summary_text(
        optimized_bom,
        cost_summary,
        risk_summary,
        issues,
        output_dir / "summary.txt",
    )


def main(argv: Optional[List[str]] = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command != "analyze":
        parser.error("Only 'analyze' command is supported in v0.1.")

    bom_path = Path(args.bom)
    config_path = Path(args.config) if args.config else None

    # suppliers path may come from CLI or config
    config = load_config(str(config_path) if config_path is not None else None)
    suppliers_path = (
        Path(args.suppliers)
        if args.suppliers
        else Path(config.get("suppliers", {}).get("path", "data/suppliers.json"))
    )

    output_dir = Path(args.output_dir)

    try:
        _run_analyze(
            bom_path=bom_path,
            suppliers_path=suppliers_path,
            output_dir=output_dir,
            config_path=config_path,
        )
        print(f"[BOMER] Analysis complete. Artifacts written to: {output_dir}")
    except BomerError as e:
        # Known, domain-level error
        print(f"[BOMER] Error: {e}")
        raise SystemExit(1)
    except KeyboardInterrupt:
        print("\n[BOMER] Aborted by user.")
        raise SystemExit(130)
    except Exception as e:
        # Unexpected bug – keep it visible but mark as unexpected
        print(f"[BOMER] Unexpected error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
