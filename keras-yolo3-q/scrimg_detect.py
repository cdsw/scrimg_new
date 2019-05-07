import os, datetime, re
from yolo import YOLO

debug = True

def main():
    config_path = "./config.txt"
    path = "./mokemify/output/"
    sc = Scrimg(config_path)
    sc.detect_img_bulk(path)
    #sc.detect_one()

def find_code(inp, mapping):
    for k, v in mapping.items():
        if str(inp) == str(v[0]) or str(inp) == str(v[1]) or inp == k:
            return k

def divide(dict1, dict2):
    dict_res = {}
    for k, v in dict1.items():
        dict_res[k] = dict1[k]/dict2[k]
    return dict_res

def summation(dict1):
    summ = 0
    for k, v in dict1.items():
        summ += v
    return summ

class Scrimg:
    def __init__(self, config_path):
        self.num_of_classes, self.class_mapping = self.import_config(config_path)
        self.img_count = self.initialize_statistics()
        self.total_correctness = self.initialize_statistics()
        self.detected = self.initialize_statistics()
        self.total_confidence = self.initialize_statistics()
        self.total_box = 0
        self.yolo = YOLO()

    @staticmethod
    def import_config(path):
        f = open(path, 'r')
        classes = f.readlines()
        num_of_classes = len(classes)
        class_mapping = {}
        for c in classes:
            c = c.split()
            class_mapping[c[2]] = [c[0], int(c[1])]  # eg 'L' : 'latin' 0
        return num_of_classes, class_mapping

    def initialize_statistics(self):
        field = {}
        for c in self.class_mapping:
            field[c] = 0
        return field

    def extract_box(self, boxes, class_to_test):
        correctness = 0
        highest_confidence = '', 0
        num_box = len(boxes)
        self.total_box += num_box
        detected = 0
        if debug:
            print("===Class to test: " + self.class_mapping[class_to_test][0] + ", found " + str(num_box) + " box(es).")
        if num_box != 0:
            confidences = self.initialize_statistics()
            for b in range(num_box):
                (l, t, r, bo) = boxes[b][1]
                temp = boxes[b][0].split()
                cls, confidence = find_code(temp[0], self.class_mapping), float(temp[1])
                if debug:
                    print("======Box #" + str(b) + ": " + cls + ' ' + str(confidence)
                      + ' ' + "(" + str(l) + ',' + str(t) + '), ' + "(" + str(r) + ',' + str(bo) + ')')
                if confidence > highest_confidence[1]:
                    highest_confidence = cls, confidence
                confidences[cls] += confidence
                if cls == class_to_test:
                    detected = 1

            if highest_confidence[0] != class_to_test:
                highest_confidence = ['', 0]
            else:
                correctness = confidences[class_to_test] / sum(confidences.values())
        return correctness, highest_confidence, detected

    def detect_img_bulk(self, path):
        thresh, iou, model_ver = self.yolo.get_params()
        for r, d, f in os.walk(path):
            for img in f:
                try:
                    r_image, boxes, time = self.yolo.detect_image(path + img)
                    class_test = img[0]
                    self.img_count[class_test] += 1
                except:
                    if debug:
                        print(" Not an image.")
                else:
                    if debug:
                        print("Image: " + img + " detected in " + str((time * 100000) // 100) + " milliseconds.")
                    correctness, highest_confidence, detected = self.extract_box(boxes, class_test)
                    self.total_correctness[class_test] += correctness
                    try:
                        self.total_confidence[highest_confidence[0]] += highest_confidence[1]
                    except KeyError:
                        pass
                    self.detected[class_test] += detected
                    if debug:
                        r_image.save('./out/' + img, 'PNG')

        # Get logging data
        f = open('./logs.txt', 'r+')
        test_num = int(f.read().count('$'))
        print(test_num)
        f.close()

        log = ''
        log += "TESTING RUN # " + str(test_num) + ' at ' + str(datetime.datetime.now()) + '\n'
        log += 'WITH MODEL VERSION: ' + re.split('/|\.',model_ver)[1] + ', THRESH = ' + str(thresh) + ', IOU = ' + str(iou) + '\n'
        log += "Num of images    : " + str(self.img_count) + ' with #boxes: ' + str(self.total_box) + '\n'
        log += "Total confidence : " + str(self.total_confidence) + '\n'
        log += "Total correctness: " + str(self.total_correctness) + '\n'
        log += "Total detected   : " + str(self.detected) + '\n'
        log += "Ave. confidence : " + str(divide(self.total_confidence, self.img_count)) + '\n'
        log += "Ave. correctness: " + str(divide(self.total_correctness, self.img_count)) + '\n'
        log += "Overall: System correctness = " + str(summation(self.total_correctness)/summation(self.img_count)) + '\n\n'

        f = open('./logs.txt', 'a+')
        print(log)
        f.write('$\n' + log)
        f.close()

        self.yolo.close_session()

    def detect_one(self):
        s = input("Image to detect: ")
        r_image, boxes, time = self.yolo.detect_image(s)
        correctness, highest_confidence, detected = self.extract_box(boxes, 'K')
        r_image.save('./out/' + '0000.png', 'PNG')


main()