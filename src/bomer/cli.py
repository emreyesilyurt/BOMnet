import argparse
from pathlib import Path
from typing import Optional

from bomer import __version__
from bomer.api import run_analysis
from bomer.core.exceptions import BomerError
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
        help=(
            "Path to suppliers JSON file. "
            "If omitted, taken from config (suppliers.path in bomer.yaml) "
            "or defaults to data/suppliers.json."
        ),
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

    _add_analyze_subparser(subparsers)

    return parser


def _run_analyze(args: argparse.Namespace) -> None:
    bom_path = Path(args.bom)
    suppliers_path = Path(args.suppliers) if args.suppliers else None
    config_path = Path(args.config) if args.config else None

    result = run_analysis(
        bom_path=bom_path,
        suppliers_path=suppliers_path,
        config_path=config_path,
    )

    normalized_bom = result["normalized_bom"]
    optimized_bom = result["optimized_bom"]
    issues = result["issues"]
    cost_summary = result["cost_summary"]
    risk_summary = result["risk_summary"]
    bom_path = result["bom_path"]
    suppliers_path = result["suppliers_path"]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

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


def main(argv: Optional[list] = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "analyze":
        try:
            _run_analyze(args)
        except BomerError as e:
            print(f"[BOMER] Error: {e}")
            raise SystemExit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
