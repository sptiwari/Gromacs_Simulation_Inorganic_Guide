eval "$(conda shell.bash hook)"
conda activate AmberTools23

rm *.tpr *.gro *.pdb *.log
rm MOL_GMX.*

cp ../2_create_nmer_from_components/nmer_forGMX.mol2 nmer.mol2

#Modify for nmers. Not done here.
#cp ../body.mol2 bonded_a.mol2

cp nmer.mol2 bonded_a.mol2

antechamber -i bonded_a.mol2 -fi mol2 -o b.mol2 -fo mol2 -s 2 -rn MOL -at gaff2

cp ~/old/atom_equiv_mol2_v2.py .
python atom_equiv_mol2_v2.py b.mol2 #Gives new_file.mol2

parmchk2 -i new_file.mol2 -f mol2 -o c.frcmod -s 2 -rn MOL # -s 2 for gaff2
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
acpype -p top.prmtop -x crd.inpcrd -b MOL #amn for amine

rm -v *.mol2
rm -v c.frcmod crd.inpcrd leap.log top.prmtop final.frcmod
'
#Manually removing the intermediate files generated from using antechamber:
rm A* esout punch qout QOUT

