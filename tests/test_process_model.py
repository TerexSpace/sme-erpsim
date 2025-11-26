import numpy as np

from sme_erpsim.process.model import Activity, ProcessModel


def test_process_model_routing():
    rng = np.random.default_rng(1)
    pm = ProcessModel("simple")
    a = Activity("a", duration=lambda r: 1.0)
    b = Activity("b", duration=lambda r: 1.0)
    pm.add_activity(a, is_start=True)
    pm.add_activity(b)
    pm.add_transition("a", "b")
    next_act = pm.choose_next("a", rng)
    assert next_act is not None
    assert next_act.name == "b"
    assert pm.start_activity == "a"
