def generate_report(bom_data, cost_summary, compliance_status, output_path):
    """Generates a report."""
    with open(output_path, "w") as f:
        f.write("BOM Report\n")
        f.write(str(cost_summary))
        f.write(str(compliance_status))
