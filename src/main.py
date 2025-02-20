import os
import json
import pandas as pd

from src.data_loader import load_bom_data
from src.llm_optimizer import optimize_bom
from src.cost_analysis import analyze_costs
from src.compliance_checker import check_compliance
from src.report_generator import generate_report

def main():
    """
    Main execution script for BOMnet - Optimized Bill of Materials processing.
    """
    # Load BOM data
    bom_file = "data/sample_bom.csv"
    suppliers_file = "data/suppliers.json"
    bom_data = load_bom_data(bom_file)
    
    if bom_data is None:
        print("Error: BOM data could not be loaded.")
        return
    
    # Load supplier data
    with open(suppliers_file, "r") as f:
        suppliers = json.load(f)
    
    # Optimize BOM using LLM-based analysis
    optimized_bom = optimize_bom(bom_data)
    
    # Perform cost analysis
    cost_summary = analyze_costs(optimized_bom, suppliers)
    
    # Check compliance
    compliance_status = check_compliance(optimized_bom)
    
    # Generate final report
    report_path = "output/bom_report.txt"
    generate_report(optimized_bom, cost_summary, compliance_status, report_path)
    
    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    main()
