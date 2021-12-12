import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
# from sklearnex import patch_sklearn
# patch_sklearn() # only used for accelerating the sklearn functions, provided by Intel

data = pd.read_csv('Score.csv')
data.drop(columns=['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course', 'writing score'], inplace=True)

fig = plt.figure()
ax = plt.subplot(1, 1, 1)
ax.set_box_aspect(1)
plt.xlabel('math score')
plt.ylabel('reading score')
plt.scatter(data['math score'][:900], data['reading score'][:900], c='b', label='Training')


x = data['math score'].values.reshape(-1, 1)
y = data['reading score'].values

from sklearn.linear_model import LinearRegression

start = time.time()
reg = LinearRegression().fit(x[:900], y[:900])
end = time.time()

b = reg.intercept_
w = reg.coef_[0] # only one feature

xi = np.array(range(100))
yi = w * xi + b

plt.plot(xi, yi)
predicatedY = reg.predict(x[900:])
plt.scatter(data['math score'][900:], predicatedY, c='r', label='Predicted')
accuracy = reg.score(x[900:], y[900:])
print('The accuracy of the linear regression model is {:.6f}, costs {:.6f}s.'.format(accuracy, end - start))

plt.title('Sample and prediction of reading scores with respect to match scores')
plt.legend()
plt.show()