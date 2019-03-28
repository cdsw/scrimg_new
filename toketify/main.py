import cv2
import os
import shutil

def main():
    imgCount = 0;

    if not os.path.exists( "./input/" ):
        os.makedirs( "./input/" )

    if os.path.exists( "./output/" ):
        shutil.rmtree( "./output/" )
    else:
        os.makedirs( "./output/" )

    for root, dirs, files in os.walk( "./input", topdown=False ):
        for name in files:
            filepath = os.path.join( root, name )

            fExtArg = filepath.split( "." )[-1]

            if fExtArg not in ["jpg", "png", "jpeg"]:
                continue

            img = cv2.imread( filepath )
            h, w, ch = img.shape
            max_dim = 416
            #resize image
            if h >= w:
                new_h, new_w = max_dim, int(max_dim/h * w)
            elif w > h:
                new_h, new_w = int(max_dim/w * h), max_dim

            new_dim = new_w, new_h
            img = cv2.resize(img, new_dim, interpolation = cv2.INTER_AREA)
            h, w, ch = img.shape
            
            wpad = 0;
            hpad = 0;
            
            if h >= w:
                wpad = (h - w)//2
            elif w > h:
                hpad = (w - h)//2
        

            procImg = cv2.copyMakeBorder(
                img,
                hpad,
                hpad,
                wpad,
                wpad,
                cv2.BORDER_CONSTANT,
                value=(0, 0, 0)
            )
            outputImg = cv2.imwrite( "./output/X" + str( imgCount ).zfill(5) + ".jpg", procImg )
            
            imgCount += 1

if __name__ == "__main__":
    main()
