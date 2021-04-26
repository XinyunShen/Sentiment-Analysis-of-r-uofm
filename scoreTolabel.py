f_score = open("output/nltk_sentiment_output.txt",'r').readlines()
f_post = open('reddit_post.csv','r').readlines()

f_new = open('naive_bayes/post_train.csv','a')
for i, line in enumerate(f_score):
    line = line.split(',')
    cat = line[0]
    flair = line[1]
    score = float(line[2].split('\n')[0])
    post = ','.join(f_post[i].split(',')[2:])
    if score >= 0.2:
        sentiment = 'positive'
    elif score <= -0.2:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    output = "{},{},{},{}".format(cat,flair,sentiment,post)
    f_new.write(output)
