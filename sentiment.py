import sys
import nlt_train
import preprocess
import LM_dic
import naive_bayes

def read_file(input_path):
    f = open(input_path, 'r').readlines()
    text_type = []
    text_flairs = []
    text = []
    for line in f:
        line = line.split('\n')[0].split(',')
        text_type.append(line[0])
        text_flairs.append(line[1])
        text.append(','.join(line[2:]))
    return text_type, text_flairs, text

def output_file(output_path, text_type, text_flairs, sentiment_output):
    f = open(output_path, 'a')
    for index, elem in enumerate(text_type):
        output = "{},{},{}\n".format(text_type[index], text_flairs[index], sentiment_output[index])
        f.write(output)



def main(argv):
    preprocess_methtod = ''
    input_path = ''
    method = ''
    output_path = ''
    test_file = ''

    long_options = ["preprocess_method=", "input_path=", "method=", "output_path=","test_file="]

    for index, elem in enumerate(argv):
        if elem == "--preprocess_method":
            preprocess_methtod = argv[index + 1]
        elif elem == "--input_path":
            input_path = argv[index + 1]
        elif elem == "--method":
            method = argv[index + 1]
        elif elem == "--output_path":
            output_path = argv[index + 1]
        elif elem == "--test_file":
            test_file = argv[index + 1]
    
    

    # preprocess
    text_tokens = []
    if preprocess_methtod == "customize_preprocess":
        # read input file
        text_type, text_flairs, text = read_file(input_path)
        text_tokens = preprocess.combine_preprocess(text)
    elif preprocess_methtod == "nltk":
        # read input file
        text_type, text_flairs, text = read_file(input_path)
        text_tokens = nlt_train.preprocess(text)
        

    sentiment_output = []
    if method == "nltk":
        sentiment_output = nlt_train.train_nltk(text_tokens)
        output_file(output_path, text_type, text_flairs, sentiment_output)
    elif method == "LM_dict":
        sentiment_output = LM_dic.train_LM_dic(text_tokens)
        output_file(output_path, text_type, text_flairs, sentiment_output)
    elif method == 'naive_bayes':
        probs = [0,0,0]
        # pos/neutral/neg
        num_words = [0,0,0]
        word_prob = [{},{},{}]
        len_vocab = 0
        probs, word_prob, smoothing, len_vocab = naive_bayes.trainNaiveBayes(input_path)
        naive_bayes.testNaiveBayes(probs, word_prob, smoothing, len_vocab, test_file, output_path)




    
if __name__ == "__main__":
    main(sys.argv[1:])