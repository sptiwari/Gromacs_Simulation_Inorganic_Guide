# Choose either of following two. Second one is more folded.

#cp ../3_create_FF_nmer/MOL.amb2gmx/em_last.pdb nmer.pdb
cp ../3_create_FF_nmer/MOL.amb2gmx/md_last.pdb nmer.pdb

# Insert 9 more nmers to make 10 nmers in the box.
gmx insert-molecules -f nmer.pdb -ci nmer.pdb -box 10 10 10 -nmol 9 -o nmers_10.pdb
# gmx insert-molecules -f nmer.pdb -ci nmer.pdb -box 10 10 10 -nmol 9 -o nmers_10.gro

# Following command is optional: Packmol may be used for a better packing, if the previous command doesn't create 10 nmers. Another option is to increase the box size.

#packmol < packmol1.inp

rm \#*
