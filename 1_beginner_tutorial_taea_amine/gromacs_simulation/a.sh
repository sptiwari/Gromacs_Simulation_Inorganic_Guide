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


sim=$PWD
topo=$sim/topo

sim_folder=equil_sim
mkdir -p $sim_folder
cd $sim_folder

rm *

gmx_mpi grompp    -v -f $sim/normal_MDP/em_steep.mdp -c $topo/solv.gro -maxwarn 3 -p $topo/topol.top -o min1.tpr
exit
mpirun gmx_mpi mdrun     -deffnm min1

gmx_mpi grompp    -v -f $sim/normal_MDP/em_l-bfgs.mdp -c min1.gro -maxwarn 3 -p $topo/topol.top -o min2.tpr
gmx_mpi mdrun     -deffnm min2

gmx_mpi grompp    -v -f $sim/normal_MDP/nvt.mdp -c min2.gro -maxwarn 3 -p $topo/topol.top -o nvt.tpr

mpirun -np 1 gmx_mpi mdrun     -deffnm nvt
exit

gmx_mpi grompp    -v -f $sim/normal_MDP/npt.mdp -c nvt.gro -maxwarn 3 -p $topo/topol.top -o npt.tpr -t nvt.cpt
mpirun -np 4 gmx_mpi mdrun     -deffnm npt

cd ..

production_dir=sim_pr
mkdir -p $production_dir
cd $production_dir

rm *

gmx_mpi grompp    -v -f $sim/normal_MDP/md.mdp -c $sim/equil_sim/npt.gro -maxwarn 3 -p $topo/topol.top -o md.tpr
mpirun -np 4 gmx_mpi mdrun    -deffnm md

