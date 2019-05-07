import sys
import argparse
from yolo import YOLO  # , detect_video
from PIL import Image
import os


def detect_img(yolo):
    path = "./mokemify/output/"
    imgCount = [0, 0, 0]
    total_accuracy = [0, 0, 0]
    undetected = [0, 0, 0]
    for r, d, f in os.walk(path):
        for img in f:
            class_mappings = {'L': ['latin', 0], 'T': ['thai', 1], 'K': ['korean', 2]}
            try:
                r_image, accuracy = yolo.detect_image(path + img, class_mappings[img[0]][0])
            except:
                print(" Not an image.")
            else:
                und = 0
                if accuracy == 0:
                    und = 1
                total_accuracy[class_mappings[img[0]][1]] += accuracy
                undetected[1] += und
                r_image.save('./out/' + img, 'PNG')
                print("acc: " + str(accuracy) + " tot: " + str(total_accuracy) + " img ct " + str(imgCount))
                print(img + '^')
    print("TOTAL_ACCURACY = "
          + "LATIN:  " + str(total_accuracy[0] / imgCount[0]) + '\n'
          + "THAI:   " + str(total_accuracy[1] / imgCount[1]) + '\n'
          + "KOREAN: " + str(total_accuracy[2] / imgCount[2]) + '\n'
          + "UNDETECTED: " + str(undetected) + '\n'
          + "TOTAL:  " + str(sum(total_accuracy) / sum(imgCount)) + '\n')

    yolo.close_session()


FLAGS = None

if __name__ == '__main__':
    detect_img(YOLO())
