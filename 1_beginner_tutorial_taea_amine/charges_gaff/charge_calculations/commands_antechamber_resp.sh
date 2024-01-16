eval "$(conda shell.bash hook)"
conda activate AmberTools23

antechamber -i lcom.log -o a.mol2 -fi gout -fo mol2 -s 2 -c resp -at gaff2
#use -pf  remove intermediate files: yes(y) or no(n)[default]

cp a.mol2 bonded_a.mol2

#I changed the residue name from default MOL to AMN:
antechamber -i bonded_a.mol2 -fi mol2 -o b.mol2 -fo mol2 -s 2 -rn AMN

cp ~/old_programs/atom_equiv_mol2_v2.py .
python atom_equiv_mol2_v2.py b.mol2 #Gives new_file.mol2


parmchk2 -i new_file.mol2 -f mol2 -o c.frcmod
cp c.frcmod final.frcmod

echo '
# Run the following commands in tleap together:
conda activate AmberTools23

tleap -f leaprc.gaff2

a=loadmol2 new_file.mol2
loadamberparams final.frcmod
#saveMol2 a bbb.mol2 1
saveamberparm a top.prmtop crd.inpcrd
check a
quit

# After quitting tleap, run the following command:
acpype -p top.prmtop -x crd.inpcrd -b amn #amn for amine
'
#Manually removing the intermediate files generated from using antechamber:
rm A* esout punch qout QOUT


