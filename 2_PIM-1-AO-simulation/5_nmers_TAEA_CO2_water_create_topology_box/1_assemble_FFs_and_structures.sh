# Create a topo folder and assemble all FF files

rm -r topo
mkdir -p topo
cd topo

# Copy 10 nmers from 4_create_nmers folder
cp ../../4_create_nmers/nmers_10.pdb .

# Copy .top file from 3_create_FF_nmer/MOL.amb2gmx
cp ../../3_create_FF_nmer/MOL.amb2gmx/MOL_GMX.top .

# Copy FFs for TAEA, CO2 and water
cp ../TAEA_ff/* .
cp ../co2_ff/* .
cp ../water_ff/* .

# Replace 1 MOL by 10 MOLs in this file
# sed -i 's/MOL              1/MOL              10/g' MOL_GMX.top

