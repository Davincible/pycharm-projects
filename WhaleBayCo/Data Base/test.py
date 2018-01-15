import pandas as pd
import sqlite3

# IMPORT: database and excel sheet.
# data_template = pd.read_excel('F:\Whale Bay & Co\Database\Oncology_data_sample_01.xlsx', index_col='Drug Name')
# database = pd.read_excel('F:\Whale Bay & Co\Database\Whale Bay & Co BV - Database.xlsx', skiprows=3)



database_path = 'F:\Whale Bay & Co\Database\Whale Bay & Co BV - Database - output.xlsx'


# IMPORT: database and excel sheet.
# data_template = pd.read_excel('F:\Whale Bay & Co\Database\Oncology_data_sample_01.xlsx')
#database = pd.read_excel('F:\Whale Bay & Co\Database\Whale Bay & Co BV - Database.xlsx', skiprows=3)
database = pd.read_excel(database_path)

#print(data_template.head(30))

raw_data_template_path = 'F:\Whale Bay & Co\Database\MARKETED INNOVATOR DRUGS LIST PER THERAPHY.xls'
raw_data_template = pd.read_excel(raw_data_template_path)
data_shortcut = raw_data_template[raw_data_template.columns.values[1]]
filter_one = data_shortcut.where(data_shortcut == "Drug Name")
filter_one.dropna(inplace=True)
skip_rows = filter_one.index.values[0] + 2
print(skip_rows)

# print(data_template.columns.values3)

# print(data_template.shape[0])

#conn = sqlite3.connect('F:\Whale Bay & Co\Database\DataBase_01.db')
#c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS sample_data("
              "company TEXT, "
              "therapeutic_area "
              "TEXT, indication TEXT, "
              "drug_name TEXT, "
              "status_of_the_drug TEXT, "
              "ownership TEXT, "
              "outlicensed TEXT, "
              "inlicensed TEXT, "
              "brand_name TEXT, "
              "sales REAL)")

def data_entry():
    pass






