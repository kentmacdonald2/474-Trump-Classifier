from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics

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
    get_test_input()

    vectorizer = CountVectorizer(stop_words='english')
    train_features = vectorizer.fit_transform(training_document_list)
    test_features = vectorizer.transform(test_document_list)

    nb = MultinomialNB()

    #Convert lables to a list of ints (They are currently strings)
    training_labels_list = list(map(int,training_labels_list))
    test_labels_list = list(map(int,test_labels_list))

    nb.fit(X = train_features, y = training_labels_list)

    predictions = nb.predict(test_features)

    fpr, tpr, thresholds = metrics.roc_curve(test_labels_list, predictions, pos_label=1)

    print("Accuracy: " + str(metrics.accuracy_score(test_labels_list, predictions)))
    print(metrics.confusion_matrix(test_labels_list, predictions))
    print("Multinomial naive bayes AUC: {0}".format(metrics.auc(fpr, tpr)))
