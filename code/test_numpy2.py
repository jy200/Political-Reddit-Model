import numpy as np
from scipy.stats import ttest_rel
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import SelectKBest
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier

# tp_and_fn = cm.sum(1)
# tp_and_fp = cm.sum(0)
# tp = cm.diagonal()
#
# precision = tp / tp_and_fp
# recall = tp / tp_and_fn


results = np.zeros((5, 5))
# results[i][0] = i + 1  # classifier # starting from 1
# results[i][1] = accuracy(C)
# results[i][2] = recall(C)
# results[i][3] = precision(C)
# results[i][4] = C.flatten()

for i in range(5):
    results[i][0] = i

a = np.array([1,2,3,4])
# results[0][2] = a.flatten()
print(results)

#   test one line if condition
p_50 = [1,2,3,4]
p_5 = [0,0,0,0]
k_feat = 5
for k_feat in [5, 50]:
    p_values = [p_50, p_5][k_feat == 5]
    p_values = np.array(p_values)
    print(f'{k_feat} p-values: {[round(pval, 4) for pval in p_values]}\n')


C = np.append(p_50, p_5)
print(C)
# print(f'{k_feat} p-values: {[round(pval, 4) for pval in p_values]}\n')

def test_inside_loop():
    # test outer list + inner list appending
    list1 = [1, 2,3 ,4]
    list2 = [50,60,70,80]
    list3 = []
    list3.append(list1)
    list3.append(list2)
    print(list3)
    list3 = np.array(list3)
    list3.astype(np.float64)
    print(np.mean(list3, axis=1))

    S = ttest_rel(list1, list2)
    print(S.pvalue)

def test_pvalues():
    arrays = [[0.3599, 0.3509, 0.4424, 0.4554, 0.4782],
            [0.3785, 0.3599, 0.4466, 0.4426, 0.4824],
            [0.3612, 0.3586, 0.4466, 0.417, 0.4856],
            [0.3459, 0.3459, 0.4466, 0.465, 0.4871]]

    best = [0.3144, 0.345, 0.4445, 0.4441, 0.481]

    values = []
    for i in range(4):
        S = ttest_rel(arrays[i], best)
        values.append(S.pvalue)
    print(values)
