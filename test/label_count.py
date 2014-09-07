#coding:utf-8

import sys
from collections import Counter

args = sys.argv[1:]
filename = args[0]

labels = []
with open(filename) as f:
    for line in f:
        label = line.split(' ')[1].strip()
        labels.append(label)

print "positive:",labels.count('positive')
print "negative:",labels.count('negative')
print "neutral:",labels.count('neutral')
print "spam:",labels.count('spam')

print Counter(labels)

