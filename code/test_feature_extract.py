import sys
import argparse
import os
import json
import re
import spacy
import html
import numpy as np
import string
# nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
# sentencizer = nlp.create_pipe("sentencizer")
# nlp.add_pipe(sentencizer)


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

print(
    "I KNOW WORDS. I HAVE THE BEST WORDS. I know words. I have the best words. and The Man")
modComm = "I/PRP KNOW/VBP WORDS/NNP ./.\nI/PRP HAVE/VBP THE/DT GOOD/JJR WORD/NNS ./.\nI/PRP know/VBP word/NNS ./.\nI/PRP have/VBP the/DT good/JJS word/NNS ./.\nand/CC the/DT man/NN\n"
print(modComm)
# feat1count = len(re.findall(r'[A-Z][A-Z][A-Z]+/', modComm)) # includes slash
all_word = re.compile(r"(\w+|\s+)(?=/)").findall(modComm)    # list of all words
# all_tag = re.compile(r"(?=\w+|\W+)/(\w+|-\w+-)").findall(modComm)    # includes dashes (i dont think this a thing)
# all_tag = re.compile(r"(?=\w+|\W+)/(\w+|.)").findall(modComm)
print(all_word)
# print(all_tag)



feat1 = re.findall("([A-Z]{3,})(?=/)", modComm)
feat1count = len(feat1)
# print(feat1)
# print(feat1count)





modComm = re.sub(r"([A-Za-z]+)(?=/)", replacement, modComm)  # lower case comment
"""
    feats[1] = len(re.findall(r'\b(' + r'|'.join(FIRST_PERSON_PRONOUNS) + r')\b', comment))
    feats[2] = len(re.findall(r'\b(' + r'|'.join(SECOND_PERSON_PRONOUNS) + r')\b', comment))
    feats[3] = len(re.findall(r'\b(' + r'|'.join(THIRD_PERSON_PRONOUNS) + r')\b', comment))
"""
# test = re.compile(r'\b(' + r'|'.join(FIRST_PERSON_PRONOUNS) + r')\b').findall(modComm)
# print(test)
# test2 = re.findall(r"(?=("+'|'.join(FIRST_PERSON_PRONOUNS)+r"))", modComm)
# print(test2)


def test_first_half():
    featcc = len(re.findall("/CC ", modComm))
    print(featcc)

    test = "go/VBG to/TO ./.\nI/PRP be/VBP go/VBG to/TO beat/VB you/PRP up/RP ./.\nYou/PRP be/VBP go/VBG to/TO die/VB ./.\n"
    future = len(re.findall(r"will/MD|shall/MD|go/VBG to/TO \w+/VB|go/VBG to/TO", test))
    print(future)

    test2 = "//SYM ////NNP $/$ $/$ $/$ $/$ #/$ #/NN .../NFP ,/, ,/, :/: :/: (/-LRB- (/-LRB- )/-RRB- )/-RRB- )/-RRB- ''/'' `/'' `/''\n"
    # print(len(re.findall('(?:^|\s)[%s]{2,}/\S' % re.escape(string.punctuation), test2)))
    print(len(re.findall(r"[^\w\s]{2,}/", test2)))  # should be 3, which it is

    test_wh = re.findall(r"\w/(WDT|WP\$|WP|WRB)", "whose/WP$ watch/NN be/VBZ that/DT ?/.\n")
    print(len(test_wh))

    test_slang = re.findall(r"(?=("+'|'.join(SLANG)+r"))", "hello. I will smh tbh. Never before have I lmfao lmao\n")
    print(len(test_slang))


def sentence_length(comment):
    sentences = comment.split("\n")
    len_sentence = 0
    len_tokens = 0
    all_token_no_punct = re.compile(r"(\w+|\s+)(?=/)").findall(comment)
    for line in sentences:
        len_sentence += len(line.split())
    for token in all_token_no_punct:
        len_tokens += len(token)
    print(sentences)
    sentence_length = comment.count("\n")
    a = len_sentence / sentence_length
    b = len_tokens/len(all_token_no_punct)
    c = sentence_length
    print(a)
    print(b)
    print(c)
sentence_length(modComm)
