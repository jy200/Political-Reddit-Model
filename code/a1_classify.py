import argparse
import os
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
from sklearn.model_selection import KFold

# set the random state for reproducibility
import numpy as np
np.random.seed(401)

SGD = SGDClassifier()
GAUSS = GaussianNB()
RF = RandomForestClassifier(max_depth=5, n_estimators=10)
MLP = MLPClassifier(alpha=0.05)
ADA = AdaBoostClassifier()
classifiers = [SGD, GAUSS, RF, MLP, ADA]


def accuracy(C):
    ''' Compute accuracy given Numpy array confusion matrix C. Returns a floating point value '''
    # sum of diagonal values / total sum
    return C.trace()/C.sum()


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


def class31(output_dir, X_train, X_test, y_train, y_test):
    ''' This function performs experiment 3.1

    Parameters
       output_dir: path of directory to write output to
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes

    Returns:
       i: int, the index of the supposed best classifier
    '''
    names = ["SGDClassifier", "GaussianNB", "RandomForestClassifier",
             "MLPClassifier", "AdaBoostClassifier"]
    accuracy_list = []

    with open(f"{output_dir}/a1_3.1.txt", "w") as outf:
        # For each classifier, compute results and write the following output:
        for i, classifier in enumerate(classifiers):
            classifier.fit(X_train, y_train)
            y_predict = classifier.predict(X_test)
            C = confusion_matrix(y_test, y_predict)
            acc_value = accuracy(C)
            accuracy_list.append(acc_value)
            outf.write(f'Results for {names[i]}:\n')  # Classifier name
            outf.write(f'\tAccuracy: {acc_value:.4f}\n')
            outf.write(f'\tRecall: {[round(item, 4) for item in recall(C)]}\n')
            outf.write(f'\tPrecision: {[round(item, 4) for item in precision(C)]}\n')
            outf.write(f'\tConfusion Matrix: \n{C}\n\n')
    # print("3.1 accuracy list:")
    # print(accuracy_list)
    max_acc = max(accuracy_list)
    iBest = accuracy_list.index(max_acc)
    return iBest


def class32(output_dir, X_train, X_test, y_train, y_test, iBest):
    ''' This function performs experiment 3.2

    Parameters:
       output_dir: path of directory to write output to
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes
       iBest: int, the index of the supposed best classifier (from task 3.1)

    Returns:
       X_1k: numPy array, just 1K rows of X_train
       y_1k: numPy array, just 1K rows of y_train
   '''
    classifier = classifiers[iBest]  # best classifier
    accuracyList = []
    sample_sizes = [1000, 5000, 10000, 15000, 20000]
    for i in sample_sizes:
        X_train_data = X_train[:i]
        y_train_label = y_train[:i]
        classifier.fit(X_train_data, y_train_label)
        y_predict = classifier.predict(X_test)
        c = confusion_matrix(y_test, y_predict)
        accuracyList.append(accuracy(c))
    with open(f"{output_dir}/a1_3.2.txt", "w") as outf:
        # For each number of training examples, compute results and write
        # the following output:
        #     outf.write(f'{num_train}: {accuracy:.4f}\n'))
        for i in range(5):
            outf.write(f'{sample_sizes[i]}: {accuracyList[i]:.4f}\n')

    X_1k = X_train[:1000]
    y_1k = y_train[:1000]
    return (X_1k, y_1k)


def class33(output_dir, X_train, X_test, y_train, y_test, i, X_1k, y_1k):
    ''' This function performs experiment 3.3

    Parameters:
       output_dir: path of directory to write output to
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes
       i: int, the index of the supposed best classifier (from task 3.1)
       X_1k: numPy array, just 1K rows of X_train (from task 3.2)
       y_1k: numPy array, just 1K rows of y_train (from task 3.2)
    '''
    classifier = classifiers[i] # best classifier
    # 32k set
    selector1 = SelectKBest(f_classif, k=5)
    X_new1 = selector1.fit_transform(X_train, y_train)
    pp1 = sorted(selector1.pvalues_)  # p values for 32k @ k = 5
    top_5 = selector1.get_support(indices=True)  # 32k, top 5 feature indices
    classifier.fit(X_new1, y_train)
    y_predict = classifier.predict(selector1.transform(X_test))
    C1 = confusion_matrix(y_test, y_predict)
    accuracy_full = accuracy(C1)

    selector2 = SelectKBest(f_classif, k=50)
    selector2.fit_transform(X_train, y_train)
    pp2 = sorted(selector2.pvalues_)  # p values for 32k @ k = 50

    # 1k set
    selector3 = SelectKBest(f_classif, k=5)
    X_new3 = selector3.fit_transform(X_1k, y_1k)
    top_5_1k = selector3.get_support(indices=True)  # 1k, top 5 feature indices
    classifier.fit(X_new3, y_1k)
    y_predict = classifier.predict(selector3.transform(X_test))
    C2 = confusion_matrix(y_test, y_predict)
    accuracy_1k = accuracy(C2)

    feature_intersection = np.intersect1d(top_5_1k, top_5)  # feature intersection
    with open(f"{output_dir}/a1_3.3.txt", "w") as outf:
        # Prepare the variables with corresponding names, then uncomment
        # this, so it writes them to outf.

        # for each number of features k_feat, write the p-values for
        # that number of features:
            # outf.write(f'{k_feat} p-values: {[format(pval) for pval in p_values]}\n')
        for k_feat in [5, 50]:
            p_values = [pp1, pp2][k_feat == 5]
            outf.write(f'{k_feat} p-values: {[format(pval) for pval in p_values[:k_feat]]}\n')

        outf.write(f'Accuracy for 1k: {accuracy_1k:.4f}\n')
        outf.write(f'Accuracy for full dataset: {accuracy_full:.4f}\n')
        outf.write(f'Chosen feature intersection: {feature_intersection}\n')    # intersection indices
        outf.write(f'Top-5 at higher: {top_5}\n')   # top 5 indices for 32k set


def class34(output_dir, X_train, X_test, y_train, y_test, i):
    ''' This function performs experiment 3.4

    Parameters
       output_dir: path of directory to write output to
       X_train: NumPy array, with the selected training features
       X_test: NumPy array, with the selected testing features
       y_train: NumPy array, with the selected training classes
       y_test: NumPy array, with the selected testing classes
       i: int, the index of the supposed best classifier (from task 3.1)
        '''
    kf = KFold(n_splits=5, shuffle=True)
    accuracy_list = []
    X2 = np.append(X_train, X_test, axis=0)
    y2 = np.append(y_train, y_test)
    for train_index, test_index in kf.split(X2): # perform 5-fold cross validation
        fold_accuracy = []
        X2_train, X2_test = X2[train_index], X2[test_index]
        y2_train, y2_test = y2[train_index], y2[test_index]
        for index in range(5):
            classifier = classifiers[index]
            classifier.fit(X2_train, y2_train)
            y_predict = classifier.predict(X2_test)
            C = confusion_matrix(y2_test, y_predict)
            fold_accuracy.append(accuracy(C))
        accuracy_list.append(fold_accuracy)

    accuracy_list = np.array(accuracy_list)
    p_values = []
    for c in range(5):
        if i == c:
            continue
        S = ttest_rel(accuracy_list[c], accuracy_list[i])
        p_values.append(S.pvalue)

    with open(f"{output_dir}/a1_3.4.txt", "w") as outf:
        # Prepare kfold_accuracies, then uncomment this, so it writes them to outf.
        # for each fold:
        #     outf.write(f'Kfold Accuracies: {[round(acc, 4) for acc in kfold_accuracies]}\n')
        # outf.write(f'p-values: {[round(pval, 4) for pval in p_values]}\n')
        for c in range(5):
            # kfold_accuracies = np.mean(accuracy_list, axis=1)   # np array of mean accuracies
            kfold_accuracies = accuracy_list[c]
            outf.write(f'Kfold Accuracies: {[round(acc, 4) for acc in kfold_accuracies]}\n')
        outf.write(f'p-values: {[round(pval, 4) for pval in p_values]}\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="the input npz file from Task 2", required=True)
    parser.add_argument(
        "-o", "--output_dir",
        help="The directory to write a1_3.X.txt files to.",
        default=os.path.dirname(os.path.dirname(__file__)))
    args = parser.parse_args()

    # load data and split into train and test.
    # complete each classification experiment, in sequence.
    data = np.load(args.input)['arr_0']
    X = data[:, :-1]  # first 173
    y = data[:, -1]    # 174 label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    output = args.output_dir

    # part 1
    iBest = class31(output, X_train, X_test, y_train, y_test)
    # print("best classifier is "+str(iBest))

    # part 2
    (X_1k, y_1k) = class32(output, X_train, X_test, y_train, y_test, iBest)
    # part 3
    class33(output, X_train, X_test, y_train, y_test, iBest, X_1k, y_1k)

    # part 4
    class34(output, X_train, X_test, y_train, y_test, iBest)
