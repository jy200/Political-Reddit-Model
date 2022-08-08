mine = [
    {
        "id": "c18y24m",
        "body": "forget/VB the/DT (/-LRB- very/RB valid/JJ )/-RRB- state/NN point/NN .../: you/PRP can/MD CHOOSE/VB not/RB to/TO drive/VB ./.\nbut/CC under/IN this/DT thing/NN ,/, you/PRP be/VBP require/VBN to/TO buy/VB a/DT private/JJ product/NN simply/RB by/IN be/VBG alive/JJ ./.\n",
        "cat": "Center"
    },
    {
        "id": "cbhkfn1",
        "body": "laugh/VB all/DT you/PRP want/VBP ,/, black/NNS have/VBP always/RB be/VBN well/JJR off/RP in/IN american/NNP than/IN in/IN africa/NNP ./.\nit/PRP be/VBD true/JJ in/IN the/DT day/NNS when/WRB jews/NNPS be/VBD bring/VBG the/DT slave/NNS to/IN the/DT US/NNP to/TO sell/VB ,/, and/CC it/PRP be/VBZ still/RB true/JJ today/NN ./.\n",
        "cat": "Right"
    },
    {
        "id": "c0fnog9",
        "body": "size/NN be/VBZ a/DT small/JJ part/NN of/IN a/DT fight/NN ./.\none/CD lucky/JJ punch/NN and/CC you/PRP could/MD be/VB incapacitate/VBN ,/, hospitalize/VBN even/RB kill/VBN ./.\nI/PRP have/VB see/VBN a/DT small/JJ guy/NN beat/VB down/RP a/DT 6'6/CD 280/CD lb/NN dude/NN ./.\nI/PRP be/VBP sure/JJ [/-LRB- gina/NNP curano/NNP ]/-RRB- (/-LRB- could/MD kill/VB or/CC seriously/RB injure/VB someone/NN with/IN a/DT strike/NN to/IN the/DT face/NN ./.\nshe/PRP s/VBZ tiny/JJ ./.\nsize/NN be/VBZ not/RB everything/NN ./.\nor/CC what/WP if/IN its/PRP$ a/DT fat/JJ girl/NN ?/.\neither/DT way/NN it/PRP come/VBZ down/RP to/IN this/DT my/PRP$ health/NN >/XX anyone/NN who/WP punch/VBZ me/PRP ./.\nI/PRP be/VBP go/VBG to/TO drop/VB them/PRP and/CC will/MD not/RB still/RB until/IN they/PRP stop/VBP or/CC can/MD not/RB continue/VB ./.\n",
        "cat": "Left"
    },
    {
        "id": "c0e4p0h",
        "body": "hehe/UH ,/, I/PRP second/VBD this/DT ./.\nI/PRP ADORE/VBP him/PRP ./.\n",
        "cat": "Alt"
    }
        ]

theirs = [
  {
    "id": "c18y24m",
    "body": "forget/VB the/DT (/-LRB- very/RB valid/JJ )/-RRB- state/NN point/NN .../: you/PRP can/MD CHOOSE/VB not/RB to/TO drive/VB ./.\nbut/CC under/IN this/DT thing/NN ,/, you/PRP be/VBP require/VBN to/TO buy/VB a/DT private/JJ product/NN simply/RB by/IN be/VBG alive/JJ ./.\n",
    "cat": "Center"
  },
  {
    "id": "cbhkfn1",
    "body": "laugh/VB all/DT you/PRP want/VBP ,/, black/NNS have/VBP always/RB be/VBN well/JJR off/RP in/IN american/NNP than/IN in/IN africa/NNP ./.\nit/PRP be/VBD true/JJ in/IN the/DT day/NNS when/WRB jews/NNPS be/VBD bring/VBG the/DT slave/NNS to/IN the/DT US/NNP to/TO sell/VB ,/, and/CC it/PRP be/VBZ still/RB true/JJ today/NN ./.\n",
    "cat": "Right"
  },
  {
    "id": "c0fnog9",
    "body": "size/NN be/VBZ a/DT small/JJ part/NN of/IN a/DT fight/NN ./.\none/CD lucky/JJ punch/NN and/CC you/PRP could/MD be/VB incapacitate/VBN ,/, hospitalize/VBN even/RB kill/VBN ./.\nI/PRP have/VB see/VBN a/DT small/JJ guy/NN beat/VB down/RP a/DT 6'6/CD 280/CD lb/NN dude/NN ./.\nI/PRP be/VBP sure/JJ [/-LRB- gina/NNP curano/NNP ]/-RRB- (/-LRB- could/MD kill/VB or/CC seriously/RB injure/VB someone/NN with/IN a/DT strike/NN to/IN the/DT face/NN ./.\nshe/PRP s/VBZ tiny/JJ ./.\nsize/NN be/VBZ not/RB everything/NN ./.\nor/CC what/WP if/IN its/PRP$ a/DT fat/JJ girl/NN ?/.\neither/DT way/NN it/PRP come/VBZ down/RP to/IN this/DT my/PRP$ health/NN >/XX anyone/NN who/WP punch/VBZ me/PRP ./.\nI/PRP be/VBP go/VBG to/TO drop/VB them/PRP and/CC will/MD not/RB still/RB until/IN they/PRP stop/VBP or/CC can/MD not/RB continue/VB ./.\n",
    "cat": "Left"
  },
  {
    "id": "c0e4p0h",
    "body": "hehe/UH ,/, I/PRP second/VBD this/DT ./.\nI/PRP ADORE/VBP him/PRP ./.\n",
    "cat": "Alt"
  }
]


categories = ['Alt', 'Center', 'Right', 'Left']
for i in range(4):
    sentence_mine = mine[i]['body'].split("\n")
    sentence_theirs = theirs[i]['body'].split("\n")
    for j, sentence in enumerate(sentence_mine):
        if sentence_mine[j] != sentence_theirs[j]:
            print(j)
            print(sentence_mine[j])
            print(sentence_mine[j])
            print(sentence_theirs[j])




def first_difference(str1, str2):
    for a, b in zip(str1, str2):
        if a != b:
            return a+b

# print(mine[2]['body'])
# print(theirs[2]['body'])
# print(first_difference(mine[2], theirs[2]))
# print(first_difference("hello", "lelloe"))
