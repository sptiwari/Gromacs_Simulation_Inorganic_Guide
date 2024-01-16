# Copy amn_GMX.top and amn_GMX.gro files from earlier the charge_calculations folder.
cp ../../charges_gaff/charge_calculations/amn.amb2gmx/amn_GMX.* .

# Extract charges, bond, angle, and dihedral parameters of AMN molecule from amn_GMX.top file
awk '/\[ system \]/ {exit} {print}' amn_GMX.top | awk '/\[ moleculetype \]/,0' > amn_GMX.itp

# Extract the atomtypes of AMN from amn_GMX.top file
awk '/\[ moleculetype \]/ {exit} {print}' amn_GMX.top > atomtypes.itp

# Add the following atomstypes to atomtypes.itp for atoms of other molecules in the system.
echo ';SPC/E atomtypes
 Ow       8           15.99940  -0.8476  A     0.3165492      0.650299455
 Hw       1           1.00800   0.4238   A     0              0
;CO2 from Wei Shi paper (A version of TraPPE)
;Wei2008 https://pubs.acs.org/doi/10.1021/jp077223x double checked
 CCO2     6           12.0107   0.70     A     0.28000002359  0.22449252
 OCO2     8           15.99940  -0.350   A     0.30499997796  0.656841976
;Please double check the N parameters for N2:
 N        7           14.0      0        A     0.331          0.299

;[ nonbond_params ]
; i     j   func    sigma(c6)   eps(c12) ;Optionally add cross nonbond_params, if needed.
' >> atomtypes.itp

echo "Created amn_GMX.itp and atomtypes.itp"
