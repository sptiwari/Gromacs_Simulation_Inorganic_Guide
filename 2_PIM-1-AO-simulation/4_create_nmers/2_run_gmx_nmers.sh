# Running commands in this file is optional
# Understand and run these commands for practice.

rm -r run_gmx_short
mkdir -p run_gmx_short
cd run_gmx_short

# Copy 10 nmers
cp ../nmers_10.pdb .

# Copy .top file from 3_create_FF_nmer/MOL.amb2gmx
cp ../../3_create_FF_nmer/MOL.amb2gmx/MOL_GMX.top .

# Replace 1 MOL by 10 MOLs in this file
sed -i 's/MOL              1/MOL              10/g' MOL_GMX.top

# Copy mdp files from 3_create_FF_nmer/MOL.amb2gmx
cp ../../3_create_FF_nmer/MOL.amb2gmx/*.mdp .

# Run energy minimization followed by a short NVT MD simulation. Correct cutoffs etc., if you wish.
gmx grompp -c nmers_10.pdb -p MOL_GMX.top -f em.mdp -o em.tpr
gmx mdrun -v -deffnm em

gmx grompp -f md.mdp -c em.gro -p MOL_GMX.top -o md.tpr
gmx mdrun -ntmpi 1 -v -deffnm md
gmx trjconv -f md.trr -s md.tpr -o conf.pdb -pbc whole <<<0

rm \#*



exit
# Visualize
vmd conf.pdb

rm \#em.*
rm '#top.gro.1#'
