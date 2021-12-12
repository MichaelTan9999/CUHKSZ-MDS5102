import pandas as pd
import matplotlib.pyplot as plt
import time
# from sklearnex import patch_sklearn
# patch_sklearn() # only used for accelerating the sklearn functions, provided by Intel

data = pd.read_csv('Score.csv')
data.drop(columns=['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'math score'], inplace=True)

unprepared = data[data['test preparation course'] == 'none']
prepared = data[data['test preparation course'] == 'completed']

rawFig = plt.figure()

ax = plt.subplot(1, 1, 1)

plt.scatter(unprepared['reading score'].values[:200], unprepared['writing score'].values[:200], c='r', label='not completed')
plt.scatter(prepared['reading score'].values[:200], prepared['writing score'].values[:200], c='b', label='completed')
plt.title('The scores distribution and the accomplishment of the prepared courses')
plt.xlabel('reading score')
plt.ylabel('writing score')
ax.set_box_aspect(1)

from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(data['test preparation course'])
neigh = KNeighborsClassifier(n_neighbors=10)
x = data.iloc[:, 1:].values
y = le.transform(data['test preparation course'])
neigh.fit(x[:200], y[:200])
predictedY = neigh.predict(x[-50:])

for i in predictedY:
    if i == 0:
        i = '#ed4b6f'
    else:
        i = '#1089a2'

plt.scatter(prepared['reading score'].values[-50:], prepared['writing score'].values[-50:], c=predictedY)
print(neigh.score(x[-50:], y[-50:]))

for k in range(5, 21):
    neigh = KNeighborsClassifier(n_neighbors=k)
    start = time.time()
    neigh.fit(x[:200], y[:200])
    end = time.time()
    print('The accuracy with k = {} is {}.'.format(k, neigh.score(x[-50:], y[-50:])))
    print('Time consumption: {:.6f}s.'.format(end - start))
    print()

plt.show()