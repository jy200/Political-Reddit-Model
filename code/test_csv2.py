import csv
import string
import numpy as np
import argparse
import re
import json
import sys

BGL_path = "../Wordlists/BristolNorms+GilhoolyLogie.csv"
WAR_path = "../Wordlists/Ratings_Warriner_et_al.csv"
feat_path = "./feats/"
bngl_dict = {}
warr_dict = {}
data = json.load(open("./sample_out.json"))
feats = np.zeros((len(data), 173 + 1))
def replacement(match):
    return match.group(1).lower()
FIRST_PERSON_PRONOUNS = {
    'i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours'}
SECOND_PERSON_PRONOUNS = {
    'you', 'your', 'yours', 'u', 'ur', 'urs'}
THIRD_PERSON_PRONOUNS = {
    'he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them',
    'their', 'theirs'}
SLANG = {
    'smh', 'fwb', 'lmfao', 'lmao', 'lms', 'tbh', 'rofl', 'wtf', 'bff',
    'wyd', 'lylc', 'brb', 'atm', 'imao', 'sml', 'btw', 'bw', 'imho', 'fyi',
    'ppl', 'sob', 'ttyl', 'imo', 'ltr', 'thx', 'kk', 'omg', 'omfg', 'ttys',
    'afn', 'bbs', 'cya', 'ez', 'f2f', 'gtr', 'ic', 'jk', 'k', 'ly', 'ya',
    'nm', 'np', 'plz', 'ru', 'so', 'tc', 'tmi', 'ym', 'ur', 'u', 'sol', 'fml'}


with open(BGL_path) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    for line in reader:
        if line[1]:
            bngl_dict[line[1]] = {
                'AoA': float(line[3]),
                'IMG': float(line[4]),
                'FAM': float(line[5])}
with open(WAR_path) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    for line in reader:
        if line[1]:
            warr_dict[line[1]] = {
                'V': float(line[2]),
                'A': float(line[5]),
                'D': float(line[8])}

def extract1(comment):
    ''' This function extracts features from a single comment

    Parameters:
        comment : string, the body of a comment (after preprocessing)

    Returns:
        feats : numpy Array, a 173-length vector of floating point features (only the first 29 are expected to be filled, here)
    '''
    # TODO: Extract features that rely on capitalization.
    # TODO: Lowercase the text in comment. Be careful not to lowercase the tags. (e.g. "Dog/NN" -> "dog/NN").
    # TODO: Extract features that do not rely on capitalization.
    # body_words = re.compile(r"(\w+|\W+)(?=/)").findall(comment)   # all words
    feats = np.zeros(173)
    feats[0] = len(re.findall("([A-Z]{3,})(?=/)", comment))     # All capital letters >= 3
    comment = re.sub(r"([A-Za-z]+)(?=/)", replacement, comment)  # convert comment to lower-case
    feats[1] = len(re.findall(r"\b("+'|'.join(FIRST_PERSON_PRONOUNS)+r")\b", comment))
    feats[2] = len(re.findall(r"\b(" + '|'.join(SECOND_PERSON_PRONOUNS) + r")\b", comment))
    feats[3] = len(re.findall(r"\b(" + '|'.join(THIRD_PERSON_PRONOUNS) + r")\b", comment))
    feats[4] = len(re.findall(r"\w/CC ", comment))
    feats[5] = len(re.findall(r"\w/VBD ", comment))
    feats[6] = len(re.findall(r"will/MD|shall/MD|go/VBG to/TO \w+/VB|go/VBG to/TO|gonna/", comment))
    feats[7] = len(re.findall(r",/, ", comment))
    feats[8] = len(re.findall(r"[^\w\s]{2,}/", comment))
    feats[9] = len(re.findall(r"\w/(NNS|NN) ", comment))
    feats[10] = len(re.findall(r"\w/(NNPS|NNP) ", comment))
    feats[11] = len(re.findall(r"\w/(RBS|RBR|RB) ", comment))
    feats[12] = len(re.findall(r"\w/(WDT|WP\$|WP|WRB) ", comment))
    feats[13] = len(re.findall(r"\b("+'|'.join(SLANG)+r")\b", comment))
    sentences = comment.split("\n")
    sentence_length = comment.count("\n")
    len_sentence = 0
    len_tokens = 0
    all_token_no_punct = re.compile(r"(\w+|\s+)(?=/)").findall(comment)
    for line in sentences:
        len_sentence += len(line.split())
    if sentence_length == 0:
        len_sentence = 0
    else:
        len_sentence = len_sentence / sentence_length
    for token in all_token_no_punct:
        len_tokens += len(token)
    if len(all_token_no_punct) == 0:
        len_tokens = 0
    else:
        len_tokens = len_tokens / len(all_token_no_punct)
    feats[14] = len_sentence
    feats[15] = len_tokens
    feats[16] = sentence_length

    AoA, IMG, FAM, V, D, A = [], [], [], [], [], []
    for token in all_token_no_punct:
        if token in bngl_dict.keys():
            AoA.append(bngl_dict[token]['AoA'])
            IMG.append(bngl_dict[token]['IMG'])
            FAM.append(bngl_dict[token]['FAM'])
        if token in warr_dict.keys():
            V.append(warr_dict[token]['V'])
            A.append(warr_dict[token]['A'])
            D.append(warr_dict[token]['D'])
    AoA = np.array(AoA)
    IMG = np.array(IMG)
    FAM = np.array(FAM)
    V = np.array(V)
    A = np.array(A)
    D = np.array(D)
    if len(AoA) > 0:    # prevent 0 errors
        feats[17] = np.mean(AoA)
        feats[20] = np.std(AoA)
    if len(IMG) > 0:
        feats[18] = np.mean(IMG)
        feats[21] = np.std(IMG)
    if len(FAM) > 0:
        feats[19] = np.mean(FAM)
        feats[22] = np.std(FAM)
    if len(V) > 0:
        feats[23] = np.mean(V)
        feats[26] = np.std(V)
    if len(A) > 0:
        feats[24] = np.mean(A)
        feats[27] = np.std(A)
    if len(D) > 0:
        feats[25] = np.mean(D)
        feats[28] = np.std(D)
    return feats


def extract2(feat, comment_class, comment_id):
    ''' This function adds features 30-173 for a single comment.

    Parameters:
        feat: np.array of length 173
        comment_class: str in {"Alt", "Center", "Left", "Right"}
        comment_id: int indicating the id of a comment

    Returns:
        feat : numpy Array, a 173-length vector of floating point features (this
        function adds feature 30-173). This should be a modified version of
        the parameter feats.
    '''
    file = None
    data = None
    if comment_class == "Left":
        file = Left_ID
        data = Left_data
    elif comment_class == "Center":
        file = Center_ID
        data = Center_data
    elif comment_class == "Right":
        file = Right_ID
        data = Right_data
    elif comment_class == "Alt":
        file = Alt_ID
        data = Alt_data
    index = file.index(comment_id)
    return np.append(feat[:29], data[index])    # returns modified array without affecting original


feat_path = "./feats/"
Alt_data = np.load(feat_path+'Alt_feats.dat.npy')
Alt_ID = open(feat_path+'Alt_IDs.txt','r').read().split('\n')

Right_data = np.load(feat_path + 'Right_feats.dat.npy')
Right_ID = open(feat_path + 'Right_IDs.txt', 'r').read().split('\n')

Left_data = np.load(feat_path + 'Left_feats.dat.npy')
Left_ID = open(feat_path + 'Left_IDs.txt', 'r').read().split('\n')

Center_data = np.load(feat_path + 'Center_feats.dat.npy')
Center_ID = open(feat_path + 'Center_IDs.txt', 'r').read().split('\n')
# np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
sample_data = np.load("../sample_data/sample_feats.npz")
# for i in range(len(data)):
#     feats[i][:-1] = extract1(data[i]["body"])
    # temp = np.zeros(173)
    # if data[i]["cat"] == "Left":
    #     feats[i][29:-1] = extract2(temp, "Left", data[i]["id"])
    #     feats[i][-1] = 0
    # if data[i]["cat"] == "Center":
    #     # feats[i] = np.append(extract2(feats[i], "Center", data[i]["id"]), np.zeros(1))
    #     feats[i][:-1] = extract2(feats[i][:-1], "Center", data[i]["id"])
    #     feats[i][-1] = 1
    # elif data[i]["cat"] == "Right":
    #     feats[i][29:-1] = extract2(temp, "Right", data[i]["id"])
    #     feats[i][-1] = 2
    # elif data[i]["cat"] == "Alt":
    #     feats[i][29:-1] = extract2(temp, "Alt", data[i]["id"])
    #     feats[i][-1] = 3
for i in range(len(data)):
    feats[i][:-1] = extract1(data[i]["body"])
    if data[i]["cat"] == "Left":
        feats[i][:-1] = extract2(feats[i][:-1], "Left", data[i]["id"])
        feats[i][-1] = 0
    elif data[i]["cat"] == "Center":
        feats[i][:-1] = extract2(feats[i][:-1], "Center", data[i]["id"])
        feats[i][-1] = 1
    elif data[i]["cat"] == "Right":
        feats[i][:-1] = extract2(feats[i][:-1], "Right", data[i]["id"])
        feats[i][-1] = 2
    elif data[i]["cat"] == "Alt":
        feats[i][:-1] = extract2(feats[i][:-1], "Alt", data[i]["id"])
        feats[i][-1] = 3
# index = Center_ID.index("c18y24m")
# feats[0][29:-1] = Center_data[index]
for i in range(4):
    for c in range(0,174):
        # print(f"Index {c}: {feats[i][c]} {sample_data['arr_0'][i][c]}")
        if feats[i][c] != sample_data['arr_0'][i][c]:
            print(f"feat[{c}]: {feats[i][c]} {sample_data['arr_0'][i][c]}")
    print("***********************************************")


def test_feat15():
    all_token_no_punct = ['size', 'be', 'a', 'small', 'part', 'of', 'a', 'fight', 'one', 'lucky',
     'punch', 'and', 'you', 'could', 'be', 'incapacitate', 'hospitalize',
     'even', 'kill', 'i', 'have', 'see', 'a', 'small', 'guy', 'beat', 'down',
     'a', '6', '280', 'lb', 'dude', 'i', 'be', 'sure', 'gina', 'curano',
     'could', 'kill', 'or', 'seriously', 'injure', 'someone', 'with', 'a',
     'strike', 'to', 'the', 'face', 'she', 's', 'tiny', 'size', 'be', 'not',
     'everything', 'or', 'what', 'if', 'its', 'a', 'fat', 'girl', 'either',
     'way', 'it', 'come', 'down', 'to', 'this', 'my', 'health', 'anyone', 'who',
     'punch', 'me', 'i', 'be', 'go', 'to', 'drop', 'them', 'and', 'will', 'not',
     'still', 'until', 'they', 'stop', 'or', 'can', 'not', 'continue']
    len_tokens = 0
    for token in all_token_no_punct:
        len_tokens += len(token)
    if len(all_token_no_punct) == 0:
        len_tokens = 0
    else:
        len_tokens = len_tokens / len(all_token_no_punct)
    print(len_tokens)

def test_2():
    comment = "size/NN be/VBZ a/DT small/JJ part/NN of/IN a/DT fight/NN ./.\none/CD lucky/JJ punch/NN and/CC you/PRP could/MD be/VB incapacitate/VBN ,/, hospitalize/VBN even/RB kill/VBN ./.\nI/PRP have/VB see/VBN a/DT small/JJ guy/NN beat/VB down/RP a/DT 6'6/CD 280/CD lb/NN dude/NN ./.\nI/PRP be/VBP sure/JJ [/-LRB- gina/NNP curano/NNP ]/-RRB- (/-LRB- could/MD kill/VB or/CC seriously/RB injure/VB someone/NN with/IN a/DT strike/NN to/IN the/DT face/NN ./.\nshe/PRP s/VBZ tiny/JJ ./.\nsize/NN be/VBZ not/RB everything/NN ./.\nor/CC what/WP if/IN its/PRP$ a/DT fat/JJ girl/NN ?/.\neither/DT way/NN it/PRP come/VBZ down/RP to/IN this/DT my/PRP$ health/NN >/XX anyone/NN who/WP punch/VBZ me/PRP ./.\nI/PRP be/VBP go/VBG to/TO drop/VB them/PRP and/CC will/MD not/RB still/RB until/IN they/PRP stop/VBP or/CC can/MD not/RB continue/VB ./.\n"
    comment2 = ">/"
    all_token_no_punct = re.compile(r"(\w+|\s+)(?=/)").findall(comment)
    print(all_token_no_punct)
    len_tokens = 0
    for token in all_token_no_punct:
        len_tokens += len(token)
    if len(all_token_no_punct) == 0:
        len_tokens = 0
    else:
        len_tokens += 2
        len_tokens = len_tokens / len(all_token_no_punct)
    print(len_tokens)

test_feat15()
# test_2()
