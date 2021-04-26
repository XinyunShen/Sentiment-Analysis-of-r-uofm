import sys
import os
import porterStemmer
import re

def tokenizeText(input):
    input = input.split('\n')[0]

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

def add_word_in_dict(word, word_prob, cat):
    index = 0
    if cat == 'neutral':
        index = 1
    elif cat == 'negative':
        index = 2
    if word in word_prob[index]:
        word_prob[index][word] += 1
    else:
        word_prob[index][word] = 1
    
def cal_word_conditional_prob(word_prob, num_word, vocab):
    for word in vocab:
        # add smoothing
        cat = ['positive', 'neutral', 'negative']
        for i in range(3):
            add_word_in_dict(word, word_prob, cat[i])
            denominator = num_word[i] + len(vocab)
            # calculate conditional probability
            word_prob[i][word] /= denominator


def trainNaiveBayes(train_file):
    f = open(train_file,'r').readlines()
    vocab = set()
    # pos/neutral/neg
    probs = [0,0,0]
    # pos/neutral/neg
    num_words = [0,0,0]
    word_prob = [{},{},{}]

    for line in f:
        line = line.split(',')
        cat = line[2]
        text = tokenizeText(','.join(line[3:]))
        if cat == 'positive':
            probs[0] += 1
            num_words[0] += len(text)
        elif cat == 'neutral':
            probs[1] += 1
            num_words[1] += len(text)
        elif cat == 'negative':
            probs[2] +=1
            num_words[2] += len(text)
        
        for word in text:
            vocab.add(word)
            add_word_in_dict(word, word_prob,cat)
    smoothing = [0,0,0]
    for i, prob in enumerate(probs):
        probs[i] /= len(vocab)
        smoothing[i] = 1/(num_words[i] + len(vocab))
    
    cal_word_conditional_prob(word_prob, num_words, vocab)
    return probs, word_prob, smoothing, len(vocab)


def cal_probability(text, class_prob, word_prob, smoothing):
    prob = class_prob
    for word in text:
        if word in word_prob:
            prob *= word_prob[word]
        else:
            prob *= smoothing
    return prob

def testNaiveBayes(probs, word_prob, smoothing, len_vocab, test_file, output_path):
    f = open(test_file, 'r').readlines()
    output_file = open(output_path, 'a')
    for line in f:
        line = line.split(',')
        text = tokenizeText(','.join(line[3:]))
        text_pos_prob = cal_probability(text, probs[0], word_prob[0], smoothing[0])
        text_neu_prob = cal_probability(text, probs[1], word_prob[1], smoothing[1])
        text_neg_prob = cal_probability(text, probs[2], word_prob[2], smoothing[2])
        prob = [text_pos_prob, text_neu_prob, text_neg_prob]
        cat = ""
        # if text_pos_prob > text_neg_prob and text_pos_prob > text_neu_prob:
        #     cat = "positive"
        # elif text_neg_prob > text_pos_prob and text_neg_prob > text_neu_prob:
        #     cat = "negative"
        # else:
        #     cat = "neutral" 
        if text_neu_prob == max(prob):
            cat = "neutral" 
        elif text_neg_prob == max(prob):
            cat = "negative"
        else:
            cat = "positive" 
        output = "{},{},{}\n".format(line[0],line[1],cat)
        output_file.write(output)
