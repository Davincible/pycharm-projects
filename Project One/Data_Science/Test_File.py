import pandas as pd
import numpy as np

purchase_1 = pd.Series({'Name': 'Chris',
                        'Item Purchased': 'Dog Food',
                        'Cost': 22.50})
purchase_2 = pd.Series({'Name': 'Kevyn',
                        'Item Purchased': 'Kitty Litter',
                        'Cost': 2.50})
purchase_3 = pd.Series({'Name': 'Vinod',
                        'Item Purchased': 'Bird Seed',
                        'Cost': 5.00})
df = pd.DataFrame([purchase_1, purchase_2, purchase_3], index=['Store 1', 'Store 1', 'Store 2'])
print(df)

series_data = pd.Series(purchase_1)
print(series_data.index)
print("\n-----------------------")
value_list = series_data.values
print(value_list)
print(type(value_list))

a_new_array = np.array(purchase_1)
print(a_new_array)
print(a_new_array.dtype)
print(a_new_array)

print('\n\n')

a_new_array.append('a dick')
print(a_new_array)