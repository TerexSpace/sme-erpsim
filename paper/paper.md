---
title: 'SME-ERPSim: A discrete-event simulation engine for SME ERP processes'
tags:
  - Python
  - ERP
  - discrete-event simulation
  - operations research
  - SMEs
authors:
  - name: Almas Ospanov
    orcid: 0009-0004-3834-130X
    affiliation: 1
affiliations:
  - name: Astana IT University
    index: 1
date: 2025-11-27
bibliography: reference.lib
repository: https://github.com/TerexSpace/sme-erpsim
---

# Summary

SME-ERPSim is a Python package for discrete-event simulation of enterprise resource planning (ERP) workflows typical in small and medium enterprises (SMEs). It models order-to-cash, procure-to-pay, and make-to-stock/assemble-to-order processes with validated configurations, ERP-native data structures (sales orders, purchase orders, inventory transactions), and key performance indicators (KPIs) such as lead time, throughput, and resource utilization. The package bridges the gap between high-cost commercial simulation suites and lightweight spreadsheet-based planning tools, enabling SMEs to perform "what-if" analysis and capacity planning without specialized training or expensive licenses.

# Statement of need

SMEs typically operate with limited information technology (IT) resources and budgets. While larger enterprises can afford commercial simulation tools (Arena, Simul8, ANYLOGIC) or custom development, SMEs often rely on spreadsheet-based planning or built-in ERP capabilities, which lack stochastic modeling and scenario analysis features.

The research question addressed by SME-ERPSim is: **How can we provide SMEs with a lightweight, open-source, data-driven simulation tool that directly ingests ERP transaction exports and delivers actionable operational insights?**

Key pain points include:

- **Limited simulation expertise:** SMEs lack operations research teams; simulation tools must expose simple, domain-familiar abstractions.
- **Cost barriers:** Commercial suites cost tens of thousands of dollars annually; open-source alternatives reduce total cost of ownership.
- **ERP integration:** Simulation must ingest real order, inventory, and resource data from existing ERP systems (SAP, NetSuite, Odoo, Tally) without complex middleware.
- **Tactical decision support:** SMEs need fast answers to questions like "Can we serve 50% more demand?" or "What if we add one more warehouse worker?" without months of custom development.

SME-ERPSim directly addresses these needs by providing a well-tested, validated, configurable simulation engine with minimal dependencies and a focus on process modeling, resource constraints, and KPI reporting.

# State of the field

Discrete-event simulation (DES) is a mature field with established principles [@law; @banks; @shannon]. Several Python packages provide general-purpose simulation frameworks:

- **SimPy** [@simpy] is a lightweight DES library widely used in research and industry.
- **Salabim** is a discrete-event simulation library with graphical output.
- **AnyLogic** offers Python API bindings but requires expensive commercial licensing.

However, existing tools are either:
1. **Too generic:** General-purpose simulators lack ERP domain semantics (orders, fulfillment, resource management).
2. **Too expensive:** Commercial suites require significant capital and annual maintenance costs.
3. **Poorly integrated:** Few packages directly consume ERP export formats (CSV, JSON) or provide ready-made order/inventory abstractions.

SME-ERPSim fills this gap by combining lightweight event simulation (SimPy), domain-specific process modeling, and ERP-ready data structures, creating a tool tailored to SME operational decision support.

# Software description

SME-ERPSim is built on the following core pillars:

## Architecture and key components

**Process modeling** (graph-based): Activities and transitions model business workflows. Transitions carry routing probabilities to enable stochastic branching. The process engine uses NetworkX [@networkx] for graph representation, enabling future extensions like cycle detection or bottleneck identification.

**Simulation kernel** (SimPy-based): A thin abstraction over SimPy [@simpy] exposes domain-specific events (OrderArrival, StartActivity, EndActivity, OrderCompletion) while hiding low-level event scheduling complexity. This design allows users to reason about order flow rather than event loops.

**Resource management**: Workers (pools of interchangeable labor), machines (with setup times and capacity), and calendars (shift-based working hours) are modeled explicitly. This enables capacity constraint analysis and bottleneck identification.

**Demand generation**: Three configurable arrival process families support stochastic (Poisson), deterministic, and empirical order arrivals. Users can calibrate parameters from historical ERP transaction logs using built-in parameter estimation utilities.

**Data validation** (Pydantic v2): All configuration—processes, resources, demand, simulation parameters—is validated against explicit schemas. This design catches configuration errors early and ensures reproducibility via deterministic random seeds.

**KPI and reporting**: Built-in utilities compute lead time, throughput, activity duration histograms, and resource utilization. Reports export to Markdown (for documentation), DataFrames (for downstream analysis), or dictionaries (for programmatic access).

**ERP integration**: CSV adapters consume standard order, purchase order, and inventory transaction exports from common ERP systems. Domain classes (SalesOrder, PurchaseOrder, InventoryTransaction) encode business semantics for calibration.

## Technical highlights

- **Reproducibility:** Deterministic random seeds enable exact replication of runs for validation and peer review.
- **Error handling:** Pydantic validation prevents silent failures from invalid configurations.
- **Extensibility:** Users can subclass Activity, OrderArrivalProcess, and RoutingPolicy to add custom behavior without modifying core code.
- **Documentation:** Inline docstrings follow Google style; YAML examples cover common workflows; a Jupyter notebook template demonstrates end-to-end usage.

# Illustrative example

Consider a small trading company simulating a make-to-stock order fulfillment process:

**Process:** Receive order → Check inventory → Pick/pack items → Ship.

**Resources:** One planning clerk, two warehouse workers, a single truck.

**Demand:** Historical data shows 3 orders/hour on average (Poisson).

Using SME-ERPSim, the operations team configures the process in YAML, loads 12 months of historical orders via CSV, estimates Poisson parameters, runs a 10-hour "next week" simulation with 3 different staffing levels, and generates a KPI report showing lead time distributions and worker utilization. Decision: hire one additional warehouse worker to reduce average lead time from 8 hours to 5 hours.

Example configuration and output are provided in `examples/make_to_stock.yaml` and `examples/small_trading_company.ipynb`.

# Availability and reuse

**Source code** is released under the OSI-approved MIT License [@opensource] and is cloneable, browsable, and installable via PyPI (planned) or GitHub (`pip install git+https://github.com/TerexSpace/sme-erpsim`).

**Testing:** A comprehensive test suite (pytest) covers process routing, simulation execution, KPI calculations, and CSV data ingestion. Continuous integration (GitHub Actions) runs tests on every push to enforce code quality.

**Documentation:**

- README with quick-start guide
- JOSS paper (this document) and academic references
- Inline docstrings in all public APIs
- Example YAML configurations for common workflows
- Jupyter notebook template for tutorial purposes
- CONTRIBUTING.md for community contributions

**Extensibility:** The modular design allows researchers and practitioners to:

- Define custom activity types and routing policies
- Integrate proprietary ERP systems via new CSV adapters
- Extend KPI calculations for domain-specific metrics
- Contribute improvements to the public repository

# Acknowledgements

We thank the developers and communities behind SimPy, Pydantic, pandas, and NetworkX for foundational libraries that made this work possible. We acknowledge Astana IT University for institutional support and the open-source software community for emphasis on reproducibility and transparency.

# References
