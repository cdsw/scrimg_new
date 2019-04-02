import re
import cv2
import os

def main():
    countoffset = 0

    if not os.path.exists( "./input/" ):
        os.makedirs( "./input/" )
    if not os.path.exists( "./output/" ):
        os.makedirs( "./output/" )

    if not os.path.exists( "./filelist.txt" ):
        open( "filelist.txt", "a" ).close()

    if not os.path.exists( "./imgcount.txt" ):
        newfile = open( "imgcount.txt", "a" )
        newfile.write("0")
        newfile.close()

    with open( 'imgcount.txt', 'r' ) as fp:
        imgcount = int(fp.read())
    filelist = [line.rstrip( '\n' ) for line in open( 'filelist.txt' )]

    for root, dirs, files in os.walk( "./input", topdown=False ):
        for name in files:
            filename = name.split( "." )[:-1]
            filename = re.sub( r'[^\w]', '', str( filename ) )
            if filename in filelist:
                print( "File " + filename + " skipped (dupe)." )
                continue

            filepath = os.path.join( root, name )
            fExtArg = filepath.split( "." )[-1]
            if fExtArg not in ["jpg", "png", "jpeg"]:
                print("File " + filename + " skipped (not image).")
                continue

            img = cv2.imread( filepath )
            h, w, ch = img.shape
            max_dim = 352
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
            outputImg = cv2.imwrite( "./output/X" + \
                                     str( imgcount + countoffset ).zfill(5) + "_" + \
                                     str(filename) + ".jpg", procImg )

            filefl = open("filelist.txt", "a")
            filefl.write(str(filename)+"\n")
            filefl.close()

            countoffset += 1
            print("File " + filename + " processed successfully.")

    fileic = open( "imgcount.txt", "w" )
    fileic.write( str( imgcount + countoffset ) )
    fileic.close()

    print("End: " + str(countoffset) + " files processed.")

if __name__ == "__main__":
    main()
