import pandas as pd
from pathlib import Path

from sme_erpsim.io.csv_adapter import load_sales_orders


def test_load_sales_orders(tmp_path: Path):
    data = pd.DataFrame(
        [
            {"order_id": "O1", "customer": "ACME", "created_at": "2024-01-01", "promised_date": "2024-01-05", "quantity": 10}
        ]
    )
    csv_path = tmp_path / "sales.csv"
    data.to_csv(csv_path, index=False)
    orders = load_sales_orders(str(csv_path))
    assert len(orders) == 1
    assert orders[0].order_id == "O1"
