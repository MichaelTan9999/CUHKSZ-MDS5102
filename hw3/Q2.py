import pandas as pd
import numpy as np

data = pd.read_csv('Score.csv')

for i in data.columns:
    print('The type of \'{}\' is {}'.format(i, data[i].dtype))

print()

for degree in data['parental level of education'].unique():
    print('****** Parental level of education: {} *****     '.format(degree))
    for subject in data.columns[-3:]:
        print('Subject: {}'.format(subject.split()[0]))
        min_score = min(data[data['parental level of education'] == degree][subject].values)
        max_score = max(data[data['parental level of education'] == degree][subject].values)
        mean_score = np.mean(data[data['parental level of education'] == degree][subject].values)
        std_score = np.std(data[data['parental level of education'] == degree][subject].values)

        print('Min: {}, Max: {}, Mean: {:.3f}, Standard deviation: {:.3f}'.format(min_score, max_score, mean_score, std_score))
    print()

sex_ratio = pd.DataFrame()
for race in data['race/ethnicity'].unique():
    for lunch in data[data['race/ethnicity'] == race]['lunch'].unique():
        total = data[(data['race/ethnicity'] == race) & (data['lunch'] == lunch)].size
        male = data[(data['race/ethnicity'] == race) & (data['lunch'] == lunch) & (data['gender'] == 'male')].size
        female = data[(data['race/ethnicity'] == race) & (data['lunch'] == lunch) & (data['gender'] == 'female')].size
        sex_ratio = sex_ratio.append({'Combination': '{} with {}'.format(race, lunch), 'Male ratio': (male / total), 'Female ratio': (female / total)}, ignore_index=True)
print(sex_ratio)

data.drop(columns=['gender', 'parental level of education'], inplace=True)
print(data.pivot_table(index='test preparation course', columns='lunch'))
