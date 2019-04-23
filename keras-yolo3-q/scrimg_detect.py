import sys
import argparse
from yolo import YOLO#, detect_video
from PIL import Image
import os

def detect_img(yolo):
    path = "./Labeling/input/"
    imgCount = 0
    total_accuracy = 0
    for r, d, f in os.walk(path):
        for img in f:
            try:
                image = Image.open(path + img)
                imgCount += 1
            except:
                print('Open Error! Try again!')
                continue
            else:
                # Temporary
                c = ''
                if img[7] == 'L':
                    c = 'latin'
                elif img[7] == 'K':
                    c = 'korean'
                elif img[7] == 'T':
                    c = 'thai'
                r_image, accuracy = yolo.detect_image(image, c)
                #r_image.show()
                r_image.save( './out/' + img, 'PNG' )
                print("acc: " + str(accuracy) + " tot: " + str(total_accuracy) + " img ct " + str(imgCount))
                total_accuracy += accuracy
    print("TOTAL_ACCURACY = " + str(total_accuracy/imgCount))
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
    #detect_img(YOLO())
    detect_img_one(YOLO())
