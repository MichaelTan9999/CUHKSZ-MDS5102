import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
# from sklearnex import patch_sklearn
# patch_sklearn() # only used for accelerating the sklearn functions, provided by Intel
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import make_pipeline

data = pd.read_csv('Score.csv')
data.drop(columns=['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'math score'], inplace=True)

le = LabelEncoder()
le.fit(data['test preparation course'])

x = data.iloc[:, 1:].values
y = le.transform(data['test preparation course'])

clf = make_pipeline(StandardScaler(), SGDClassifier(loss='log'))

N = 200

clf.fit(x[:N], y[:N])
bias = clf[1].intercept_[0]
w1, w2 = clf[1].coef_.T

color = []
for i in y:
    if i == 0:
        color.append('r')
    else:
        color.append('b')

c = - bias/w2
m = - w1/w2
xmin, xmax = 0, 100
ymin, ymax = 0, 100
xd = np.array([xmin, xmax])
yd = m * xd + c
plt.plot(xd, yd, 'k', lw=1, ls='--')
plt.fill_between(xd, yd, ymin, color='tab:blue', alpha=0.2)
plt.fill_between(xd, yd, ymax, color='tab:orange', alpha=0.2)
plt.scatter(data['reading score'][:N], data['writing score'][:N], c = color[:N], label = 'train', marker = 'o')
plt.scatter(data['reading score'][-50:], data['writing score'][-50:], c = color[-50:], label = 'predict', marker = 'x')
plt.legend()
plt.xlabel('reading score')
plt.ylabel('writing score')

n = []
accuracies = []

while N <= 950:
    start = time.time()
    clf.fit(x[:N], y[:N])
    end = time.time()
    accuracy = clf.score(x[-50:], y[-50:])
    print('The accuracy with {} training samples is {}, costs {:.6f}s.'.format(N, accuracy, end - start))
    N += 50
    n.append(N)
    accuracies.append(accuracy)

acc_n = plt.figure()
plt.plot(n, accuracies)
plt.xlabel('Size of the traing set')
plt.ylabel('Accuracy')

plt.show()