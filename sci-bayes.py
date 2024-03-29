from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
from sklearn import svm
from sklearn import tree
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import BernoulliNB
import numpy as np

training_document_list = []
training_labels_list = []
test_document_list = []
test_labels_list = []

def get_training_input():
    global training_data, training_labels
    training_data_name = get_file_name("Please enter the training data file name: ")
    training_data = open(training_data_name)
    if (training_data):
        print("Read successful")
    else:
        print("Error: Read Failure")
        exit(-1)
    training_labels_name = get_file_name("Please enter the training labels file name: ")
    training_labels = open(training_labels_name)
    if training_labels:
        print("Read successful")
    else:
        print("Error: Read Failure")
        exit(-1)
    for line in training_labels:
        training_labels_list.append(line)
    for line in training_data:
        training_document_list.append(line)


def get_test_input():
    test_data_name = get_file_name("Please enter the test data file name: ")
    test_data = open(test_data_name)
    if (test_data):
        print("Read successful")
    else:
        print("Error: Read Failure")
        exit(-1)
    test_labels_name = get_file_name("Please enter the test labels file name: ")
    test_labels = open(test_labels_name)
    if training_labels:
        print("Read successful")
    else:
        print("Error: Read Failure")
        exit(-1)
    for line1 in test_labels:
        test_labels_list.append(line1)
    for line2 in test_data:
        test_document_list.append(line2)

def get_file_name(prompt):
    return input(prompt)


if __name__ == '__main__':
    get_training_input()
    # get_test_input()

    # Create kFolds
    skf = StratifiedKFold(n_splits= 10)

    vectorizer = CountVectorizer(stop_words='english')
    train_features = vectorizer.fit_transform(training_document_list)
    # test_features = vectorizer.transform(test_document_list)

    train_labels = list(map(int, training_labels_list))
    train_labels_array = np.array(train_labels)

    # Convert lables to a list of ints (They are currently strings)
    # test_labels_list = list(map(int, test_labels_list))

    bern_bayes_auc = []
    bayes_auc = []
    svm_auc = []
    tree_auc = []
    sgd_auc = []


    count = 1


    bern_pred_total= []
    nb_pred_total = []
    svm_pred_total = []
    tree_pred_total = []
    stoch_pred_total = []
    true_results_total= []

    # KFolds Loop here:
    for train_index, test_index in skf.split(X= train_features, y= train_labels):
        X_train, X_test = train_features[train_index], train_features[test_index]
        y_train, y_test = train_labels_array[train_index], train_labels_array[test_index]

        true_results_total.extend(y_test)

        # Classifiers
        bern_nb = BernoulliNB()
        multi_nb = MultinomialNB()
        support_vec = svm.SVC(kernel='linear')
        tree_clf = tree.DecisionTreeClassifier()
        stoch_gd = SGDClassifier(loss="hinge", penalty="l2")

        # Fit the classifiers
        bern_nb.fit(X = X_train, y = y_train)
        multi_nb.fit(X = X_train, y = y_train)
        support_vec.fit(X = X_train, y = y_train)
        tree_clf.fit(X = X_train, y = y_train)
        stoch_gd.fit(X= X_train, y = y_train)

        # Make predictions
        bern_predictions = bern_nb.predict(X_test)
        nb_predictions = multi_nb.predict(X_test)
        svm_predictions = support_vec.predict(X_test)
        tree_predictions = tree_clf.predict(X_test)
        stoch_predictions = stoch_gd.predict(X_test)

        bern_pred_total.extend(bern_predictions)
        nb_pred_total.extend(nb_predictions)
        svm_pred_total.extend(svm_predictions)
        tree_pred_total.extend(tree_predictions)
        stoch_pred_total.extend(stoch_predictions)


        # Report accuracy
        print("\tEvaluating Fold #"+ count.__str__())
        count += 1


    print("---------------------  Results  ---------------------")
    print("\tBernoulli Naive Bayes Accuracy: " + str(metrics.accuracy_score(true_results_total, bern_pred_total)))
    fpr, tpr, thresholds = metrics.roc_curve(true_results_total, bern_pred_total, pos_label=1)
    print("\tBernoulli Naive Bayes AUC: "+ metrics.auc(fpr, tpr).__str__())
    print(metrics.classification_report(true_results_total,bern_pred_total))
    print("")

    print("\tMultinomial Naive Bayes Accuracy: " + str(metrics.accuracy_score(true_results_total, nb_pred_total)))
    fpr, tpr, thresholds = metrics.roc_curve(true_results_total, nb_pred_total, pos_label=1)
    print("\tMultinomial Naive Bayes AUC: " + metrics.auc(fpr, tpr).__str__())
    print(metrics.classification_report(true_results_total,nb_pred_total))
    print("")

    print("\tSVM Accuracy: " + str(metrics.accuracy_score(true_results_total, svm_pred_total)))
    fpr, tpr, thresholds = metrics.roc_curve(true_results_total, svm_pred_total, pos_label=1)
    print("\tSVM AUC: " + metrics.auc(fpr, tpr).__str__())
    print(metrics.classification_report(true_results_total,svm_pred_total))
    print("")

    print("\tDecision Tree Accuracy: " + str(metrics.accuracy_score(true_results_total, tree_pred_total)))
    fpr, tpr, thresholds = metrics.roc_curve(true_results_total, tree_pred_total, pos_label=1)
    print("\tDecision Tree AUC: " + metrics.auc(fpr, tpr).__str__())
    print(metrics.classification_report(true_results_total,tree_pred_total))
    print("")

    print("\tStochastic Gradient Descent Accuracy: " + str(metrics.accuracy_score(true_results_total, stoch_pred_total)))
    fpr, tpr, thresholds = metrics.roc_curve(true_results_total, stoch_pred_total, pos_label=1)
    print("\tStochastic Gradient Descent AUC: " + metrics.auc(fpr, tpr).__str__())
    print(metrics.classification_report(true_results_total,stoch_pred_total))
    print("")