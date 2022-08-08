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

n = 4
C = [[1,    1,  1,  1],
     [2,    2,  2,  2],
     [3,    3,  3, 3],
     [4,    4,  4,  4]]
C = np.array(C)
sum_first_diagonal = sum(C[i][i] for i in range(n))
# sum_second_diagonal = sum(a[n-i-1][n-i-1] for i in range(n))
# print(str(sum_first_diagonal)+" "+str(sum_first_diagonal))
# print(sum_first_diagonal)
# print(np.sum(a))

print(sum_first_diagonal/np.sum(C))
recall = np.diag(C) / C.sum(axis=1)
precision = np.diag(C) / C.sum(axis=0)
print(recall)
print(precision)
print(f'\tPrecision: {[round(item, 4) for item in precision]}\n')
# Note: #1 gives normal list. #3 and mine gives np array

def accuracy(C):
    ''' Compute accuracy given Numpy array confusion matrix C. Returns a floating point value '''
    diagonal_sum = sum(C[i][i] for i in range(4))
    all_sum = sum(C[i][j] for i in range(4) for j in range(4))
    return diagonal_sum/all_sum

def recall(C):
    ''' Compute recall given Numpy array confusion matrix C. Returns a list of floating point values '''
    # TP / (TP+FP)
    # iterate (value over diagonal/ row)
    return C.diagonal()/C.sum(1)


def precision(C):
    ''' Compute precision given Numpy array confusion matrix C. Returns a list of floating point values '''
    # TP / (TP+FN)
    # iterate (value over diagonal/ column)
    return C.diagonal()/C.sum(0)

print(accuracy(C))
print(C.trace()/C.sum())
# print(C)
# print(C.flatten())
# print(f'\tConfusion Matrix: \n{C.flatten()}\n\n')

