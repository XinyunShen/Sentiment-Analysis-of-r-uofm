from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from pprint import pprint

# nltk.download('vader_lexicon')
# nltk.download('stopwords')

def preprocess(texts):
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = stopwords.words('english')
    tokens = []
    for line in texts:
        toks = tokenizer.tokenize(line)
        toks = [t.lower() for t in toks if t.lower() not in stop_words]
        tokens.append(toks)
    return tokens



def train_nltk(text_tokens):
    sentiment_output = []
    sia = SentimentIntensityAnalyzer()

    for tokens in text_tokens:
        sentences = ' '.join(tokens)
        score = sia.polarity_scores(sentences)["compound"]
        sentiment_output.append(score)
        # if score >= 0.05:
        #     sentiment_output.append("positive")
        # elif score <= 0.05:
            # sentiment_output.append("negative")
        # else:
        #     sentiment_output.append("neutral")

    return sentiment_output


