# Name: Xinyun Shen
# uniqname: xinyun

import re
import porterStemmer
import sys
import os

def removeSGML(input):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', input)
    return cleantext

def tokenizeText(input):
    input = input.lower()
    # replace 'm to am
    input = input.replace("'m ", " am")

    # replace 's to @'s@ for easy split
    input = input.replace("'s ", "@'s@")
    #replace s'
    # Sundays' ->["Sunday","s'"]
    input = input.replace("s’", "@s’@")

    # replace all the preiode to @ (only when preiod at the end of the words)
    # the period in the paragraph
    # input = input.replace(". ", "@.@")
    # the period at the end of the paragraph
    # for example data. ->data@.@
    # 170. -> 170@.@
    # 0.50 -> 0.50
    regex = r"([a-z][.])"
    subst = r'\1@'
    input = re.sub(regex, subst, input, 0, re.MULTILINE)
    input = input.replace(".@", "@.@")

    regex = r"([0-9][.]$)"
    subst = r'\1@'
    input = re.sub(regex, subst, input, 0, re.MULTILINE)
    input = input.replace(".@", "@.@")

    # replace all the / begin/end which is not in the date
    # adb/ /adfg 1000/ 
    regex = r"([a-z][/]|\s[/])"
    subst = r'\1@'
    input = re.sub(regex, subst, input, 0, re.MULTILINE)
    input = input.replace("/@", "@/@")
    regex = r"([0-9][/]\s)"
    subst = r'\1@'
    input = re.sub(regex, subst, input, 0, re.MULTILINE)
    input = input.replace("/ @", "@/@")

    # replace comma ()
    regex = r"([a-z][,]|[0-9][,]\s)"
    subst = r'\1@'
    input = re.sub(regex, subst, input, 0, re.MULTILINE)
    input = input.replace(",@", "@,@")
    input = input.replace(", @", "@,@")

    regex = r"([()|!#$%&*_+={}:;?~`])"
    subst = r'@\1@'
    input = re.sub(regex, subst, input, 0, re.MULTILINE)

    input = input.replace(" ", "@")

    # replace all the sequencial nonword character
    regex = r"([^\w]{2,})"
    subst = r'@'
    input = re.sub(regex, subst, input, 0, re.MULTILINE)

    # seperate all tokens
    output = re.split("@", input)
    # remove empty tokens
    output = [item for item in output if item]
    return output

def add_stopwords(file, stopwords):
    f = open(file, "r").readlines()
    for stopword in f:
        stopword = stopword.split('\n')[0].lower()
        stopwords.add(stopword)

def read_stopwords():
    f = open("dictionary/stopwords", "r").readlines()
    stopwords=set()
    for stopword in f:
        stopword = stopword.split('\n')[0].replace(" ", "")
        stopwords.add(stopword)
    add_stopwords("dictionary/StopWords_Generic.txt", stopwords)
    add_stopwords("dictionary/StopWords_GenericLong.txt", stopwords)
    return stopwords

def removeStopwords(input, stopwords):
    temp = input.copy()
    for elem in temp:
        lower_elem = elem.lower()
        if lower_elem in stopwords:
            input.remove(elem)
    return input

def stemWords(input):
    stem = porterStemmer.PorterStemmer()
    output = []
    for word in input:
        output.append(stem.stem(word, 0,len(word)-1))
    return output


def remove_punctuations(input):
    output = []
    punctuation_string = "/()!#$%&*_+={}:;?~`.,"
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for elem in input:
        if elem not in punctuation_string and elem not in alphabet and elem != "'s" and elem != "s'":
            output.append(elem)
    return output

def combine_preprocess(texts):
    stopwords = read_stopwords()
    text_tokens = []
    for line in texts:
        # removeSGML
        text = removeSGML(line)
        # tokenizetext
        text_array = tokenizeText(text)
        # removestopwords
        text_array = removeStopwords(text_array, stopwords)
        # remove punctuations
        text_array = remove_punctuations(text_array)
        # stemmer
        # text_array = stemWords(text_array)
        # print(text_array)
        text_tokens.append(text_array)
    return text_tokens


