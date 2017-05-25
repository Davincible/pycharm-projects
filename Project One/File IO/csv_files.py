import csv

with open('C:/Users/David.MIDDENAARDE/Downloads/nation.1751_2014.csv') as data_file:
    file_contents = list(csv.DictReader(data_file))


file_contents_copy = file_contents
file_contents_copy = str(file_contents_copy)
file_contents_copy = file_contents_copy.replace(", ", ",\n")
file_contents_copy = file_contents_copy.replace("{", "\n{")


# Get the average and total emission for selected years
data_year = ['1988', '1990', '1995', '2000', '2010', '2014']
sum = [0.00] * 6
element_count = [0.00] * 6
average_emission = [0.00] * 6
year_int = 0

for year in data_year:
    for d in file_contents:
        if d['Year'] == year:
            sum[year_int] += float(d['Total CO2 emissions from fossil-fuels and cement production (thousand metric tons of C)'])
            element_count[year_int] +=1

    average_emission[year_int] = sum[year_int]/element_count[year_int]
    year_int +=1
# ------------------------------------------------------------------------------------------
#
# Get the average value per country over all the years

countries = []

# - get all the countries
countries = sorted(set(nations['Nation'] for nations in file_contents))

# convert the countries list to a printable string
countries_string = str(countries)
countries_string = countries_string.replace(', ', '\n')
countries_string = countries_string.replace("'", '')
countries_string = countries_string.replace('{', '')
countries_string = countries_string.replace('}', '')
countries_string = countries_string.replace('[', '')
countries_string = countries_string.replace(']', '')
#print(countries_string)

countries_tuple = tuple(countries_string.split('\n'))
countries_dictionary = dict.fromkeys(countries_tuple, [0, 1, 2, 3])
print(countries_dictionary)

for number_of_countries in range(len(countries)):
    for data in file_contents:
        if data['Nation'] == countries[number_of_countries]:
            try:
                print(data['Nation'])
                temp = int(data['Total CO2 emissions from fossil-fuels and cement production (thousand metric tons of C)'])
                print(data['Nation'] + ' : ' + str(temp))
                countries_dictionary[str(data['Nation'])][1] = temp
                print(countries_dictionary[data['Nation']][1])
            except KeyError:
                print('This %s country is not in the dictionary' % data['Nation'])

print(countries_dictionary)
var = max(countries_dictionary, key=countries_dictionary.get)
print(var + ' with: %d' % countries_dictionary[var][0])

# print the output and write it to an output file
with open('C:/Users/David.MIDDENAARDE/Downloads/Data_Output_01.txt', 'r+') as output_file:
    try:
        for element in range(len(data_year)):
            print('The total emission over %d countries in %s was: %.4f' % (element_count[element], data_year[element], sum[element]))
            print('In the year %s the average CO2 emission was: %.4f' % (data_year[element], average_emission[element]))
            print()

            output_file.write('The total emission over %d countries in %s was: %.4f\n' % (element_count[element], data_year[element], sum[element]))
            output_file.write('In the year %s the average CO2 emission was: %.4f\n' % (data_year[element], average_emission[element]))
            output_file.write('\n')

    except ZeroDivisionError:
        print('No data was found')


with open('C:/Users/David.MIDDENAARDE/Downloads/Nation_List.txt', 'w') as output_nations:
    output_nations.write(countries_string)