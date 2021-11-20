import pandas as pd

data = pd.read_csv('q3.csv', delimiter='\t')
data.drop(columns=['Unnamed: 0'], inplace=True)

print('Number of observations: ', len(data))
print('Number of columns: ', len(data.columns))
print('Column names are: ', end='')
for i in data.columns.values:
    print(i, end=' ')
print()

print('The first 10 entries of the data: ')
print(data.head(10))
print('The last 15 entries of the data: ')
print(data.tail(15))

print('The Education data with least occurrence is ', data['Education'].value_counts().keys()[-1])
print('The number of Year_Birth is ', len(data['Year_Birth'].value_counts()))
print('The most frequent Marital_Status is ', data['Marital_Status'].value_counts().keys()[0])
print('All values of Kidhome of the most frequent Marital_Status is ', data[data['Marital_Status'] == data['Marital_Status'].value_counts().keys()[0]]['Kidhome'].unique())

income = []
for i in data['Education'].unique():
    income.append([max(data[data['Education'] == i]['Income']), min(data[data['Education'] == i]['Income'])])
income_df = pd.DataFrame(income, columns=['Max income', 'Min income'], index=data['Education'].unique())
print(income_df)

wines = []
for i in data['Marital_Status'].unique():
    wines.append([data[data['Marital_Status'] == i]['MntWines'].mean(), data[data['Marital_Status'] == i]['MntWines'].std()])
wines_df = pd.DataFrame(wines, columns=['Mean', 'Standard deviation'], index=data['Marital_Status'].unique())
print(wines_df)

'''
                Mean  Standard deviation
Married   299.480324          337.982007
Together  306.825862          334.562564
Single    288.331250          333.111329
Divorced  324.844828          347.097304
Widow     369.272727          333.919059
Alone     184.666667          302.572856
Absurd    355.500000          163.341666
YOLO      322.000000            0.000000


Roughly it can be observed that ones with normal relationships (Married, Single) have fewer wine consumption than that of ones who have
terrible relationships (Divorced, Window, Absurd).

'''