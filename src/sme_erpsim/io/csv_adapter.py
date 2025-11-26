"""CSV adapters to load ERP-like data."""
from __future__ import annotations

from typing import List
import pandas as pd

from .erp_structures import SalesOrder, PurchaseOrder, InventoryTransaction


def load_sales_orders(path: str) -> List[SalesOrder]:
    df = pd.read_csv(path, parse_dates=["created_at", "promised_date"])
    return [
        SalesOrder(
            order_id=row["order_id"],
            customer=row["customer"],
            created_at=row["created_at"],
            promised_date=row.get("promised_date"),
            quantity=int(row["quantity"]),
        )
        for _, row in df.iterrows()
    ]


def load_purchase_orders(path: str) -> List[PurchaseOrder]:
    df = pd.read_csv(path, parse_dates=["created_at", "expected_date"])
    return [
        PurchaseOrder(
            po_id=row["po_id"],
            supplier=row["supplier"],
            created_at=row["created_at"],
            expected_date=row.get("expected_date"),
            quantity=int(row["quantity"]),
        )
        for _, row in df.iterrows()
    ]


def load_inventory_transactions(path: str) -> List[InventoryTransaction]:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return [
        InventoryTransaction(
            transaction_id=row["transaction_id"],
            item=row["item"],
            quantity=int(row["quantity"]),
            timestamp=row["timestamp"],
            movement_type=row["movement_type"],
        )
        for _, row in df.iterrows()
    ]


__all__ = ["load_sales_orders", "load_purchase_orders", "load_inventory_transactions"]
