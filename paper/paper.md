---
title: 'SME-ERPSim: A discrete-event simulation engine for SME ERP processes'
tags:
  - Python
  - ERP
  - discrete-event simulation
  - operations research
  - SMEs
authors:
  - name: Your Name
    affiliation: 1
affiliations:
  - name: Your Institution
    index: 1
date: 2024-01-01
bibliography: reference.lib
---

# Summary
SME-ERPSim is a Python package for discrete-event simulation of ERP processes typical in small and medium enterprises. It models order-to-cash, procure-to-pay, and light make-to-stock flows with validated configurations, ERP-friendly data structures, and KPIs such as lead time, fill rate, and resource utilization.

# Statement of need
SMEs often rely on spreadsheets or ERP modules that lack scenario analysis and stochastic modeling. Existing simulation tools are either costly or generic. SME-ERPSim offers a lightweight, open-source engine that ingests ERP exports, captures domain semantics (orders, workers, machines), and reports performance metrics needed for operational decisions.

# State of the field
Classic simulation texts describe discrete-event principles [@law; @banks; @shannon]. Several Python libraries offer general-purpose simulation, but few provide ERP-focused abstractions or validated configs tailored to SMEs. SME-ERPSim fills this gap with domain-specific events and ready-to-use adapters.

# Software description
The package builds on SimPy for event scheduling and Pydantic for configuration validation. Process models combine activities and transitions, with routing policies and resources (workers, machines, calendars). Demand processes support Poisson, deterministic, and empirical arrivals. KPI modules compute lead time, throughput, and activity duration summaries, and reporting yields Markdown or data frames. Visualization utilities provide Gantt charts and process graphs.

# Illustrative example
A make-to-stock scenario defines activities (receive, pick/pack, ship), worker pools, and a Poisson arrival process. Running an 8-hour simulation generates event traces; the KPI report shows average lead time and throughput. Example YAML configs and a notebook outline are provided for reproduction.

# Availability and reuse
The source code is packaged for `pip install .`, with tests using `pytest` and examples under `examples/`. Users can extend activity definitions, integrate ERP CSV exports, and design experiments via provided helpers.

# Acknowledgements
We thank the open-source SimPy and Pydantic communities for foundational tools.

# References
