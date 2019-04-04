import sys
import argparse
from yolo import YOLO#, detect_video
from PIL import Image
import os

def detect_img(yolo):
    path = "./Labeling/input/"
    for r, d, f in os.walk(path):
        for img in f:
            #print(img)
            try:
                image = Image.open(path + img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                r_image = yolo.detect_image(image)
                #r_image.show()
                r_image.save( './out/' + img, 'PNG' )
    yolo.close_session()

FLAGS = None

if __name__ == '__main__':
    detect_img(YOLO())
