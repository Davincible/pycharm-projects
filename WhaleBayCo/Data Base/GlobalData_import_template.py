#   Create automatic backup

import pandas as pd
import numpy as np
import time

start = time.time()

rows_to_skip = 18
rows_appended = 0

database_path = 'F:\Whale Bay & Co\Database\Whale Bay & Co BV - Database - output.xlsx'
data_template_path = 'F:\Whale Bay & Co\Database\MARKETED INNOVATOR DRUGS LIST PER THERAPHY.xls'

# IMPORT: database and excel sheet.
# data_template = pd.read_excel('F:\Whale Bay & Co\Database\Oncology_data_sample_01.xlsx')
#database = pd.read_excel('F:\Whale Bay & Co\Database\Whale Bay & Co BV - Database.xlsx', skiprows=3)
database = pd.read_excel(database_path)
data_template = pd.read_excel(data_template_path, skiprows=rows_to_skip)

# check if there is any data in the data base already, if so, what is the first emtpy line?
# start to add the data from the first empty line.


# create a dictionary with all the columns, by default conaining the value None
DB_columns = {}
for item in database.columns.values:
    DB_columns[item] = None
# create a dictionary with all the columns, by default conaining the value None
DT_columns = {}
for item in data_template.columns.values:
    DT_columns[item] = None

# copy the dictionaries to an empty backup, to easily empty a filled dictionary after each row of data
empty_DB_columns = DB_columns.copy()
empty_DT_columns = DT_columns.copy()

existing_rows = []

# create a list with the columns to later use in the data filter to check if a row aleady exists in the database
db_cols = list(database.columns.values)
dt_cols = list(data_template.columns.values)

limit = 0
try:
    index = 0
    while True:

        # reset the dictionary to an empty dictionary with all the columns
        DT_columns = empty_DT_columns.copy()
        row_series = None
        data_filter = None
        column_index = 0
        row_exists = False
        previous_match = True


        # fetch a row of the data sheet
        row = data_template.iloc[index]

        # temporarily limit the number of rows processed
        if limit == 100000:
            break

        # itterate over the columns and assign the data to the dictionary
        for column in DT_columns:
            DT_columns[column] = row[column]

        if type(DT_columns['Drug Name']) != type(np.nan) and DT_columns['Drug Name'] != 'Source:':
            # print(DT_columns['Drug Name'], 'and the data type is: ', type(DT_columns['Drug Name']))

            # sync the dictionaries
            DB_columns['Company'] = DT_columns['Company Name']
            DB_columns['Therapeutic area'] = DT_columns['Therapy Area']
            DB_columns['Indiciation'] = DT_columns['Indication']
            DB_columns['Drug Name'] = DT_columns['Drug Name']
            DB_columns['Status of the Drug'] = DT_columns['Development Stage']
            DB_columns['Brand Name'] = DT_columns['Brand Name']
            DB_columns['Drug Geography'] = DT_columns['Drug Geography']

            # check if this row of data already exists in the current database
            for column in db_cols:

                if previous_match:
                    # print("passed the first if statement")
                    # if we are checking the first column, check all rows
                    if db_cols.index(column) == 0:
                        if DB_columns[column] == None:
                            database.loc[overlapping_row, database.columns.get_loc(column)] = None
                            # print("DATATYPE: ", type(database.iloc[overlapping_row[0]][column]), '\n', database.iloc[overlapping_row[0]][column])
                        # print('\n checking first column \n')
                        # create a boolean mask of the columns
                        data_filter = database[column].where(database[column] == DB_columns[column])

                        if DB_columns[column] == None:
                            data_filter.loc[overlapping_row] = 'None'

                        # drop the NaN values in the mask
                        data_filter = data_filter.dropna()


                    # if we are checking anything but the first column, only check the rows with which the previous column matched.
                    else:
                        if DB_columns[column] == None:
                            database.loc[overlapping_row, database.columns.get_loc(column)] = None
                            # print("DATATYPE: ", type(database.iloc[overlapping_row[0]][column]), '\n', '--RETURNS--',database.iloc[overlapping_row[0]][column])
                        # create a boolean mask of the columns
                        data_filter = database.iloc[overlapping_row][column].where(database[column] == DB_columns[column])

                        if DB_columns[column] == None:
                            # print('-----------------------------THE OVERLAPPING ROW IS: ', overlapping_row)
                            # print(data_filter)
                            data_filter.loc[overlapping_row] = 'None'

                        # drop the NaN values in the mask
                        data_filter = data_filter.dropna()
                        # print('\n checking %d th column \n %s %s \n %s %s \n' % (db_cols.index(column), database.iloc[overlapping_row][column], type(database.iloc[overlapping_row][column]), DB_columns[column], type(DB_columns[column])))

                    # check if there is any value in
                    if data_filter.empty == False and previous_match == True:
                        overlapping_row = list(data_filter.index.values)
                        previous_match = True
                        # print('found overlap: ', overlapping_row)

                        if db_cols.index(column) == (len(db_cols) - 1):
                            row_exists = True
                            existing_rows.append(index)

                            # print('row_exists set to true')

                    elif data_filter.empty == True and previous_match == True:
                        previous_match = False
                        # print('previous match set to false')

                column_index += 1

            if row_exists == False:
                row_series = pd.Series(DB_columns)
                database = database.append(row_series, ignore_index=True)
                rows_appended += 1
                print("no conflict found")
            else:
                print("this row already exits -------------")
            # print(row_series)

        limit += 1
        index += 1

except IndexError as error01:
    print("Processed all of %d rows in the excel sheet" % data_template.shape[0])
    # raise error01

print('-------------------------------------------')
if existing_rows:
    for i in range(len(existing_rows)):
        existing_rows[i] += 2 + rows_to_skip
    print('These rows of data have not been appended: ', existing_rows)

if rows_appended > 0:
    print('You just appened %d rows to the DataBase' % rows_appended)
else:
    print('No rows have been appended')

database.to_excel('F:\Whale Bay & Co\Database\Whale Bay & Co BV - Database - output.xlsx')
end = time.time()
elapsed = end - start
print("THIS JOB TOOK %d SECONDS" % elapsed)

# Search if a row already exists in the database: filter using df.where(), then put that returned series in a variable,
# then series.dropna(), if series.empty returns True then it is empty. if it returns False then not.
# use if statements, only check the next column if the first returns true. Only check the rows which returned true in the first place.