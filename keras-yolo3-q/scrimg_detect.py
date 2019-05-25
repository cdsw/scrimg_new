import os, datetime, re
from utilities.yolo import YOLO

debug = True
print_trace = False

class Scrimg:
    def __init__(self, config_path, version, model_path, anchors_path, classes_path, threshold, iou, model_image_size, gpu_num):
        self.version = version
        self.initialize_paths()
        self.num_of_classes, self.class_mapping = self.import_config(config_path)
        self.img_count = self.initialize_statistics()
        self.total_correctness = self.initialize_statistics()
        self.detected = self.initialize_statistics()
        self.total_confidence = self.initialize_statistics()
        self.total_box = 0
        self.threshold = threshold
        self.iou = iou
        self.yolo = YOLO(version, model_path, anchors_path, classes_path, threshold, iou, model_image_size, gpu_num)

    @staticmethod
    def find_code(inp, mapping):
        for k, v in mapping.items():
            if str(inp) == str(v[0]) or str(inp) == str(v[1]) or inp == k:
                return k
    @staticmethod
    def divide(dict1, dict2):
        dict_res = {}
        for k, v in dict1.items():
            try:
                dict_res[k] = dict1[k] / dict2[k]
            except ZeroDivisionError:
                dict_res[k] = 0
        return dict_res

    @staticmethod
    def summation(dict1):
        summ = 0
        for k, v in dict1.items():
            summ += v
        return summ

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

    def initialize_paths(self):
        if not os.path.exists("./out-" + self.version + "/"):
            os.makedirs("./out-" + self.version + "/")

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
        if debug and print_trace:
            print("===Class to test: " + self.class_mapping[class_to_test][0] + ", found " + str(num_box) + " box(es).")
        if num_box != 0:
            confidences = self.initialize_statistics()
            for b in range(num_box):
                (l, t, r, bo) = boxes[b][1]
                temp = boxes[b][0].split()
                cls, confidence = Scrimg.find_code(temp[0], self.class_mapping), float(temp[1])
                if debug and print_trace:
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
                    if debug and print_trace:
                        print("Image: " + img + " detected in " + str((time * 100000) // 100) + " milliseconds.")
                    correctness, highest_confidence, detected = self.extract_box(boxes, class_test)
                    self.total_correctness[class_test] += correctness
                    try:
                        self.total_confidence[highest_confidence[0]] += highest_confidence[1]
                    except KeyError:
                        pass
                    self.detected[class_test] += detected
                    if debug:
                        r_image.save('./out-' + self.version + '/' + img, 'PNG')

        # Get logging data
        f = open('./utilities/logs.txt', 'r+')
        test_num = int(f.read().count('$'))
        print(test_num)
        f.close()

        log = ''
        log += "TESTING RUN # " + str(test_num) + ' at ' + str(datetime.datetime.now()) + '\n'
        log += 'WITH MODEL VERSION: ' + self.version + ', THRESH = ' + str(self.threshold) \
               + ', IOU = ' + str(self.iou) + '\n'
        log += "Num of images    : " + str(self.img_count) + ' with #boxes: ' + str(self.total_box) + '\n'
        log += "Total confidence : " + str(self.total_confidence) + '\n'
        log += "Total correctness: " + str(self.total_correctness) + '\n'
        log += "Total detected   : " + str(self.detected) + '\n'
        log += "Ave. confidence : " + str(Scrimg.divide(self.total_confidence, self.img_count)) + '\n'
        log += "Ave. correctness: " + str(Scrimg.divide(self.total_correctness, self.img_count)) + '\n'
        if Scrimg.summation(self.img_count) != 0:
            log += "Overall: System correctness = " + str(Scrimg.summation(self.total_correctness)/Scrimg.summation(self.img_count)) + '\n\n'
        else:
            log += "Overall: System correctness = 0 \n\n"

        f = open('./utilities/logs.txt', 'a+')
        print(log)
        f.write('$\n' + log)
        f.close()

        self.yolo.close_session()

    def detect_one(self):
        while True:
            s = input("Image to detect: (empty to exit)")
            if s == '':
                break
            try:
                r_image, boxes, time = self.yolo.detect_image(s)
                correctness, highest_confidence, detected = self.extract_box(boxes, 'K')
                r_image.save('./out/' + str("datetime") + '.png', 'PNG')
            except:
                print('Image cannot be processed.')

if __name__ == "__main__":
    version = 'T0518'
    grid = 8
    model_path= 'model_data/yolo-' + version + '.h5'
    anchors_path= 'model_data/scrimg_anchors-' + version + '.txt'
    classes_path= 'model_data/scrimg_classes.txt'
    threshold= 0.1
    iou= 0.35
    model_image_size= (32 * grid, 32 * grid)
    gpu_num= 1
    config_path = "./utilities/config.txt"
    path = "./dataset/output/"
    sc = Scrimg(config_path, version, model_path, anchors_path, classes_path, threshold, iou, model_image_size, gpu_num)

    sc.detect_img_bulk(path)
    #sc.detect_one()