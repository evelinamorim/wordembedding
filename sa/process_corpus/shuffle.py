import random

myseed = 10007
random.seed(myseed)

with open('drugs_reviews.json', 'r') as source:
    data = [(random.random(), line) for line in source]
data.sort()
with open('shuffle_drugs_reviews.json', 'w') as target:
    for _, line in data:
        target.write(line)
