 # -*- coding: utf-8 -*-
"""
Created on 4/4/18 US date
revised on 4/3/20 for python3
@author: stiwari

Read mol2 file, find equivalent atoms, average their charges, and write a new mol2 file.
"""
#from __future__ import print_function
import math
import sys
import re
import datetime
import os


def process_file(filename):

    ### Read the file ###
    mol_file = open (filename, 'r')
    rline = mol_file.readlines()
    mol_file.close()

    # Read atomname and charge information:
    for i in range (len(rline)):
        if "<TRIPOS>ATOM" in rline[i]:
            start = i

    for m in range (start, len(rline)):
        if "<TRIPOS>BOND" in rline[m]:
            end = m
            break

    total_charge = 0
    atomDetails_array = []
    for line in rline[start+1 : end] :
        words = line.split()
        atom_name = str(words[1])
        atom_type = str(words[5])
        charge = float(words[8])
        total_charge += charge

        atomDetails_array.append ([atom_name, atom_type, charge])
#        print atom_name, atom_type, charge
#        print total_charge

#    print atomDetails_array

    # Read the Bond information:
    for i in range (len(rline)):
        if "BOND" in rline[i]:
            start = i

    end = None
    for m in range (start, len(rline)):
        if "SUBSTRUCTURE" in rline[m]:
            end = m
            break
    if end == None:
        end = len(rline)


    bond_array = []
    for line in rline[start+1 : end] :
        words = line.split()
        bond_atom1 = int(words[1])
        bond_atom2 = int(words[2])

        bond_array.append ([bond_atom1, bond_atom2])
#        print (bond_atom1, bond_atom2)

    atomicPath_list_full_arr = []
    atomNumber = 0
    score_arr_all = []

    # Calculate atom paths and scores for all the paths for all the atoms:
    for atomDetails in atomDetails_array:
        atomNumber += 1
#        print (atomNumber)
        atom_name = atomDetails[0]

        parentAtom = None
#        first_parentAtom = atomNumber
        parentAtoms_list = []
        super_parentAtom = None
        # Get the path in shorter format:
        atomicPath_list = atomicPath_fn(atomNumber, parentAtom, parentAtoms_list, bond_array)
#        atomicPath_list = atomicPath_fn2(atomNumber, parentAtom, super_parentAtom, bond_array)
        atomicPath_list_full_arr.append(atomicPath_list)
        print (atomicPath_list)
        print (len(atomicPath_list))

        parent_list = []
        level = 0
        all_paths_atom_arr = []
    #    atomicPath_list = [1, [2, [6], [7], [8, [9], [10, [12], [13], [14]], [11]]], [3], [4], [5]]
        # Get all the paths for each atom:
        all_paths_atom = get_all_paths(atomicPath_list, parent_list, level, all_paths_atom_arr)
#        print all_paths_atom

        # Calculate scores for paths:
        score_arr_atom = []
        for i in all_paths_atom:
            score = score_fn(i, atomDetails_array)
#            print i, score
            score_arr_atom.append(score)

#        print sorted(score_arr_atom)
        score_arr_all.append([atomNumber, sorted(score_arr_atom)])
#        score_arr_all.append(score_arr_atom)
#        print score_arr_all

    # Compare the path arrays and find equivalent atoms:
    k = 0
    recorded_atoms_arr = []
    eq_atoms_arr_all = []
    for i in score_arr_all:
        k += 1
        eq_atoms_arr = []
        eq_atoms_arr.append(i[0])
        if i[0] in recorded_atoms_arr:
            continue
#            pass
        for j in score_arr_all[k:]:
            if i[0] != j[0]:
                if i[1] == j[1]:
#                    print i[0], j[0]
                    eq_atoms_arr.append(j[0])
                    recorded_atoms_arr.append(j[0])

        eq_atoms_arr_all.append(eq_atoms_arr)


    # Find charges for all equivalent atoms:
    avg_charge_arr = []
    print ("Equiv atoms, Current charges, New charges")
    for eq_atoms_arr in eq_atoms_arr_all:
        charges_eq_atoms_arr = charges_eq_atoms_fn(eq_atoms_arr, atomDetails_array)
        avg_charge = round(sum(charges_eq_atoms_arr)/len(charges_eq_atoms_arr), 7)
        print (eq_atoms_arr, charges_eq_atoms_arr, avg_charge)
        avg_charge_arr.append(avg_charge)

    atom_no = 0
    atom_no_newCharges_arr = []
    for atomDetails in atomDetails_array:
        atom_no += 1
        for i in zip (eq_atoms_arr_all, avg_charge_arr):
            for j in i[0]:
                if atom_no == j:
#                    print j, i[1]
                    atom_no_newCharges_arr.append([j, i[1]])


    write_file_mol(filename, atom_no_newCharges_arr)


def atomicPath_fn2(atomNumber, parentAtom, super_parentAtom, bond_array):

    neighbor = None
    neighbor_list = [atomNumber]
    num_of_bonds_for_atomNumber = 0

    for i, j in bond_array:

        if i == atomNumber:
            neighbor = j
            num_of_bonds_for_atomNumber += 1
        elif j == atomNumber:
            neighbor = i
            num_of_bonds_for_atomNumber += 1

#    print (atomNumber, num_of_bonds_for_atomNumber)
    if neighbor == parentAtom:
        if num_of_bonds_for_atomNumber == 1:
#            print (atomNumber)
            return [atomNumber]

#    print atomNumber, num_of_bonds_for_atomNumber
#
    if neighbor == super_parentAtom:
        if num_of_bonds_for_atomNumber > 1:
#            print (atomNumber)
            return [atomNumber]


    for i, j in bond_array:

        neighbor = None
        if i == atomNumber:
            neighbor = j
        elif j == atomNumber:
            neighbor = i

        if neighbor == parentAtom:
            continue
        elif neighbor == super_parentAtom:
            continue
#        continue

        if neighbor != None:
#            print (neighbor, atomNumber)
            super_parentAtom = atomNumber
            gg = atomicPath_fn2(neighbor, atomNumber, super_parentAtom, bond_array)
            neighbor_list.append(gg)

#    print (neighbor_list)
    return neighbor_list




def atomicPath_fn(atomNumber, parentAtom, parentAtoms_list, bond_array):

    neighbor = None
    neighbor_list = [atomNumber]
    num_of_bonds_for_atomNumber = 0

    for i, j in bond_array:

        if i == atomNumber:
            neighbor = j
            num_of_bonds_for_atomNumber += 1
        elif j == atomNumber:
            neighbor = i
            num_of_bonds_for_atomNumber += 1

#    print (atomNumber, num_of_bonds_for_atomNumber)
    if neighbor == parentAtom:
        if num_of_bonds_for_atomNumber == 1:
#                print (atomNumber)
            return [atomNumber]

#    print atomNumber, num_of_bonds_for_atomNumber
#
#    if neighbor in parentAtoms_list:
#        if num_of_bonds_for_atomNumber > 1:
##            print (atomNumber)
#            return [atomNumber]


    for i, j in bond_array:

        neighbor = None
        if i == atomNumber:
            neighbor = j
        elif j == atomNumber:
            neighbor = i

        if neighbor == parentAtom:
            continue
        elif neighbor in parentAtoms_list:
            continue

        if neighbor != None:
#            print (neighbor, atomNumber)
            parentAtoms_list.append(atomNumber)
            gg = atomicPath_fn(neighbor, atomNumber, parentAtoms_list, bond_array)
            neighbor_list.append(gg)

#    print (neighbor_list)
    return neighbor_list



def write_file_mol(filename, atom_no_newCharges_arr):

    read_file = open (filename, 'r')
    rline = read_file.readlines()
    read_file.close()
    # Read atomname and charge information:
    for i in range (len(rline)):
        if "<TRIPOS>ATOM" in rline[i]:
            start = i

    # Read bond information:
    for m in range (start, len(rline)):
        if "<TRIPOS>BOND" in rline[m]:
            end = m
            break

    read_file = open (filename, 'r')
    write_file = open ("new_file.mol2", 'w')
    print ('\nWrote new charges in new_file.mol2')

    line_no = 0
    for line in read_file:
        line_no += 1
#        print line_no
        if line_no > start+1 and line_no <= end:
            words = line.split()
            for i in words:
                for j in atom_no_newCharges_arr:
#                    print words[0], j[0]
                    if int(words[0]) == j[0]:
                        words[-1] = j[1]
            for i in words:
#                print i,
                write_file.write(str(i) + "\t")
            write_file.write("\n")
#            print ""
        else:
#            print line.rstrip() #sys.stdout.write(line)
            a = str(line)
            write_file.write(a)



def charges_eq_atoms_fn(eq_atoms_arr, atomDetails_array):

    charge_arr = []
    for atom_no in eq_atoms_arr:
        i = 0
        for atomDetails in atomDetails_array:
            i += 1
            if atom_no == i:
#                atomDetails[2] = 0
#                print i, atomDetails[2]
                charge_arr.append(atomDetails[2])
    return charge_arr


def score_fn(path_atom, atomDetails_array):

    i = 0
    score = 0
    for j in path_atom:
        i += 1
        atomic_number = find_atomic_number(j, atomDetails_array)
        score += i*0.11 + atomic_number*0.08
#        print j, i, score
    return round(score,2)



def find_atomic_number(j, atomDetails_array):

    atom_no = 0
    for atomDetails in atomDetails_array:
        atom_no += 1
#        print atomDetails, atom_no
        if atom_no == j:
            atom_type = atomDetails[1]
#            print j, atom_type
            break
#    print atom_type
    #"read file later"
    if atom_type == 'C.3': an = 6
    if atom_type == 'c3': an = 6
    if atom_type == 'cg': an = 6
    if atom_type == 'cc': an = 6
    if atom_type == 'C.ar': an = 6
    if atom_type == 'ca': an = 6
    if atom_type == 'ce': an = 6
    if atom_type == 'c': an = 6
    if atom_type == 'c1': an = 6
    elif atom_type == 'c5': an = 6
    elif atom_type == 'H': an = 1
    elif atom_type == 'hc': an = 1
    elif atom_type == 'h4': an = 1
    elif atom_type == 'h1': an = 1
    elif atom_type == 'h2': an = 1
    elif atom_type == 'ho': an = 1
    elif atom_type == 'ha': an = 1
    elif atom_type == 'hn': an = 1
    elif atom_type == 'hx': an = 1
    elif atom_type == 'Si': an = 14
    elif atom_type == 'N': an = 7
    elif atom_type == 'n': an = 7
    elif atom_type == 'nh': an = 7
    elif atom_type == 'n1': an = 7
    elif atom_type == 'n2': an = 7
    elif atom_type == 'n3': an = 7
    elif atom_type == 'n4': an = 7
    elif atom_type == 'n7': an = 7
    elif atom_type == 'n8': an = 7
    elif atom_type == 'ne': an = 7
    elif atom_type == 'nv': an = 7
    elif atom_type == 'O': an = 8
    elif atom_type == 'o': an = 8
    elif atom_type == 'os': an = 8
    elif atom_type == 'oh': an = 8
    elif atom_type == 'Co': an = 27
    elif atom_type == 'p5': an = 15
    elif atom_type == 'f': an = 9
    #Put new atom_type's atomic number here using elif information.

#    else: an=1

    try:
        an
    except NameError:
        print ("atomic number of", atom_type, "not found. Plz add.")
        sys.exit('Please enter the atom_type\'s atomic number in the python file.')

    return an


def get_all_paths(atomicPath_list, parent_list, level, all_paths_atom_arr):

    if len(atomicPath_list) == 1:
        parent_list.append(atomicPath_list[0])
#        print parent_list, level
        all_paths_atom_arr.append(parent_list[:])

    for i in atomicPath_list:
        if isinstance(i, int):
            parent_list.append(i)
            level += 1
        elif isinstance(i, list):
            get_all_paths(i, parent_list[:level], level, all_paths_atom_arr)

    return all_paths_atom_arr


def score_atom(atomicPath_list, position_index_prev, score_total, score_arr, atomDetails_array):

    if len(atomicPath_list) == 1:
        position_index = position_index_prev + 1
        score_total += position_index*0.11
        score_arr.append(score_total)
        print (atomicPath_list, score_total, score_arr, position_index)
        return score_total, score_arr


    for i in atomicPath_list:
        if isinstance(i, int):
            atomNumber = i
#            score_arr.append(score_total)
#            print score_total
        elif isinstance(i, list):
            next_array = i
#            print next_array

            position_index = position_index_prev + 1
            score_total += position_index*0.11

            score_atom(next_array, position_index, score_total, score_arr, atomDetails_array)



def main():

    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit ("enter format: \npython atom_equiv_mol2.py filename") #filename = "b.mol2"
    else:
        filename = "b.mol2"
        filename = args[0]

    if os.path.isfile(filename):
        print ("Opened", filename, "for processing...")
        process_file(filename)
    else:
        print (filename, "not found")
        sys.exit("Entered filename not found")


if __name__ == '__main__':
  main()

