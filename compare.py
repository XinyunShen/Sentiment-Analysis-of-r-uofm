import matplotlib.pylab as plt

f = open("output/LM_dict_sentiment_output.txt",'r')
category_score = {}
for line in f:
    line = line.split('\n')[0].split(',')
    category = line[1]
    score = float(line[2])
    if category in category_score:
        category_score[category] += score
    else:
        category_score[category] = score

# print(category_score)
my_dict = category_score
# my_dict = { 'Khan': 4, 'Ali': 2, 'Luna': 6, 'Mark': 11, 'Pooja': 8, 'Sara': 1}

myList = my_dict.items()
myList = sorted(myList) 
x, y = zip(*myList) 
print(x)
print(y)

# plt.plot(x, y)
# plt.show()

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
# langs = ['C', 'C++', 'Java', 'Python', 'PHP']
# students = [23,17,35,29,12]
ax.bar(x[20:],y[20:])
plt.show()