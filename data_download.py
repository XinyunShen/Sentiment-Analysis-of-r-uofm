from IPython import display
import math
from pprint import pprint
import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
import praw
from praw.models import MoreComments

def preprocess(text):
    text = text.split('\n')
    text = " ".join(text)
    return text


def main():
    sns.set(style='darkgrid', context='talk', palette='Dark2')

    reddit = praw.Reddit(client_id='8N3Jm_LZUT-sjQ',
                     client_secret='drCsZJL7XTkh_WH09aEzSGe8aeLMSA',
                     user_agent='Alyssa_yun')
    headlines = set()

    saved_file = open("reddit_post.csv",'a') 

    i = 0
    for submission in reddit.subreddit('uofm').new(limit=2000):
        i += 1
        print(i)
        headlines.add(submission.title)
        post_text = preprocess(submission.selftext)
        flair_text = submission.link_flair_text
        output = "post,{},{}\n".format(flair_text, post_text)
        saved_file.write(output)
        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            comment_text = preprocess(top_level_comment.body)
            output = "comment,{},{}\n".format(flair_text, comment_text)
            saved_file.write(output)
        display.clear_output()
    
    print(len(headlines))


if __name__ == '__main__':
    main()