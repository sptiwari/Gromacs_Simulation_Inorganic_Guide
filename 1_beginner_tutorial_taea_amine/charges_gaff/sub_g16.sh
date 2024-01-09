#!/bin/bash -l
##
## Job Name as it will appear on squeue
#SBATCH --job-name="jn_6_TAEA_dir"
##
## Number of cores. Try to pick a multiple of 40 when using the general partition.
#SBATCH --tasks=40
##
## The partition to use
#SBATCH --partition=general
##SBATCH --partition=gpu

##Note: G16 will not run on multiple nodes. Requests should be 40 cores or less.

# Load Modules and Program Settings
module load gaussian/g16
setenv GAUSS_SCRDIR `pwd`
source $G16PATH/bsd/g16.login
source $G16PATH/bsd/g16.profile

# Run the program
g16 < com.com > lcom.log

# Delete any core dumps or Gau files
rm -rf Gau-*
rm -rf core*
rm -rf *.rwf

