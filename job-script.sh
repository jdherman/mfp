#!/bin/bash -l
#SBATCH -n 256            # Total number of processors to request (32 cores per node)
#SBATCH -p high           # Queue name hi/med/lo
#SBATCH -t 24:00:00        # Run time (hh:mm:ss) - used to be 240 hrs
#SBATCH --mail-user=jdherman@ucdavis.edu              # address for email notification
#SBATCH --mail-type=ALL                  # email at Begin and End of job

# module swap openmpi/1.6.5
export PATH=/group/hermangrp/miniconda3/bin:$PATH
mpirun python main-opt-all-REDO.py
