def read_postive_negative():
    positives = []
    negatives = []
    f = open("dictionary/LoughranMcDonald_negative.csv", 'r')
    for line in f:
        negatives.append(line.split('\n')[0].lower())
    f = open("dictionary/LoughranMcDonald_positive.csv", 'r')
    for line in f:
        positives.append(line.split('\n')[0].lower())
    return positives, negatives

def train_LM_dic(text_tokens):
    sentiment_output = []
    positives, negatives = read_postive_negative()
    for tokens in text_tokens:
        # print(tokens)
        positive = 0
        negative = 0
        for token in tokens:
            token = token.lower()
            if token in positives:
                positive += 1
            if token in negatives:
                negative += 1
        score = 0
        if positive + negative != 0:
            score = (positive - negative) / (positive + negative)
        sentiment_output.append(score)
        # print(score)
    return sentiment_output