antechamber -i lcom.log -o a.mol2 -fi gout -fo mol2 -s 2 -c resp #-at amber

#use -pf  remove intermediate files: yes(y) or no(n)[default]

cp a.mol2 bonded_a.mol2
antechamber -i bonded_a.mol2 -fi mol2 -o b.mol2 -fo mol2 -s 2

cp ~/old_programs/atom_equiv_mol2_v2.py .
python atom_equiv_mol2_v2.py b.mol2 #Gives new_file.mol2


parmchk2 -i new_file.mol2 -f mol2 -o c.frcmod
cp c.frcmod final.frcmod

echo '
# Run the following commands in tleap together:

tleap -f leaprc.gaff

a=loadmol2 b.mol2
loadamberparams final.frcmod
#saveMol2 a bbb.mol2 1
saveamberparm a top.prmtop crd.inpcrd
check a
quit

# After quitting tleap, run the following command:
acpype -p top.prmtop -x crd.inpcrd -b amn #amn for amine
'


