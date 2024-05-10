#!/bin/bash -l

#SBATCH --qos=normal

##SBATCH --partition=general
#SBATCH --partition=bigmem
##SBATCH --partition=gpu
#SBATCH --nodes=1

#SBATCH --job-name="mmm"

#conda init bash
#eval "$(conda shell.bash hook)"

#source /nfs/home/5/stiwari/softwares/gromacs/gromacs-5.1.4/install_remote_mpi/bin/GMXRC

module ()
{
    eval `/nfs/apps/Modules/3.2.10/bin/modulecmd bash $*`
}

module load gnu/8.2.0 openmpi/3.1.6_gnu8.2 plumed/2.8.0 gromacs/2021.4
which gmx_mpi

set sim=$PWD
set topo=$sim/topo

set production_dir=sim_pr
mkdir -p $production_dir
cd $production_dir


gmx convert-tpr -s md.tpr -extend 50000000 -o next.tpr
mpirun gmx mdrun -s next.tpr -cpi md.cpt -deffnm md

#tpbconv -s previous.tpr -extend timetoextendby -o next.tpr
#mdrun -s next.tpr -cpi previous.cpt
