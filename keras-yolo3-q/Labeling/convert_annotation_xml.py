import os, cv2
import xml.etree.ElementTree as ET

def main():
    direc = "./output/PASCAL_VOC/"
    filem = open("scrimg_train.txt", "a")
    for root, dirs, files in os.walk(direc):
        for filename in files:
            newfn = "input/" + filename[:-3] + 'jpg'
            img = cv2.imread(newfn, cv2.IMREAD_COLOR)
            if img.__class__.__name__ != "NoneType":
                tree = ET.parse(direc + filename)
                root = tree.getroot()
                annotations = "./Labeling/" + newfn
                num_of_boxes = 0
                for boxes in root.iter('object'):
                    meta = boxes.getchildren()
                    cls_id = str(["latin", "thai", "inuktitut"].index(meta[0].text))
                    box = meta[4]
                    xmin, ymin, xmax, ymax = box[0].text, box[1].text, box[2].text, box[3].text
                    box_text = ' ' + xmin + ',' + ymin + ',' + xmax + ',' + ymax + ',' + cls_id
                    annotations += box_text
                    num_of_boxes += 1
                if num_of_boxes > 0:
                    filem.write(annotations + '\n')
    filem.close()
    
main()
