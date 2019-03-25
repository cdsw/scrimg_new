f = open("loss_log.txt", 'r')
s = 0
c = 0
l = []
for line in f:
    if line[:5] == "13/13":
        sec = int(line[6:9])
        c += 1
        s += sec
        l.append(tuple([c, s]))
print(l)
