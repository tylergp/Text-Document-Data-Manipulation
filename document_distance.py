# 6.100A Fall 2023
# Problem Set 3
# Name: Tyler Proctor
# Collaborators: N/A

"""
Description:
    Computes the similarity between two texts using two different metrics:
    (1) shared words, and (2) term frequency-inverse document
    frequency (TF-IDF).
"""

import string
import math
import re

### DO NOT MODIFY THIS FUNCTION
def load_file(filename):
    """
    Args:
        filename: string, name of file to read
    Returns:
        string, contains file contents
    """
    # print("Loading file %s" % filename)
    inFile = open(filename, 'r')
    line = inFile.read().strip()
    for char in string.punctuation:
        line = line.replace(char, "")
    inFile.close()
    return line.lower()


### Problem 1: Prep Data ###
def prep_data(input_text):
    """
    Args:
        input_text: string representation of text from file,
                    assume the string is made of lowercase characters
    Returns:
        list representation of input_text, where each word is a different element in the list
    """

    data_list = []
    temp_word = ""
    # iterate through length of input_text and use index i
    for i in range(len(input_text)):
        # check if string value at that index is a space, if so append the string that includes only characters to the data list created and reset string to repeat
        if not input_text[i].isalpha():
            if len(temp_word) > 0:
                data_list.append(temp_word)
            temp_word = ""
        # if not a space, add the text from the input at that index to the word creater
        else:
            temp_word += input_text[i]
    # add last word that doesn't have space after it
    data_list.append(temp_word)
    return data_list
    # pass


### Problem 2: Get Frequency ###
def get_frequencies(word_list):
    """
    Args:
        word_list: list of strings, all are made of lowercase characters
    Returns:
        dictionary that maps string:int where each string
        is a word in l and the corresponding int
        is the frequency of the word in l
    """
    word_frequency = {}
    for word in word_list:
        if word_frequency.__contains__(word) == False:
            frequency = 0
            for i in word_list:
                if word == i:
                    frequency += 1
            word_frequency.update({word: frequency})
    return word_frequency
    

    # pass


### Problem 3: Get Words Sorted by Frequency
def get_words_sorted_by_frequency(frequencies_dict):
    """
    Args:
        frequencies_dict: dictionary that maps a word to its frequency
    Returns:
        list of words sorted by decreasing frequency with ties broken
        by alphabetical order
    """
    frequencies_list = list(sorted(frequencies_dict.values(), reverse=True))
    keys_list = list(sorted(frequencies_dict.keys()))
    final_words_list = []
    # go through each sorted frequency value to find appropriate key and add to final words_list
    for i in frequencies_list:
        for j in keys_list:
            if frequencies_dict[j] == i:
                if final_words_list.__contains__(j) == False:
                        final_words_list.append(j)
    return final_words_list

    # pass


### Problem 4: Most Frequent Word(s) ###
def get_most_frequent_words(dict1, dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        dict1: frequency dictionary for one text
        dict2: frequency dictionary for another text
    Returns:
        list of the most frequent word(s) in the input dictionaries

    The most frequent word:
        * is based on the combined word frequencies across both dictionaries.
          If a word occurs in both dictionaries, consider the sum the
          frequencies as the combined word frequency.
        * need not be in both dictionaries, i.e it can be exclusively in
          dict1, dict2, or shared by dict1 and dict2.
    If multiple words are tied (i.e. share the same highest frequency),
    return an alphabetically ordered list of all these words.
    """
    combined_dict = {}
    final_dict = {"test": 0}
    for word in dict1:
        if word in dict2:
            combined_dict.update({word: dict1[word] + dict2[word]})
        else:
            combined_dict.update({word: dict1[word]})
    for leftWord in dict2:
        if not leftWord in dict1:
            combined_dict.update({leftWord: dict2[leftWord]})
    for allWord in combined_dict:
        if (combined_dict[allWord] > list(final_dict.values())[0]):
            del final_dict[list(final_dict)[0]]
            final_dict.update({allWord: combined_dict[allWord]})
    for x in combined_dict:
        if (combined_dict[x] == list(final_dict.values())[0]):
            final_dict.update({x: combined_dict[x]})

    return(sorted(final_dict))
    # pass


### Problem 5: Similarity ###
def calculate_similarity_score(dict1, dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        dict1: frequency dictionary of words of text1
        dict2: frequency dictionary of words of text2
    Returns:
        float, a number between 0 and 1, inclusive
        representing how similar the words/texts are to each other

        The difference in words/text frequencies = DIFF sums "frequencies"
        over all unique elements from dict1 and dict2 combined
        based on which of these three scenarios applies:
        * If an element occurs in dict1 and dict2 then
          get the difference in frequencies
        * If an element occurs only in dict1 then take the
          frequency from dict1
        * If an element occurs only in dict2 then take the
          frequency from dict2
         The total frequencies = ALL is calculated by summing
         all frequencies in both dict1 and dict2.
        Return 1-(DIFF/ALL) rounded to 2 decimal places
    """
    unique_words = []
    frequency_diff = 0
    frequency_total = 0
    similarity = 0.00

    # Find all the unique words for both dict1 and dict2
    for i in dict1:
        if not i in unique_words:
            unique_words.append(i)
    for j in dict2:
        if not j in unique_words:
            unique_words.append(j)

    # Iterate through all and see if they are in only one of the original dictionaries or both
    # Find DIFF sums for frequencies and find ALL for total frequencies
    for word in unique_words:
        if word in dict1 and word in dict2:
            frequency_diff += abs(dict1[word] - dict2[word])
            frequency_total += dict1[word] + dict2[word]
        elif word in dict1:
            frequency_diff += abs(dict1[word] - 0)
            frequency_total += dict1[word]
        elif word in dict2:
            frequency_diff += abs(0 - dict2[word])
            frequency_total += dict2[word]

    # Get float to two decimal places for 1-(DIFF/ALL)
    similarity = 1 - (frequency_diff/frequency_total)
    return round(similarity, 2)
    # pass


### Problem 6: Finding TF-IDF ###
def get_tf(text_file):
    """
    Args:
        text_file: name of file in the form of a string
    Returns:
        a dictionary mapping each word to its TF

    * TF is calculated as TF(i) = (number times word *i* appears
        in the document) / (total number of words in the document)
    * Think about how we can use get_frequencies from earlier
    """
    tF_dict = {}
    # Prep data from text_file passed in
    word_list = prep_data(load_file(text_file))

    # find total number of words in the doc
    total_words = len(word_list)

    # for each unique word, find total num of times its in list (use get_frequencies function from earlier)
    word_freq = get_frequencies(word_list)

    # for each unique word, calculate TF and put in dictionary
    for word in word_freq:
        tF = float(word_freq[word] / total_words)
        tF_dict.update({word: tF})
    # return dictionary
    return tF_dict
    # pass

def flatten(L):
    """
    L: a list
    Returns a copy of L, which is a flattened version of L
    """
    global counter
    if len(L) == 0:
        return []
    elif type(L[0]) == list:
        return flatten(L[0]) + flatten(L[1:])
    else:
        return [L[0]] + flatten(L[1:])


def get_idf(text_files):
    """
    Args:
        text_files: list of names of files, where each file name is a string
    Returns:
       a dictionary mapping each word to its IDF

    * IDF is calculated as IDF(i) = log_10(total number of documents / number of
    documents with word *i* in it), where log_10 is log base 10 and can be called
    with math.log10()
    """
    iDF_dict = {}
    unique_word_list = []
    word_list = []
    word_int_docs = {}
    # Find total num of documents & all words in all docs
    total_num_docs = len(text_files)
    for file in text_files:
        word_list.append(prep_data(load_file(file)))
    # for each unique word, Find num of docs w word in it
    for word in word_list:
        if not word in unique_word_list:
            unique_word_list.append(word)
    unique_word_list = flatten(unique_word_list)
    for word in unique_word_list:
        counter = 0
        for file in text_files:
            if word in prep_data(load_file(file)):
                counter += 1
        word_int_docs.update({word: counter})
    # for each unique word, Calculate IDF and add to dictionary
    for word in word_int_docs:
        iDF = float(math.log10(total_num_docs/word_int_docs[word]))
        iDF_dict.update({word: iDF})
    return iDF_dict
    # pass


def get_tfidf(text_file, text_files):
    """
    Args:
        text_file: name of file in the form of a string (used to calculate TF)
        text_files: list of names of files, where each file name is a string
        (used to calculate IDF)
    Returns:
       a sorted list of tuples (in increasing TF-IDF score), where each tuple is
       of the form (word, TF-IDF). In case of words with the same TF-IDF, the
       words should be sorted in increasing alphabetical order.

    * TF-IDF(i) = TF(i) * IDF(i)
    """
    tFIDF_list = []
    # Find TF dict for all unique words
    tF_dict = get_tf(text_file)
    # Find IDF dict for all unique words
    iDF_dict = get_idf(text_files)
    # Calculate TF-IDF for all unique words
    # List stores tuples for (word, TF-IDF)
    for word in tF_dict:
        tf_idf = tF_dict[word] * iDF_dict[word]
        tFIDF_list.append((word, tf_idf))
    # Sort list based on TF_IDF score and increasing alphabetical order
    tFIDF_list = sorted(tFIDF_list)
    tFIDF_list = sorted(tFIDF_list, key= lambda x: x[1])
    return tFIDF_list
    # pass


if __name__ == "__main__":
    # pass
    ##Uncomment the following lines to test your implementation
    ## Tests Problem 1: Prep Data
    test_directory = "tests/student_tests/"
    hello_world, hello_friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    world, friend = prep_data(hello_world), prep_data(hello_friend)
    # print(world) ## should print ['hello', 'world', 'hello', 'there']
    # print(friend) ## should print ['hello', 'friends']

    # ## Tests Problem 2: Get Frequencies
    world_word_freq = get_frequencies(world)
    friend_word_freq = get_frequencies(friend)
    # print(world_word_freq) ## should print {'hello': 2, 'world': 1, 'there': 1}
    # print(friend_word_freq) ## should print {'hello': 1, 'friends': 1}

    # ## Tests Problem 3: Get Words Sorted by Frequency
    world_words_sorted_by_freq = get_words_sorted_by_frequency(world_word_freq)
    friend_words_sorted_by_freq = get_words_sorted_by_frequency(friend_word_freq)
    # print(world_words_sorted_by_freq) ## should print ['hello', 'there', 'world']
    # print(friend_words_sorted_by_freq) ## should print ['friends', 'hello']

    # ## Tests Problem 4: Most Frequent Word(s)
    freq1, freq2 = {"hello":5, "world":1}, {"hello":1, "world":5}
    most_frequent = get_most_frequent_words(freq1, freq2)
    # print(most_frequent) ## should print ["hello", "world"]

    # ## Tests Problem 5: Similarity
    test_directory = "tests/student_tests/"
    hello_world, hello_friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    world, friend = prep_data(hello_world), prep_data(hello_friend)
    world_word_freq = get_frequencies(world)
    friend_word_freq = get_frequencies(friend)
    word_similarity = calculate_similarity_score(world_word_freq, friend_word_freq)
    # print(word_similarity)        # should print 0.33

    # ## Tests Problem 6: Find TF-IDF
    text_file = 'tests/student_tests/hello_world.txt'
    text_files = ['tests/student_tests/hello_world.txt', 'tests/student_tests/hello_friends.txt']
    tf = get_tf(text_file)
    idf = get_idf(text_files)
    tf_idf = get_tfidf(text_file, text_files)
    # print(tf) ## should print {'hello': 0.5, 'world': 0.25, 'there': 0.25}
    # print(idf) ## should print {'there': 0.3010299956639812, 'world': 0.3010299956639812, 'hello': 0.0, 'friends': 0.3010299956639812}
    # print(tf_idf) ## should print [('hello', 0.0), ('there', 0.0752574989159953), ('world', 0.0752574989159953)]