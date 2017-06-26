import re

input_string = ['eu', 'heeft', 'kei']
# regex = r'(?i)(\b{}\b)'.format(input_string)
inputt = "EU Great Britain heeft de eu kei hard in de poepert genomen EU eu"
# compiled = re.compile(regex)

regex = []
index = 0
for item in input_string:
    regex.append(r'(?i)(\b{}\b)'.format(item))
    regex[index] = re.compile(regex[index])
    index +=1

output = []

for compiled in regex:
    output.append(compiled.findall(inputt))

print(output)
