import sys
import argparse
import os
import json
import re
import spacy
import html

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)


def tag(modComm):
    modComm = re.sub(r"[^\S ]+", " ", modComm)
    modComm = html.unescape(modComm)
    modComm = re.sub(r"(http|www)\S+", "", modComm)
    modComm = re.sub(r" +", " ", modComm)

    # print(modComm)
    doc = nlp(modComm)
    temp = ""
    for sent in doc.sents:
        for token in sent:
            # print(token)
            if token.lemma_[0] == "-" and token.text[0] != "-":
                if token.text.isupper():
                    temp += token.text.upper()
                else:
                    temp += token.text.lower()
            else:
                if token.text.isupper():
                    temp += token.lemma_.upper()
                else:
                    # print(token.lemma_)
                    temp += token.lemma_.lower()
                    # print(temp)
            temp += "/" + token.tag_ + " "
        temp = temp[:-1]
        temp += "\\n"
    modComm = temp
    return modComm

# print(tag("I KNOW WORDS. I HAVE THE BEST WORDS. I know words. I have the best words. and The Man will"))
# print(tag("/ /// $$$$ ## ... ,, :: (( ))) "" '' ``"))
# print(tag("smh fwb lmfao lmao lms tbh"))

# print(tag("brother"))
# print(tag("hi\n                            , brother. How are you doing, cousin?"))
# print(tag("It works just fine for me.  \n\nI have used UD's product"))
