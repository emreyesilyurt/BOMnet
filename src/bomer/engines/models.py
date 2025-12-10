from dataclasses import dataclass
from typing import List


@dataclass
class CostLineItem:
    PartNumber: str
    Quantity: float
    UnitPrice: float
    LineCost: float


@dataclass
class CostSummary:
    currency: str
    total_cost: float
    line_items: List[CostLineItem]
    missing_prices: List[str]


@dataclass
class RiskLine:
    PartNumber: str
    supplier_count: int
    single_source: bool
    missing_price: bool
    obsolete: bool


@dataclass
class RiskSummary:
    risk_score: float
    single_source_ratio: float
    missing_price_ratio: float
    obsolete_ratio: float
    lines: List[RiskLine]
