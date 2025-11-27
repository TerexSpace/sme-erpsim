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
SME-ERPSim is a Python package for discrete-event simulation of ERP processes typical in small and medium enterprises. It models order-to-cash, procure-to-pay, and light make-to-stock flows with validated configurations, ERP-friendly data structures, and KPIs such as lead time, fill rate, and resource utilization.

# Statement of need
SMEs often rely on spreadsheets or ERP modules that lack scenario analysis and stochastic modeling. Existing simulation tools are either costly or generic. SME-ERPSim offers a lightweight, open-source engine that ingests ERP exports, captures domain semantics (orders, workers, machines), and reports performance metrics needed for operational decisions.

# State of the field
Classic simulation texts describe discrete-event principles [@law; @banks; @shannon]. Several Python libraries offer general-purpose simulation, but few provide ERP-focused abstractions or validated configs tailored to SMEs. SME-ERPSim fills this gap with domain-specific events and ready-to-use adapters.

# Software description
SME-ERPSim builds on SimPy for event scheduling [@simpy], Pydantic for configuration validation [@pydantic], and pandas for tabular outputs [@mckinney2010pandas]. Process models combine activities and transitions, with routing policies and resources (workers, machines, calendars). Demand processes support Poisson, deterministic, and empirical arrivals. KPI modules compute lead time, throughput, and activity duration summaries, and reporting yields Markdown or data frames. Visualization utilities provide Gantt charts and process graphs.

## Design and implementation
- **Configuration and validation:** YAML/JSON configs are validated against explicit schemas (Pydantic v2) for reproducibility and error checking.
- **Simulation kernel:** A thin abstraction over SimPy hides event scheduling while exposing ERP-specific events (order arrival, start/end activity, completion).
- **Domain resources:** Worker pools, work centers, and calendars model capacity constraints; routing policies support FIFO, LIFO, and priority.
- **Data integration:** CSV adapters load sales/purchase orders and inventory movements to calibrate demand and service times.
- **Metrics and reporting:** KPI utilities compute lead time, throughput, and activity durations; reports can be exported to Markdown or data frames for downstream analysis.

## Quality control
Automated tests (pytest) cover process routing, simulation runs, KPI calculations, and CSV ingestion. A GitHub Actions workflow runs the test suite on pushes and pull requests to enforce reproducibility. Example configurations and a notebook outline serve as executable documentation for reviewers.

# Illustrative example
A make-to-stock scenario defines activities (receive, pick/pack, ship), worker pools, and a Poisson arrival process. Running an 8-hour simulation generates event traces; the KPI report shows average lead time and throughput. Example YAML configs and a notebook outline are provided for reproduction.

# Availability and reuse
The source code is released under the OSI-approved MIT license and installable via `pip install .`. The public repository includes automated tests (`pytest`), a continuous-integration workflow, and examples under `examples/`. Users can extend activity definitions, integrate ERP CSV exports, and design experiments via provided helpers.

# Acknowledgements
We thank the open-source SimPy and Pydantic communities for foundational tools.

# References
