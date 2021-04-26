# Sentiment Analysis of r/uofm 

This project uses the praw python library/api to gather data from r/uofm. 

## Getting Started

To run the sentiment analysis program, you will need all of the files on this repo. You can either clone this repository, or download the files a compressed tar ball. To make the stress of gathering the data simpler, we've already included the files ``reddit_post.csv`` which consists of the pulled text data from r/uofm. To see how we gathered this data, take a look at ``data_download.py``.

Also, make sure you have python3 installed in order to run the sentiment analysis.

## Analyzing (2 methods)

All of the commands mentioned below can be found in ``commands_to_run.txt``. Once you have all the files downloaded,  use the following command to run the first sentiment analysis:

### NLTK + Naive Bayes Method

For NLTK, we should first install NLTK package using

``$ pip install nltk``

We also have to download the dictionary in NLTK in a python file using

``$ nltk.download('vader_lexicon')``

``$ nltk.download('stopwords')``

Then we can run

``$ python3 sentiment.py --preprocess_method nltk --input_path reddit_post.csv --method nltk --output_path output/nltk_sentiment_output.txt``

This will create the file ``output/nltk_sentiment_output.txt`` which processes the csv with the nltk method. The output of the file is in the format ``<type of post>, <flair>, <nltk score>``. The nltk scores will be bounded from -1 to 1 where -1 indicates a negative polarity and 1 indicates a positive polarity given the text. 
After we run complete nltk process, we convert the score into sentimental labels using ``scoreTolabel.py``. This will generated a file in the format  ``<type of post>, <flair>, <sentiments>,<post content>``. We use part of it to train our naive bayes classifier and part of it to test using the following command:

``$ python3 sentiment.py --input_path naive_bayes/post_train.csv --method naive_bayes --test_file naive_bayes/post_test.csv --output_path output/naive_bayes_sentiment_output.txt ``

Here we will be able to get the output of naive bayes that exsists within the output folder called ``naive_bayes_sentiment_output.txt ``. The output of this file will be in the form of ``<type of post>, <flair>, <sentiment>`` where sentiment is either Positive, Negative, or Neutral.


### Dictionary Method

We can also use what we called the 'dictionary' method to do some analysis on the sentiment of the content on r/uofm. We can run the following command:

``$ python3 sentiment.py --preprocess_method customize_preprocess --input_path reddit_post.csv --method LM_dict --output_path output/LM_dict_sentiment_output.txt``

and get a text file ``LM_dict_sentiment_output.txt`` of the format ``<type of post>, <flair>, <sentiment score>``. This method uses a predefined set of words that are considered positive and negative which could explain why posts are very extreme within the range of -1 to 1.


## Acknowledgements

This project was built as final project for EECS 486 at the University of Michigan -- Ann Arbor.

Authors - EECS 486 Group 14

