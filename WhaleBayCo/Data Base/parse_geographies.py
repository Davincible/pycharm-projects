import pandas as pd

datasheet = pd.read_excel("F:\Whale Bay & Co\Database\Whale Bay & Co BV - Database - output.xlsx")
# print(datasheet.head)
geo_column = datasheet['Drug Geography']
# print('---------------------------------------------------')
# geo_list = geo_column.tolist()
geo_list = list()

for item in geo_column:
    temp = item.split(';')
    temp = map(str.strip, temp)
    for loc in temp:
        if loc in geo_list:
            pass
        else:
            geo_list.append(loc)

print('THE LIST IS:', geo_list)

# ['South Korea',
# 'United States',
# 'Russia',
# 'United Kingdom',
# 'Germany',
# 'Italy',
# 'Spain',
# 'Mexico',
# 'EU',
# 'France',
# 'Canada',
# 'South Africa',
# 'Brazil',
# 'Japan',
# 'Australia',
# 'China',
# 'India',
# 'Global',
# 'Asia-Pacific',
# 'North America',
# 'Taiwan']
