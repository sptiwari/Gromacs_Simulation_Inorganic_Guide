rm *.mol2

cp ../1_polymer_components_tail_body_head/tail.mol2 .
cp ../1_polymer_components_tail_body_head/body.mol2 .
cp ../1_polymer_components_tail_body_head/head.mol2 .

python make_nmer_for_gmx.py
