import pandas as pd 

l = pd.read_csv('new_dev.csv').drop(['delete_column','delete_column_2'],axis=1)
uni_values = l.Address.unique()

print(uni_values)



