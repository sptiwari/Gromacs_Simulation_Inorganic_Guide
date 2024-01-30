gmx insert-molecules -f amn_GMX.gro -ci amn_GMX.gro -nmol 49 -box 5 5 5 -o 50amines.gro
sleep 3s

gmx insert-molecules -f 50amines.gro -ci co2.gro -nmol 100 -o 50amines_100co2.gro

gmx insert-molecules -f 50amines_100co2.gro -ci n2_trappe.gro -nmol 100 -o 50amines_100co2_100n2.gro

gmx solvate -cp 50amines_100co2_100n2.gro -cs spc216.gro -maxsol 1000 -o solv.gro

rm \#*


# Note: If we want the order of molecules to be different, say N2 molecules should come in the end, following commands can be used. Also change the order of molecules in topol.top file.

# gmx insert-molecules -f amn_GMX.gro -ci amn_GMX.gro -nmol 49 -box 5 5 5 -o 50amines.gro
# gmx insert-molecules -f 50amines.gro -ci co2.gro -nmol 100 -o 50amines_100co2.gro
# gmx solvate -cp 50amines_100co2.gro -cs spc216.gro -maxsol 1000 -o a.gro
# gmx insert-molecules -f a.gro -ci n2.gro -nmol 100 -o solv.gro

cd ..
bash a.sh
