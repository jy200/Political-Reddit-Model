import numpy as np
import argparse
import json
import re
import csv

# Provided wordlists.
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

def replacement(match):
    return match.group(1).lower()


def extract1(comment):
    ''' This function extracts features from a single comment

    Parameters:
        comment : string, the body of a comment (after preprocessing)

    Returns:
        feats : numpy Array, a 173-length vector of floating point features (only the first 29 are expected to be filled, here)
    '''
    # Extract features that rely on capitalization.
    # Lowercase the text in comment. Be careful not to lowercase the tags. (e.g. "Dog/NN" -> "dog/NN").
    # Extract features that do not rely on capitalization.
    # body_words = re.compile(r"(\w+|\W+)(?=/)").findall(comment)   # all words
    feats = np.zeros(173)
    feats[0] = len(re.findall("([A-Z]{3,})(?=/)", comment))     # All capital letters >= 3
    comment = re.sub(r"([A-Za-z]+)(?=/)", replacement, comment)  # convert comment to lower-case
    feats[1] = len(re.findall(r"\b("+'|'.join(FIRST_PERSON_PRONOUNS)+r")\b", comment))
    feats[2] = len(re.findall(r"\b(" + '|'.join(SECOND_PERSON_PRONOUNS) + r")\b", comment))
    feats[3] = len(re.findall(r"\b(" + '|'.join(THIRD_PERSON_PRONOUNS) + r")\b", comment))
    feats[4] = len(re.findall(r"\w/CC ", comment))
    feats[5] = len(re.findall(r"\w/VBD ", comment))
    feats[6] = len(re.findall(r"will/MD|go/VBG to/TO \w+/VB|go/VBG to/TO", comment))
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
        data = Left_feats
    elif comment_class == "Center":
        file = Center_ID
        data = Center_feats
    elif comment_class == "Right":
        file = Right_ID
        data = Right_feats
    elif comment_class == "Alt":
        file = Alt_ID
        data = Alt_feats
    index = file.index(comment_id)
    return np.append(feat[:29], data[index])    # returns modified array without affecting original


def main(args):
    # Declare necessary global variables here.
    global Alt_feats, Alt_ID, Right_feats, Right_ID, \
        Left_feats, Left_ID, Center_feats, Center_ID
    global BGL_path, WAR_path, bngl_dict, warr_dict
    BGL_path = args.a1_dir + "/../Wordlists/BristolNorms+GilhoolyLogie.csv"
    WAR_path = args.a1_dir + "/../Wordlists/Ratings_Warriner_et_al.csv"
    bngl_dict, warr_dict = {}, {}
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

    feat_path = args.a1_dir + "/feats/"
    Alt_feats = np.load(feat_path+'Alt_feats.dat.npy')
    Alt_ID = open(feat_path+'Alt_IDs.txt','r').read().split('\n')
    Right_feats = np.load(feat_path + 'Right_feats.dat.npy')
    Right_ID = open(feat_path + 'Right_IDs.txt', 'r').read().split('\n')
    Left_feats = np.load(feat_path + 'Left_feats.dat.npy')
    Left_ID = open(feat_path + 'Left_IDs.txt', 'r').read().split('\n')
    Center_feats = np.load(feat_path + 'Center_feats.dat.npy')
    Center_ID = open(feat_path + 'Center_IDs.txt', 'r').read().split('\n')

    # Load data
    data = json.load(open(args.input))
    feats = np.zeros((len(data), 173 + 1))

    # Call extract1 for each datatpoint to find the first 29 features.
    # Add these to feats.
    # Call extract2 for each feature vector to copy LIWC features (features 30-173)
    # into feats. (Note that these rely on each data point's class,
    # which is why we can't add them in extract1).

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
    np.savez_compressed(args.output, feats)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-o", "--output",
                        help="Directs the output to a filename of your choice",
                        required=True)
    parser.add_argument("-i", "--input",
                        help="The input JSON file, preprocessed as in Task 1",
                        required=True)
    parser.add_argument("-p", "--a1_dir",
                        help="Path to csc401 A1 directory. By default it is set to the cdf directory for the assignment.",
                        default="/u/cs401/A1/")
    args = parser.parse_args()

    main(args)

