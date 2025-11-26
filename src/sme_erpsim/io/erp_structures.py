"""Canonical ERP structures."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SalesOrder:
    order_id: str
    customer: str
    created_at: datetime
    promised_date: Optional[datetime]
    quantity: int


@dataclass
class PurchaseOrder:
    po_id: str
    supplier: str
    created_at: datetime
    expected_date: Optional[datetime]
    quantity: int


@dataclass
class InventoryTransaction:
    transaction_id: str
    item: str
    quantity: int
    timestamp: datetime
    movement_type: str
