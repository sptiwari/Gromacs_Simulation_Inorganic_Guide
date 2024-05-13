# %%

# Ends of a polymer should be capped. I capped them with CH3 groups.
# So, in the following, tail has CH3 groups on one side, head has CH3 groups on the other side.
# And, body comes in between tail and head, and has no CH3 caps. Note that CH3 group is charge neutral.

ftail = "tail.mol2"
fbody = "body.mol2"
fhead = "head.mol2"

# In the following, we have a tail unit, followed by eight body units, followed by a head unit.
# Total 10-mers.
# polymer = [ftail, fbody, fbody, fbody, fbody, fbody, fbody, fbody, fbody, fhead]

# In the following, we have a tail unit, followed by one body unit, followed by a head unit.
# Total 3-mers.
polymer = [ftail, fbody, fhead]

# If you want to simulate only a monomer, please look at another folder, where I have capped the both sides of body with CH3 groups.

print(len(polymer))

# %%
import sys

# from biopandas.mol2 import PandasMol2
import pandas as pd
import numpy as np
import re

# total arguments
n = len(sys.argv)
# print("Total arguments passed:", n)
# Arguments passed
# print("\nName of Python script:", sys.argv[0])
# filename to open
try:
    filename = sys.argv[1]
except:
    filename = "body.mol2"
# filename to write
try:
    write_filename = sys.argv[2]
except:
    write_filename = "nmer_forGMX.mol2"

# filename = "final.mol2"
# write_filename = "uncapped.mol2"

print(filename, write_filename)

new_bond1_atoms = ["C24", "O4"]
new_bond2_atoms = ["C23", "O3"]


# %%
def bond_parser(filename):
    with open(filename, "r") as f:
        f_text = f.read()
    bonds = np.array(
        re.sub(
            r"\s+", " ", re.search(r"@<TRIPOS>BOND([a-z0-9\s]*)@", f_text).group(1)
        ).split()
    ).reshape((-1, 4))
    df_bonds = pd.DataFrame(bonds, columns=["bond_id", "atom1", "atom2", "bond_type"])
    # df_bonds.set_index(['bond_id'], inplace=True)
    df_bonds["atom1"] = df_bonds["atom1"].astype("int")
    df_bonds["atom2"] = df_bonds["atom2"].astype("int")
    df_bonds["bond_id"] = df_bonds["bond_id"].astype("int")

    return df_bonds


def atom_parser(filename):
    with open(filename, "r") as f:
        f_text = f.read()
    regex = r"\@\<TRIPOS\>ATOM\n([\s\S]*?)\@\<TRIPOS\>"
    m1 = re.search(regex, f_text)
    m2 = m1.group(1).split()
    # print(m1.group(1).split())
    m3 = np.array(m2)
    # print(m3)
    # print(m3.shape)
    atoms = m3.reshape(-1, 9)
    columns = [
        "atom_id",
        "atom_name",
        "x",
        "y",
        "z",
        "atom_type",
        "mol_id",
        "mol_name",
        "charge",
    ]
    df_atoms = pd.DataFrame(atoms, columns=columns)
    df_atoms["atom_id"] = df_atoms["atom_id"].astype("int")
    df_atoms["x"] = df_atoms["x"].astype("float")
    df_atoms["y"] = df_atoms["y"].astype("float")
    df_atoms["z"] = df_atoms["z"].astype("float")
    return df_atoms


def atom_id_from_atom_name(df, atom_name):
    return df[df["atom_name"] == atom_name].index.values + 1


def translate_df(df, translate_len_x, translate_len_y, translate_len_z):
    df2 = df.copy()
    df2["x"] = df2["x"] + float(translate_len_x)
    df2["y"] = df2["y"] + float(translate_len_y)
    df2["z"] = df2["z"] + float(translate_len_z)
    # df2['x'] = df2['x'] + del_z
    return df2


def new_bond_idx_fn(df, new_bond_atoms):
    new_bond_idx = []
    i = 0
    for atom in new_bond_atoms:
        atom_ids = atom_id_from_atom_name(df, atom)
        # print(atom, atom_ids)
        if i == 0:
            new_bond_idx.append(atom_ids[-2])
            i = i + 1
        else:
            new_bond_idx.append(atom_ids[-1])

    # print(new_bond_idx)
    return new_bond_idx


def make_atoms_df(df, df2, translate_len_x, translate_len_y, translate_len_z):
    df2 = translate_df(df2, translate_len_x, translate_len_y, translate_len_z)

    frames = [df, df2]
    df_concat = pd.concat(frames)
    df_concat.reset_index(inplace=True, drop=True)

    atom_id_new = 0
    for index, row in df_concat.iterrows():
        atom_id_new = atom_id_new + 1
        # df_concat.loc[index, 'atom_id'] = atom_id_new
        df_concat.loc[index, "atom_id"] = atom_id_new
        # print(atom_id_new, df_concat.loc[index, 'atom_id'])

    df = df_concat
    return df


def make_bonds_df(df, df2, new_bond_idx1, new_bond_idx2, num_atoms_df):
    num_bonds_file1 = len(df)
    frames = [df, df2]
    df_concat = pd.concat(frames)
    df_concat.reset_index(inplace=True, drop=True)

    df = df_concat.copy()

    bond_id_new = 0
    for index, row in df.iterrows():
        bond_id_new = bond_id_new + 1
        df.loc[index, "bond_id"] = bond_id_new
        # # print(index, row)
        atom1_old = df.loc[index, "atom1"]
        atom2_old = df.loc[index, "atom2"]

        if bond_id_new <= num_bonds_file1:
            df.loc[index, "atom1"] = atom1_old
            df.loc[index, "atom2"] = atom2_old

        else:
            df.loc[index, "atom1"] = atom1_old + num_atoms_df
            df.loc[index, "atom2"] = atom2_old + num_atoms_df

    # df.loc[bond_id_new-1,'atom2'] = atom2_old + num_atoms_file1
    df.loc[len(df.index)] = [bond_id_new + 1, new_bond_idx1[0], new_bond_idx1[1], 1]
    df.loc[len(df.index)] = [bond_id_new + 2, new_bond_idx2[0], new_bond_idx2[1], 1]

    return df


# %%

translate_len_x = 25.7
translate_len_y = 0.3
translate_len_z = 3

i = 0
for fname in polymer[1:]:
    if i == 0:
        df1 = atom_parser(polymer[0])
        df3 = bond_parser(polymer[0])
        atoms_df = df1
        bonds_df = df3

    else:
        df1 = atoms_df
        df3 = bonds_df

    i = i + 1

    df2 = atom_parser(fname)
    df4 = bond_parser(fname)

    atoms_df = make_atoms_df(
        df1, df2, i * translate_len_x, i * translate_len_y, i * translate_len_z
    )

    # Find atom_ids corresponding to new_bond1_atoms
    new_bond_idx1 = new_bond_idx_fn(atoms_df, new_bond1_atoms)
    new_bond_idx2 = new_bond_idx_fn(atoms_df, new_bond2_atoms)

    num_atoms_df1 = len(df1)
    bonds_df = make_bonds_df(df3, df4, new_bond_idx1, new_bond_idx2, num_atoms_df1)


print(atoms_df)
print(bonds_df)


# %%

# print(df.dtypes)

# a2 = df.dropna()
# bonds_df = a2.copy()
# # print(df.dtypes)

# # df.to_csv('new.mol2')
# bonds_df['atom1'] = bonds_df['atom1'].astype('int')
# bonds_df['atom2'] = bonds_df['atom2'].astype('int')
# total_bonds = len(bonds_df)
# bonds_df['bond_id'] = bonds_df['bond_id'].astype('int')
# bonds_df['bond_id'] = np.arange(1, rem_bonds+1, 1)
# print(b.dtypes)
# bonds_df.to_csv('bonds.mol2', index=False, sep = "\t")
# print(len(bonds_df))

# %%
# write to new file


def write_mol2(write_filename, atoms_df, bonds_df):
    total_atoms = len(atoms_df)
    total_bonds = len(bonds_df)
    f = open(write_filename, "w")
    f.write(f"""@<TRIPOS>MOLECULE
MOL
   {total_atoms}    {total_bonds}     1     0     0
SMALL
rc


""")

    f.write("@<TRIPOS>ATOM\n")
    f.close()

    f = open(write_filename, "a")
    atoms_df.to_csv(write_filename, mode="a", header=False, index=False, sep="\t")
    f.close()

    f = open(write_filename, "a")
    f.write("@<TRIPOS>BOND\n")
    f.close()

    f = open(write_filename, "a")
    bonds_df.to_csv(write_filename, mode="a", header=False, index=False, sep="\t")

    f.close()

    f = open(write_filename, "a")
    f.write(f"""@<TRIPOS>SUBSTRUCTURE
     1 MOL         1 TEMP              0 ****  ****    0 ROOT
""")
    f.close()


write_mol2(write_filename, atoms_df, bonds_df)
