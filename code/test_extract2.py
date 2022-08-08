import csv
import numpy as np
import argparse

BGL_path = "../Wordlists/BristolNorms+GilhoolyLogie.csv"
WAR_path = "../Wordlists/Ratings_Warriner_et_al.csv"
feat_path = "./feats/"
# with open(BGL_path) as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     bngl_dict = {}
#     next(reader)
#     for row in reader:
#         if row[1]:
#             bngl_dict[row[1]]={'AoA':float(row[3]),'IMG':float(row[4]),'FAM':float(row[5])}
# with open(WAR_path) as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     warr_dict = {}
#
#     next(reader)
#     for row in reader:
#         if row[1]:
#             warr_dict[row[1]]={'V':float(row[2]),'A':float(row[5]),'D':float(row[8])}
bngl_dict = {}
warr_dict = {}
with open(BGL_path) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    for line in reader:
        if line[1]:
            bngl_dict[line[1]] = {
                'AoA': line[3],
                'IMG': line[4],
                'FAM': line[5]}
with open(WAR_path) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    for line in reader:
        if line[1]:
            warr_dict[line[1]] = {
                'V': line[2],
                'A': line[5],
                'D': line[8]}

# print(bngl_dict)
# print(warr_dict)
feats = np.zeros(29)
feat_path = "./feats/"
comment_class = "Alt"
comment_id = "c05275y"
index = 0
# with open(feat_path + comment_class + "_IDs.txt", "r") as file:
#     for i, line in enumerate(file):
#         if line == comment_id+"\n":
#             index = i
#             print(line)
#             break
file = open(feat_path + comment_class + "_IDs.txt").read().split("\n")
# for i, line in enumerate(file):
#     if line == comment_id:
#         index = i
#         print(line)
#         break
# print(index)
index = file.index(comment_id)
print(index)

data = np.load(feat_path + comment_class + "_feats.dat.npy")
feats= np.append(feats, data[index])
# len(data[index]) #144
# print(feats)
# print(data[index])
# print(feats[29])
# print(len(feats))
# print(feats)
# np.savez_compressed("../sample_data/sample_feats.npz", array1=array1, array2=array2)
sample_data = np.load("../sample_data/sample_feats.npz")
print(sample_data['arr_0'][0])

# def main(args):
#     print(args.a1_dir)
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Process each .')
#     parser.add_argument("-o", "--output",
#                         help="Directs the output to a filename of your choice",
#                         required=True)
#     parser.add_argument("-i", "--input",
#                         help="The input JSON file, preprocessed as in Task 1",
#                         required=True)
#     parser.add_argument("-p", "--a1_dir",
#                         help="Path to csc401 A1 directory. By default it is set to the cdf directory for the assignment.",
#                         default="/u/cs401/A1/")
#     args = parser.parse_args()
#     main(args)
