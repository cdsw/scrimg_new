import sys
import argparse
from yolo import YOLO#, detect_video
from PIL import Image
import os

def detect_img(yolo):
    path = "./mokemify/output/"
    imgCount = [0, 0, 0]
    total_accuracy = [0, 0, 0]
    undetected = [0, 0, 0]
    for r, d, f in os.walk(path):
        for img in f:
            try:
                image = Image.open(path + img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                # Temporary
                c = ''
                if img[0] == 'L':
                    c = 'latin'
                    imgCount[0] += 1
                elif img[0] == 'K':
                    c = 'korean'
                    imgCount[2] += 1
                elif img[0] == 'T':
                    c = 'thai'
                    imgCount[1] += 1
                r_image, accuracy = yolo.detect_image(image, c)
                und = 0
                if accuracy == 0:
                    und = 1
                if img[0] == 'L':
                    total_accuracy[0] += accuracy
                    undetected[0] += und
                elif img[0] == 'K':
                    total_accuracy[2] += accuracy
                    undetected[2] += und
                elif img[0] == 'T':
                    total_accuracy[1] += accuracy
                    undetected[1] += und
                r_image.save( './out/' + img, 'PNG' )
                print("acc: " + str(accuracy) + " tot: " + str(total_accuracy) + " img ct " + str(imgCount))
                print(img + '^')
    print("TOTAL_ACCURACY = "
          + "LATIN:  " + str(total_accuracy[0]/imgCount[0]) + '\n'
          + "THAI:   " + str(total_accuracy[1]/imgCount[1]) + '\n'
          + "KOREAN: " + str(total_accuracy[2]/imgCount[2]) + '\n'
          + "UNDETECTED: " + str(undetected) + '\n'
          + "TOTAL:  " + str(sum(total_accuracy)/sum(imgCount)) + '\n')

    yolo.close_session()

FLAGS = None

def detect_img_one(yolo):
    path = input("Input image location: ")
    try:
        image = Image.open(path)
    except:
        print('Open Error! Try again!')
    else:
        r_image, accuracy = yolo.detect_image(image)
        #r_image.show()
        r_image.save( './out/' + path, 'PNG' )
    yolo.close_session()

if __name__ == '__main__':
    detect_img(YOLO())
    #detect_img_one(YOLO())
