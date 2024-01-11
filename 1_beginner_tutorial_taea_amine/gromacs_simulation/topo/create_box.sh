gmx insert-molecules -f MOL_GMX.gro -ci MOL_GMX.gro -nmol 49 -box 5 5 5 -o 50amines.gro

gmx solvate -cp 50amines.gro -cs spc216.gro -maxsol 1000 -o solv.gro

