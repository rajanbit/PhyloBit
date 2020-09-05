#!/usr/bin/python
#!python

"""

PhyloBit Version 1.0 2020

PhyloBit is a Phylogenetic tree construction tool that is based
on Distance-Matrix method for making tree.

Numpy is used for making Distance-matrix and handling Average-distance-matrix(s).

It takes aligned multi fasta file as an argument and return the tree.

"""

####################__IMPORTING_MODULES__#####################
##############################################################

import sys
import numpy as np
import numpy.ma as mask

####################__MAKE_SEQUENCE_LIST__####################
##############################################################

# Input and Read Multi_FASTA record
multi_fasta_file = sys.argv[1]
multi_fasta = open(multi_fasta_file)
fasta_rec = multi_fasta.readlines()

print("Phylogenetic tree construction initiated...")

# Make Accession list
def make_acc_list(fasta_records):
	acc_list = []
	for line in fasta_records:
		if line[0] == ">":
			acc_list.append(line[1:10])
	return(acc_list)

# Parsing Multi_FASTA record
def parsing_data(acc_id, data):
	head_index = None
	temp_list = []
	seq = ""
	header = ""
	for i in range(0, len(data)):
		data_f = data[i]
		if acc_id in data_f:
			header += data_f.replace("\n", "")
			head_index = i
			break
	if head_index != None:
		for i in range(head_index+1, len(data)):
			data_s = data[i]
			if data_s[0] != ">":
				seq += data_s.replace("\n", "")
			else:
				break
	temp_list.append(header)
	temp_list.append(seq)
	return(temp_list)

# Make Sequence_list from Multi_FASTA record
def seq_to_list():
	l_fasta = []
	acc_list = make_acc_list(fasta_rec)
	for i in range(0, len(acc_list)):
		acc_id = acc_list[i]
		f2 = parsing_data(acc_id, fasta_rec)
		l_fasta.append(f2)
	return(l_fasta)

# Make Name_list from Sequence_list
def name_list():
	list_fasta = seq_to_list()
	n_list = []
	for i in range(len(list_fasta)):
		name = list_fasta[i][0][1:]
		n_list.append(name)
	return(n_list)

###################__MAKE_DISTANCE_MATRIX__###################
##############################################################

# Make Distance_Matrix from Sequence data
def distance_matrix():
	seq_list = seq_to_list()
	n = len(seq_list)
	d_matrix = np.full((n, n), 0)
	for i in range(0, len(seq_list)):
		seq_i = seq_list[i][1]
		for j in range(i+1, len(seq_list)):
			seq_j = seq_list[j][1]
			if len(seq_i) == len(seq_j):
				diff_nt = 0
				for k in range(0, len(seq_i)):
					if seq_i[k] != seq_j[k]:
						diff_nt += 1
			d_matrix[i,j] = diff_nt 
			diff_nt = 0
			d_matrix[j,i] = d_matrix[i,j]
	return(d_matrix)

######__Additional_Functions__for_making_Matrix_&_Tree_#######
##############################################################

# Create list used to switch from Distance_matrix to Average_distance_matrix
def d_matrix_list(matrix):
	d_list = []
	for i in range(len(matrix)):
		d_list.append(i)
	return(d_list)

# Find Minimum_Distance in matrix
def find_min_distance(matrix):
	mask_mat = (mask.masked_array(matrix, mask=matrix==0))
	min_dis = mask_mat.min()
	index = np.where(matrix == min_dis)
	index_min_dis = index[0][0],index[1][0]
	i_list = list(index_min_dis)
	return(i_list)

# Create New_list to switch from one Average_distance_matrix to another
def new_list(l1, l2):
	d_list  = [x for x in l1 if x not in l2]
	new_list = [l2]+d_list
	return(new_list)

# Create Header_list(initial_tree) for making phylogenetic tree
def header_list(fasta_records):
	list1 = []
	for line in fasta_records:
		if line[0] == ">":
			list1.append(line[1:].replace("\n", ""))
	return(list1)

##################__MAKE_PHYLOGENETIC_TREE__##################
##############################################################

# Make Average_Distance_Matrix(s) from Distance_Matrix
print("Constructing Distance_Matrix...")
array = distance_matrix()
min_d = find_min_distance(array)
l = d_matrix_list(distance_matrix())
n_list = new_list(l, min_d)
def avg_dis_mat(matrix, list1):
	new_len = (len(matrix)-1)
	new_m = np.full((new_len,new_len), 0)
	new_m = new_m.astype(float)
	new_m_element = 0
	for i in range (1,len(list1)):
		data = list1[i]
		dis_avg = 0
		for data1 in list1[0]:
			dis_avg  += matrix[data,data1]
		new_m[0,i] = (dis_avg/2.0)
		new_m[i,0] = new_m[0,i]
	for i in range(1,len(list1)):
		i1 = list1[i]
		for j in range(i+1, len(list1)):
			i2 = list1[j]
			new_m[i,j] = matrix[i1,i2]
			new_m[j,i] = new_m[i,j]
	return(new_m)

# Running Average_Distance_Matrix_function & Additional_Functions
def out_ADM(matrix, list1):
	mat = avg_dis_mat(matrix, list1)
	m_list = d_matrix_list(mat)
	min_index = find_min_distance(mat)
	new_l = new_list(m_list,min_index)
	new_mat = avg_dis_mat(mat, new_l)
	return(mat,new_mat,new_l)

# Make Phylogenetic_Tree
init_tree = header_list(fasta_rec)
def tree_maker(matrix,list1):
	index = []
	min_d = find_min_distance(matrix)
	for data in min_d:
		index.append(list1[data])
	return(index)

##############################################################
#######################__Running_All__########################

print("Constructing Average_Distance_Matrix...")
r = out_ADM(array,n_list)
a = r[0]
b = r[1]
c = r[2]
tree = new_list(init_tree, tree_maker(array,init_tree))
tree1 = new_list(tree, tree_maker(a,tree))
tree2 = new_list(tree1, tree_maker(b,tree1))
temp_mat1 = a
temp_mat2 = b
temp_lis = c
temp_tree = tree2
while (len(temp_mat2) != 3):
	result = out_ADM(temp_mat1,temp_lis)
	temp_mat1 = result[0]
	temp_mat2 = result[1]
	temp_lis = result[2]
	temp_tree = new_list(temp_tree, tree_maker(temp_mat2,temp_tree))
ot1 = str(temp_tree).replace("[", "(")
ot2 = ot1.replace("]",")")
ot3 = ot2.replace("'", "")
output = ot3+";"

##########################__OUTPUT__############################
print("Phylogenetic tree construction completed..."+"\n")
print("\n"+"Phylogenetic Tree Data:"+"\n")
print(output +"\n")
save_op = input("Save Tree [y/n]: ")
if save_op == "y":
	tree_nm = input("Enter the tree name: ")
	tree_name = "PhyloBit_Tree_"+ tree_nm + ".txt"
	save_tree = open(tree_name, "w")
	save_tree.write(output)
	save_tree.close()
	print("Tree Saved...")
