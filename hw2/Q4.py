import pandas as pd

data = pd.read_csv('q4.txt', delimiter='|')

data.set_index('user_id', inplace=True)

age = []
for i in data['occupation'].unique():
    age.append([data[data['occupation'] == i]['age'].mean(), data[data['occupation'] == i]['age'].std()])
age_df = pd.DataFrame(age, columns=['Mean', 'Standard deviation'], index=data['occupation'].unique())
print(age_df)

print()
sex_ratio = []
for i in data['occupation'].unique():
    sex_ratio.append(len(data[(data['occupation'] == i) & (data['gender'] == 'F')]) / len(data[data['occupation'] == i]))
sex_ratio_df = pd.DataFrame(sex_ratio, columns=['Female ratio'], index=data['occupation'].unique())
print(sex_ratio_df.sort_values(by=['Female ratio'], ascending=False))

print()
occupation_sex_age = []
for i in data['occupation'].unique():
    occupation_sex_age.append([data[(data['occupation'] == i) & (data['gender'] == 'M')]['age'].mean(), data[(data['occupation'] == i) & (data['gender'] == 'F')]['age'].mean()])
occupation_sex_age_df = pd.DataFrame(occupation_sex_age, columns=['Male mean age', 'Female mean age'], index=data['occupation'].unique())
print(occupation_sex_age_df)

print()
sex_ratio_temp = pd.DataFrame([1 - i for i in sex_ratio], columns=['Male ratio'], index=data['occupation'].unique())
sex_ratio_df2 = sex_ratio_df.join(sex_ratio_temp)
print(sex_ratio_df2)
