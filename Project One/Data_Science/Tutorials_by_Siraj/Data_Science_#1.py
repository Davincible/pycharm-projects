from sklearn import tree

# [height, width, shoe  size]
x = [[181, 80, 44], [177, 70, 43], [160, 60, 38], [154, 54, 37], [166, 65, 40],
     [190, 90, 47], [175, 64, 39],
     [177, 70, 40], [159, 55, 37], [171, 75, 42], [181, 85, 43]]

m = 'male'
f = 'female'
y = [m, f, f, f, m, m, m, f, m, f, m]

clf = tree.DecisionTreeClassifier()

clf = clf.fit(x,y)
predicion_values = [190,70,43]

prediction = clf.predict([predicion_values])

print(prediction)
