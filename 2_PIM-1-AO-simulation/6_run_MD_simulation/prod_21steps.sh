#!/bin/bash -l
#SBATCH --qos=normal

##SBATCH --partition=general
#SBATCH --partition=bigmem
##SBATCH --partition=gpu
#SBATCH --nodes=1

#SBATCH --job-name="jobname"
#conda init bash
#eval "$(conda shell.bash hook)"
#source /nfs/home/5/stiwari/softwares/gromacs/gromacs-5.1.4/install_remote_mpi/bin/GMXRC

module ()
{
    eval `/nfs/apps/Modules/3.2.10/bin/modulecmd bash $*`
}

module load gnu/8.2.0 openmpi/3.1.6_gnu8.2 plumed/2.8.0 gromacs/2021.4; which gmx_mpi

change_and_run(){
    i=$1
    rm $MDP/${i}.mdp
    cp -v ../MDP/sample.mdp $MDP/${i}.mdp
    sed -i "s/tempX/$2/g"   $MDP/${i}.mdp
    sed -i "s/pcouplX/$3/g" $MDP/${i}.mdp
    sed -i "s/pressX/$4/g"  $MDP/${i}.mdp
    sed -i "s/dtX/$5/g"     $MDP/${i}.mdp
    sed -i "s/stepX/$6/g"   $MDP/${i}.mdp

    prev_num=$(($i-1))


# Following are for extra steps as my some of my simulations were crashing. Please ignore if you don't want to include these.
    if [ $i == 31 ]; then
        prev_num=3
    elif [ $i == 4 ]; then
        prev_num=34

    elif [ $i == 61 ]; then
        prev_num=6
    elif [ $i == 7 ]; then
        prev_num=61

    elif [ $i == 91 ]; then
        prev_num=9
    elif [ $i == 10 ]; then
        prev_num=91
    fi

    echo $prev_num

    gmx_mpi grompp -v -f $topo/$MDP/${i}.mdp -c $sim/$sim_folder/${prev_num}.gro -maxwarn 3 -p $topo/topol.top -o $i.tpr
    mpirun gmx_mpi mdrun -deffnm $i
}

sim=$PWD
topo=$sim/topo
MDP="../21steps_MDP"

sim_folder=equil_sim
mkdir -p $sim_folder
cd $sim_folder

# rm *

gmx_mpi grompp    -v -f $sim/normal_MDP/em_steep.mdp -c $topo/solv.gro -maxwarn 3 -p $topo/topol.top -o min1.tpr
mpirun gmx_mpi mdrun     -deffnm min1

gmx_mpi grompp    -v -f $sim/normal_MDP/em_l-bfgs.mdp -c min1.gro -maxwarn 3 -p $topo/topol.top -o 0.tpr
gmx_mpi mdrun     -deffnm 0

# Pmax=10,000
pcoupl="C-rescale"
#function       step  temp    pcoupl             press     dt      steps
#               1       2       3                4         5       6
# Run steps differ from the paper by Colina et al.
change_and_run  1     600     no                 1         0.001   50000
change_and_run  2     300     no                 1         0.001   50000

change_and_run  3     300     $pcoupl            200       0.0001  500000
# Following 31 to 34 are extra steps as my some of my simulations were crashing.
change_and_run  31    300     $pcoupl            200       0.0005  800000 #500000
change_and_run  32    300     $pcoupl            200       0.0002  1000000 #500000
change_and_run  33    300     $pcoupl            200       0.0002  1000000 #500000
change_and_run  34    300     $pcoupl            200       0.0002  1000000 #500000

change_and_run  4     600     no                 1         0.0005  100000
change_and_run  5     300     no                 1         0.0005  200000
change_and_run  6     300     $pcoupl            6000      0.0001  1000000
# Following 61 is extra step as my some of my simulations were crashing.
change_and_run  61    300     $pcoupl            6000      0.0002  2000000

change_and_run  7     600     no                 1         0.0005  100000
change_and_run  8     300     no                 1         0.0005  200000
change_and_run  9     300     $pcoupl            10000     0.0001  1000000
# Following 91 is extra step as my some of my simulations were crashing.
change_and_run  91    300     $pcoupl            10000     0.0002  2000000

change_and_run  10     600     no                 1        0.0005  100000
change_and_run  11     300     no                 1        0.0005  200000
change_and_run  12     300     $pcoupl           5000      0.0002  50000

change_and_run  13     600     no                1         0.0005  10000
change_and_run  14     300     no                1         0.0005  20000
change_and_run  15     300     $pcoupl           1000      0.0002  50000

change_and_run  16     600     no                1         0.0005  10000
change_and_run  17     300     no                1         0.0005  20000
change_and_run  18     300     $pcoupl           100       0.0002  50000

change_and_run  19     600     no                1         0.0005  10000
change_and_run  20     300     no                1         0.0005  20000
change_and_run  21     300     $pcoupl           1         0.0005  100000

cd ..

production_dir=sim_pr
mkdir -p $production_dir
cd $production_dir

rm *

gmx_mpi grompp    -v -f $sim/normal_MDP/md.mdp -c $sim/equil_sim/21.gro -maxwarn 3 -p $topo/topol.top -o md.tpr
mpirun gmx_mpi mdrun    -deffnm md
