import os

class0 = 0
class1 = 0
class2 = 0

for root, dirs, files in os.walk("."):  
    for filename in files:
        file = open(filename, "r")
        for line in file:
            if line[0] == '0':
                class0 += 1
            elif line[0] == '1':
                class1 += 1
            elif line[0] == '2':
                class2 += 1
print(class0, class1, class2)
