import os
from enum import Enum
from random import randint

from PIL import Image, ImageDraw, ImageFont


class Script(Enum):
    LATN = 0
    THAI = 1
    KORN = 2


def initial(num):
    if int(num) == Script.LATN.value:
        return "L"
    elif int(num) == Script.THAI.value:
        return "T"
    elif int(num) == Script.KORN.value:
        return "K"


def initialisePaths():
    if not os.path.exists("./output/"):
        os.makedirs("./output/")

    if not os.path.exists("./filelist.txt"):
        open("filelist.txt", "a").close()

    if not os.path.exists("./imgcount.txt"):
        newfile = open("imgcount.txt", "a")
        newfile.write("0")
        newfile.close()

    if not os.path.exists("./fonts/"):
        os.makedirs("./fonts/")

    if not os.path.exists("./words/latnWords.txt"):
        open("latnWords.txt", "a").close()
    if not os.path.exists("./words/thaiWords.txt"):
        open("thaiWords.txt", "a").close()
    if not os.path.exists("./words/kornWords.txt"):
        open("kornWords.txt", "a").close()


def begoneFolder(list):
    outList = []
    for font in list:
        if font[-4:] == ".otf" or font[-4:] == ".ttf":
            outList.append(font)
    return outList


latnFonts = begoneFolder(os.listdir('./fonts/Latin/'))
thaiFonts = begoneFolder(os.listdir('./fonts/Thai/'))
kornFonts = begoneFolder(os.listdir('./fonts/Korean/'))


def fontRand(script):
    if script == 0:  # Latin
        num = randint(0, len(latnFonts) - 1)
        return './fonts/Latin/' + latnFonts[num]
    elif script == 1:  # Thai
        num = randint(0, len(thaiFonts) - 1)
        return './fonts/Thai/' + thaiFonts[num]
    elif script == 2:  # Korean
        num = randint(0, len(kornFonts) - 1)
        return './fonts/Korean/' + kornFonts[num]


def generateWords(wordlist, amountMin, amountMax, randomCase=False):
    wordIndices = []
    outList = []
    for i in range(randint(amountMin, amountMax)):
        wordIndices.append(randint(0, len(wordlist) - 1))
    for i in range(len(wordIndices)):
        if randomCase == True:
            case = randint(0, 2)  # 0 = lower, 1 = UPPER, 2 = Title
            if case == 0:
                outList.append(wordlist[wordIndices[i]].lower())
            elif case == 1:
                outList.append(wordlist[wordIndices[i]].upper())
            elif case == 2:
                outList.append(wordlist[wordIndices[i]].capitalize())
        else:
            outList.append(wordlist[wordIndices[i]])
    return outList


def generateString(list, space=" "):
    outStr = ""
    for i in range(len(list)):
        outStr += list[i] + space
    return outStr


def generateColour():
    red = randint(0, 100)
    green = randint(0, 100)
    blue = randint(0, 100)
    return (red, green, blue)


# GLOBALS
initialisePaths()

countoffset = 0

with open('imgcount.txt', 'r') as fp:
    imgcount = int(fp.read())
# filelist = [line.rstrip( '\n' ) for line in open( 'filelist.txt' )]

# INP STRINGS FILE
latnWords = [line.rstrip('\n') for line in open('./words/latnWords.txt', encoding='utf-8')]
thaiWords = [line.rstrip('\n') for line in open('./words/thaiWords.txt', encoding='utf-8')]
kornWords = [line.rstrip('\n') for line in open('./words/kornWords.txt', encoding='utf-8')]


def generateImage(scriptChoice, genAmount):
    global countoffset
    w = 256
    h = 256
    img = Image.new( 'RGB', (w, h), color='white' )
    fntChoice = fontRand( scriptChoice )
    fnt = ImageFont.truetype( fntChoice, randint( w // 12, w // 8 ) )
    d = ImageDraw.Draw( img )
    text = ""

    randY = randint( h // 7, (h // 7) * 6 )
    randX = randint( w // 50, w // 20 )
    randPosi = (randX, randY)

    if scriptChoice == 0:
        text = generateString(generateWords(latnWords, 3, 5, randomCase=True))

    elif scriptChoice == 1:
        text = generateString(generateWords(thaiWords, 3, 5), space="")
        text = text + " "
        fnt = ImageFont.truetype(fntChoice, randint(w // 10, w // 6))

    elif scriptChoice == 2:
        text = generateString(generateWords(kornWords, 3, 5))

    d.text(randPosi, text, font=fnt, fill=generateColour())

    draw = False

    # ==============================
    textWithoutEndSpace = text[:-1]
    textSize = d.textsize(textWithoutEndSpace, font=fnt)

    point1 = randPosi
    point2 = (min(randPosi[0] + textSize[0], w), randPosi[1] + textSize[1])
    if draw:
        d.rectangle([point1, point2], outline='red')

    labelText = ""
    if scriptChoice == 0:
        labelText = "Latin"
    elif scriptChoice == 1:
        labelText = "Thai"
    elif scriptChoice == 2:
        labelText = "Korean"
    labelFont = ImageFont.truetype('./fonts/Latin/SourceSansPro-Bold.ttf', 18)
    labelTextSize = d.textsize(labelText, font=labelFont)

    # ==============================
    point3 = (point1[0], point1[1] - labelTextSize[1])
    point4 = (point1[0] + labelTextSize[0], point1[1])
    if draw:
        d.rectangle([point3, point4], fill='red')
        d.text(point3, labelText, font=labelFont, fill='white')

    # ==============================
    filename = "./output/" + str(initial(scriptChoice)) + "_" + \
               str(imgcount + countoffset).zfill(5) + ".jpg"
    img.save(filename)

    filefl = open("filelist.txt", "a")
    filefl.write(str(filename) + "\n")
    filefl.close()

    countoffset += 1
    print_trace = False
    if print_trace:
        print("==> File " + filename + " processed successfully.")
        print("    TEXT FONT: " + str(fntChoice))
        print("    TEXT POSI: " + str(randPosi))
        print("    TEXT SIZE: " + str(textSize))
    generateAnnotation(filename, scriptChoice, point1, point2)


def generateAnnotation(filename, script_class, topLeft, bottomRight):
    annot_file = open('annotation.txt', 'a')
    filename = './mokemify' + filename[1:]
    annot_file.write(filename + ' ' + str(topLeft[0]) + ',' + str(topLeft[1]) + ',' + \
                     str(bottomRight[0]) + ',' + str(bottomRight[1]) + ',' + str(script_class) + '\n')
    annot_file.close()


def main():
    # scriptChoice = int( input( "Generate images in which script?\n" + \
    #                           "(LATN = 0, THAI = 1, KORN = 2) : " ) )
    genAmount = int(input("How many images to generate? : "))

    # GENERATE
    for choice in range( 3 ):
        for i in range( genAmount ):
            generateImage( choice, genAmount )

    fileic = open("imgcount.txt", "w")
    fileic.write(str(imgcount + countoffset))
    fileic.close()

    print("End: " + str(countoffset) + " files processed.")


if __name__ == "__main__":
    main()
