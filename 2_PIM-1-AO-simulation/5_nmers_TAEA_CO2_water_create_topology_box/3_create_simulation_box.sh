cd topo
gmx insert-molecules -f nmers_10.pdb -ci taea_GMX.gro -nmol 50 -box 10 10 10 -o nmers_amines.gro
sleep 3s

gmx insert-molecules -f nmers_amines.gro -ci co2.gro -nmol 100 -o nmers_amines_co2.gro

#gmx insert-molecules -f 50amines_100co2.gro -ci n2_trappe.gro -nmol 100 -o 50amines_100co2_100n2. gro

gmx solvate -cp nmers_amines_co2.gro -cs spc216.gro -maxsol 100 -o solv.gro


