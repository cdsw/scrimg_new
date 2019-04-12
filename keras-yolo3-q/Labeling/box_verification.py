import cv2

def draw_rectangle(box, img):
    xmin, ymin, xmax, ymax, cid = int(box[0]), int(box[1]), int(box[2]), int(box[3]), int(box[4])
    if cid == 0:
        color = (0,0,255)
    elif cid == 1:
        color = (0,255,0)
    else:
        color = (255,0,0)
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, thickness=3)

def main():
    filem = open("scrimg_train.txt", "r")
    for line in filem:
        line = line.strip()
        if len(line) > 0:
            line_data = line.split()
            location = line_data[0][11:]
            boxes = []
            for i in range(1, len(line_data)):
                boxes.append(line_data[i])

            img = cv2.imread(location, cv2.IMREAD_COLOR)
            for box in boxes:
                box = box.split(',')
                draw_rectangle(box, img)
            print("verif/" + location)
            cv2.imwrite("verif/"+location[5:], img)
    filem.close()


main()
