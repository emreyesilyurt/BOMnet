import pandas as pd


def optimize_bom(bom: pd.DataFrame) -> pd.DataFrame:
    """
    Very first version of optimizer.

    - Requires PartNumber and Quantity columns.
    - Aggregates rows by PartNumber, summing quantities.
    - Sorts by PartNumber.
    - Adds 'Optimized' boolean column (True for all).

    This is where LLM/ensemble logic will plug in later.
    """
    if "PartNumber" not in bom.columns or "Quantity" not in bom.columns:
        raise ValueError("BOM must contain PartNumber and Quantity columns.")

    aggregated = (
        bom.groupby("PartNumber", as_index=False)["Quantity"]
        .sum()
        .sort_values("PartNumber")
        .reset_index(drop=True)
    )

    aggregated["Optimized"] = True
    return aggregated
