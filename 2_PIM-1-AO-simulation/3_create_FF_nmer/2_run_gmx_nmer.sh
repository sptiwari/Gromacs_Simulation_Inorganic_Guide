cd MOL.amb2gmx
gmx editconf -f MOL_GMX.gro -box 10 10 10 -o gro.gro

gmx grompp -c gro.gro -p MOL_GMX.top -f em.mdp -o em.tpr
gmx mdrun -v -deffnm em
gmx trjconv -f em.trr -s em.tpr -o em.pdb -pbc whole <<<0


gmx grompp -f md.mdp -c em.gro -p MOL_GMX.top -o md.tpr
gmx mdrun -ntmpi 1 -v -deffnm md
gmx trjconv -f md.trr -s md.tpr -o conf.pdb -pbc whole <<<0

gmx trjconv -f md.trr -s md.tpr -o em_last.pdb -e 0.001 -pbc whole <<<0
gmx trjconv -f md.trr -s md.tpr -o md_last.pdb -b 10 -pbc whole <<<0



rm \#*



exit
vmd em.gro em.trr

rm \#em.*
rm '#top.gro.1#'
