### Middle Fork American River hydropower optimization model

Code for reservoir model portion of [Bryant et al. (2023)](https://www.mdpi.com/2071-1050/15/15/11549). Simulation and optimization of hydropower generation and environmental flows in the Middle Fork Project, California.

`ptreeopt/`: local copy of policy tree optimization code. Latest version maintained [here](https://github.com/jdherman/ptreeopt).

`mfp/`: Reservoir simulation model in `mfp.py`. The directory `mfp/data/` contains the input historical flows as well as the streamflow scenarios with modified vegetation due to forest treatment.

`results/`: output from simulation and optimization runs. Two main sets of outputs, `fit-historical` and `opt-historical`. The first is set to minimize the RMSE with observed reservoir storage, and the second maximizes hydropower generation under different scenarios. `results/` also contains plotting scripts.

The outer directory contains the main scripts and cluster job scripts for running the historical fit (`main-fit`) and optimization scenarios (`opt-all`).