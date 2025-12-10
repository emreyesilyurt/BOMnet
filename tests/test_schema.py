import pandas as pd

from bomer.core.schema import normalize_bom_columns, validate_bom


def test_normalize_bom_columns_aliases():
    df = pd.DataFrame(
        {
            "mpn": ["RES-10K-1%", "CAP-100NF"],
            "qty": [10, 20],
        }
    )

    norm = normalize_bom_columns(df)

    assert "PartNumber" in norm.columns
    assert "Quantity" in norm.columns
    assert list(norm["PartNumber"]) == ["RES-10K-1%", "CAP-100NF"]
    assert list(norm["Quantity"]) == [10, 20]


def test_validate_bom_detects_missing_quantity():
    df = pd.DataFrame(
        {
            "PartNumber": ["RES-10K-1%", "CAP-100NF"],
            "Quantity": [10, None],
        }
    )

    issues = validate_bom(df)
    assert any(issue["field"] == "Quantity" for issue in issues)
