import argparse
from pathlib import Path
from typing import Optional

from bomer import __version__
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


def _add_analyze_subparser(subparsers: argparse._SubParsersAction) -> None:
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a BOM: normalize, optimize, compute cost and risk, and write reports.",
    )

    analyze_parser.add_argument(
        "--bom",
        required=True,
        help="Path to BOM CSV file.",
    )
    analyze_parser.add_argument(
        "--suppliers",
        help="Path to suppliers JSON file. "
             "If omitted, taken from config (suppliers.path in bomer.yaml).",
    )
    analyze_parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to write reports and artifacts (default: ./output).",
    )
    analyze_parser.add_argument(
        "--config",
        help="Path to bomer YAML config file (default: ./bomer.yaml if present).",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bomer",
        description="Bomer – deterministic BoM analysis and optimization engine.",
    )

    # Global flags
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show Bomer version and exit.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="subcommands",
        metavar="<command>",
        help="Available commands",
    )

    # v0.1.x: only 'analyze' is implemented, but structure is ready for more.
    _add_analyze_subparser(subparsers)

    return parser


def _run_analyze(args: argparse.Namespace) -> None:
    # 1) Load config
    config = load_config(args.config)

    # 2) Paths
    bom_path = Path(args.bom)
    suppliers_path = (
        Path(args.suppliers)
        if args.suppliers
        else Path(config.get("suppliers", {}).get("path", "data/suppliers.json"))
    )
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 3) Load BOM
    bom_df = load_bom(bom_path)

    # 4) Normalize columns
    normalized_bom = normalize_bom_columns(bom_df)

    # 5) Validate
    issues = validate_bom(normalized_bom)

    # 6) Load suppliers
    suppliers_data = load_suppliers(suppliers_path)

    # 7) Optimize BOM
    optimized_bom = optimize_bom(normalized_bom)

    # 8) Cost & Risk
    cost_summary = analyze_costs(optimized_bom, suppliers_data)
    risk_summary = analyze_risk(optimized_bom, suppliers_data, config=config)

    # 9) Write artifacts
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

    print(f"[BOMER] Analysis complete. Artifacts written to: {output_dir}")


def main(argv: Optional[list[str]] = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "analyze":
        _run_analyze(args)
    else:
        # If no subcommand provided, show help
        parser.print_help()


if __name__ == "__main__":
    main()
