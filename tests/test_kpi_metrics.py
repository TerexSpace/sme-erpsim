from sme_erpsim.kpi.metrics import compute_lead_times, compute_activity_durations, compute_throughput
import pandas as pd


def test_metrics_compute():
    log = pd.DataFrame(
        [
            {"time": 0.0, "type": "order_arrival", "order_id": "O0"},
            {"time": 1.0, "type": "order_complete", "order_id": "O0"},
            {"time": 2.0, "type": "order_arrival", "order_id": "O1"},
            {"time": 4.0, "type": "order_complete", "order_id": "O1"},
            {"time": 0.5, "type": "end_activity", "order_id": "O0", "activity": "a", "duration": 0.5},
        ]
    )
    leads = compute_lead_times(log)
    assert leads == [1.0, 2.0]
    durations = compute_activity_durations(log)
    assert durations["a"] == 0.5
    throughput = compute_throughput(log, horizon=4.0)
    assert throughput == 0.5
