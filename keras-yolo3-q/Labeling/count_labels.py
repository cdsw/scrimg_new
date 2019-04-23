import os

path = 'output/'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))

l0 = 0
l1 = 0
l2 = 0

for f in files:
    ff = open(f, 'r')
    for line in ff:
        c = line[0]
        if c == '0':
            l0 += 1
        elif c == '1':
            l1 += 1
        elif c == '2':
            l2 += 1

print(l0, l1, l2)
