import os, cv2

def main():
    direc = "./output/YOLO_darknet/"
    filem = open("trainh.txt", "a")
    for root, dirs, files in os.walk(direc):
        for filename in files:
            newfn = "input/" + filename[:-3] + 'jpg'
            img = cv2.imread(newfn, cv2.IMREAD_COLOR)
            if img.__class__.__name__ != "NoneType":
                file = open(direc + filename, "r")
                count = 0
                for line in file:
                    if count == 0:
                        filem.write("./Labeling/" + newfn + " ")
                        count += 1
                    h = img.shape[0]
                    w = img.shape[1]
                    line = line.split(' ')
                    cls = line[0]
                    bx = float(line[1])
                    by = float(line[2])
                    bw = float(line[3])
                    bh = float(line[4])
                    xmin = int(bx*w)
                    ymin = int(by*h)
                    xmax = int((bx+bw)*w)
                    ymax = int((by+bh)*h)
                    m = str(xmin) + "," + str(ymin) + "," + \
                        str(xmax) + "," + str(ymax) + "," + cls + ' '
                    filem.write(m)
                file.close()
                filem.write('\n')
    filem.close()
    with open('trainh.txt') as infile, open('scrimg_train.txt', 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output
    infile.close()
    outfile.close()
    os.remove("trainh.txt")
    
main()
