import math

training_document_list = []
training_labels_list = []
test_document_list = []
test_labels_list = []
top_trump_indicators = []
top_not_trump_indicators = []

class indicatorWord():
    def __init__(self, score, word):
        self.score = score
        self.word = word


def get_file_name(prompt):
    return input(prompt)


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


def extract_vocabulary(doc):
    vocabulary = []
    for line in training_document_list:
        for word in line.split():
            if word not in vocabulary:
                vocabulary.append(word)
    return vocabulary


def count_docs(document):
    count = 0
    for _ in training_document_list:
        count += 1
    return count


def count_docs_in_class(document, curr_class, training_labels):
    count = 0
    for line in training_labels_list:
        if int(line) == curr_class:
            count += 1
    return count


def count_docs_in_class_containing_term(c, t):
    loop_count = 0
    doc_count = 0
    for doc in training_document_list:
        if int(training_labels_list[loop_count]) == int(c):
            if t in doc:
                doc_count += 1
        loop_count += 1
    return doc_count


def concatenate_text_of_all_docs_in_class(c):
    concat_text = " "
    count = 0
    for line in training_labels_list:
        if int(line) == c:
            concat_text += training_document_list[count]
        count += 1
    return concat_text


def count_tokens_of_term(text,t):
    count = 0
    for curr in text.split():
        if t == curr:
            count += 1
    return count


'''
Primary function for training the Multinomial Model
'''
def train_multinomial_nb(c, document, training_labels):
    prior = []
    V = extract_vocabulary(document)
    N = count_docs(document)
    condprob = []
    for y in range(V.__len__()):
        condprob.append([0 for x in range(2)])
    c_count = 0
    for curr_class in c:
        n_c = count_docs_in_class(document, curr_class, training_labels)
        prior.append(n_c/N)
        text_c = concatenate_text_of_all_docs_in_class(curr_class)
        t_count = 0
        t_c_t = []

        for t in V:
            t_c_t.append(count_tokens_of_term(text_c, t))
            t_count += 1

        t_count = 0
        for t in V:
            summation = text_c.split().__len__()+ V.__len__()
            condprob[t_count][c_count] = float((t_c_t[t_count]+1)/(summation + 1))
            t_count += 1
        c_count += 1
    return V, prior, condprob


def extract_terms_from_doc(V, d):
    v_d = []
    for item in V:
        if item in d:
            # print(" \"" + item + "\" is in: " + d)
            v_d.append(item)
    return v_d


def extract_tokens_from_doc(V,d):
    tokens = []
    for item in d.split():
            if item in V:
                if item not in tokens:
                    tokens.append(item)
    return tokens


def apply_multinomial_nb(classes, V, prior, condprob, d):
    W = extract_tokens_from_doc(V,d)
    score = []
    c_count = 0
    for c in classes:
        score.append(math.log(prior[c_count]))
        t_count = 0
        for t in V:
            if c == 0:
                top_trump_indicators.append(indicatorWord(condprob[t_count][c_count], t))
            if c == 1:
                top_not_trump_indicators.append(indicatorWord(condprob[t_count][c_count], t))
            if t in W:
                #print("Adding the probability of: \"" + t + "\" Which is:  "+ condprob[t_count][c_count].__str__()+" at: condprob["+t_count.__str__()+"]["+c_count.__str__()+"]")
                score[c_count] += math.log(condprob[t_count][c_count])
            t_count += 1
        c_count += 1

    if score[0] > score[1]:
        return 0
    else:
        return 1


if __name__ == '__main__':
    get_training_input()
    classes = [0, 1]
    V, prior, condprob = train_multinomial_nb(classes, training_data, training_labels)
    get_test_input()
    d_count = 0
    correct_guesses = 0

    print("-----------------------------   Predictive Results:   ----------------------------")
    for d in test_document_list:
        guess = apply_multinomial_nb(classes, V, prior, condprob, d)
        if int(guess) == int(test_labels_list[d_count]):
            #print(" \"" + d[:-1] + "\" = " + guess.__str__())
            correct_guesses += 1
        else:
            pass
            #print(" \"" + d[:-1] + "\" = " + guess.__str__() + " X")
        d_count += 1


    print("-----------------------------   Conditional Probability   -----------------------")
    #print(condprob.__str__())
    top_not_trump_indicators.sort(key=lambda x: x.score)
    top_trump_indicators.sort(key=lambda x: x.score)

    print("\n\t Top 10 Trump Indicators\n")
    top_trump_indicators.__str__()
    for index in range(10):
        print("\t"+(index+1).__str__()+". "+top_trump_indicators[index].word +" -> " + top_trump_indicators[index].score.__str__())

    print("\n\t Top 10 Non-Trump Indicators\n")
    top_not_trump_indicators.__str__()
    for index in range(10):
        print("\t" + (index + 1).__str__() + ". " + top_not_trump_indicators[index].word + " -> " + top_not_trump_indicators[index].score.__str__())


    correct_percentage = (correct_guesses/test_labels_list.__len__())*100
    correct_percentage_string = correct_percentage.__str__()
    print("\n")
    print("-----------------------------------   Summary:   ----------------------------------")
    print("\t\t\t\tAccuracy: " + correct_guesses.__str__() + "/" + test_labels_list.__len__().__str__() + " (%" + correct_percentage_string[:4] + ")")
    print("-----------------------------------------------------------------------------------\n")

