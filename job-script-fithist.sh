#!/bin/bash -l
#SBATCH -n 96            # Total number of processors to request (32 cores per node)
#SBATCH -p high           # Queue name hi/med/lo
#SBATCH -t 32:00:00        # Run time (hh:mm:ss) - 24 hours
#SBATCH --mail-user=jdherman@ucdavis.edu              # address for email notification
#SBATCH --mail-type=ALL                  # email at Begin and End of job

module swap openmpi/1.6.5
mpirun python main-fit-hist.py
