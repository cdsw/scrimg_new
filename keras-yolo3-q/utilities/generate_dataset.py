import os
from random import randint

from PIL import Image, ImageDraw, ImageFont, ImageFilter


class DatasetGenerator:
    def __init__(self, version):
        self.initializePaths()
        self.labels = ["Latin", "Thai", "Korean"]
        self.wordDirs = ['./dataset/words/latnWords.txt', './dataset/words/thaiWords.txt', './dataset/words/kornWords.txt']
        self.fontDirs = ['./dataset/fonts/Latin/', './dataset/fonts/Thai/', './dataset/fonts/Korean/']
        self.scriptCodes = ['L', 'T', 'K']
        self.fonts = self.initializeFonts()
        self.words = self.importWords()
        self.fontSizeDivisors = [(13, 7.5), (10, 7), (13, 7.5)]
        self.countOffset = 0
        with open('./dataset/imgcount.txt', 'r') as fp:
            self.imgCount = int(fp.read())
        self.version = version

        self.draw = False

    ######################################################################################################
    # to_test. Have a sample file like words, check with the output list whether it contains all the words.
    # coverage: all-edge and all-node.
    def importWords(self):
        words = []
        for dir in self.wordDirs:
            words.append([line.rstrip('\n') for line in open(dir, encoding='utf-8')])
        return words

    @staticmethod
    def removeNonFont(list):
        outList = []
        for font in list:
            if font[-4:] == ".otf" or font[-4:] == ".ttf":
                outList.append(font)
        return outList

    def initializeFonts(self):
        fonts = []
        for dir in self.fontDirs:
            fonts.append(DatasetGenerator.removeNonFont(os.listdir(dir)))
        return fonts

    @staticmethod
    def initializePaths():
        if not os.path.exists("./dataset/output/"):
            os.makedirs("./dataset/output/")

        if not os.path.exists("./dataset/filelist.txt"):
            open("./dataset/filelist.txt", "a").close()

        if not os.path.exists("./dataset/imgcount.txt"):
            newfile = open("./dataset/imgcount.txt", "a")
            newfile.write("0")
            newfile.close()

        if not os.path.exists("./dataset/fonts/"):
            os.makedirs("./dataset/fonts/")

        if not os.path.exists("./dataset/words/latnWords.txt"):
            open("./dataset/latnWords.txt", "a").close()
        if not os.path.exists("./dataset/words/thaiWords.txt"):
            open("./dataset/thaiWords.txt", "a").close()
        if not os.path.exists("./dataset/words/kornWords.txt"):
            open("./dataset/kornWords.txt", "a").close()

    def fontRand(self, script):
        num = randint(0, len(self.fonts[script]) - 1)
        return self.fontDirs[script] + self.fonts[script][num]

    def generateWords(self, wordlist, amountMin, amountMax, randomCase=False):
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

    @staticmethod
    def generateString(list, space=" "):
        outStr = ""
        for i in range(len(list)):
            outStr += list[i] + space
        return outStr

    @staticmethod
    def generateTextCol(mode):
        if mode == 0 or mode == 'bw':
            rand = randint(0, 50)
            red = blue = green = rand
        else:
            red = randint(0, 50)
            green = randint(0, 50)
            blue = randint(0, 50)
        return red, green, blue

    @staticmethod
    def generateBgCol(mode):
        base = randint(230, 255)
        if mode == 0 or mode == 'bw':
            red = green = blue = base
        elif mode == 'm':
            red = 255
            green = 255
            blue = 255
        else:
            red = randint(base - 5, base + 5)
            green = randint(base - 5, base + 5)
            blue = randint(base - 5, base + 5)
        return red, green, blue

    @staticmethod
    def applyBlur(image, mode):
        if mode == 'm':
            return image
        else:
            blurFactor = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.3, 0.4, 0.4, 0.5,
                          0.6, 0.8, 1, 1.2]
            num = randint(0, len(blurFactor) - 1)
            blurred_image = image.filter(ImageFilter.GaussianBlur(radius=blurFactor[num]))
            return blurred_image

    def generateAnnotation(self, filename, script_class, topLeft, bottomRight):
        annot_file = open('./dataset/annotation-' + self.version + '.txt', 'a')
        annot_file.write(filename + ' ' + str(topLeft[0]) + ',' + str(topLeft[1]) + ',' + \
                         str(bottomRight[0]) + ',' + str(bottomRight[1]) + ',' + str(script_class) + '\n')
        annot_file.close()

    def generateImage(self, scriptChoice, mode):
        randomFactors = [randint(90, 120) / 100, randint(75, 110) / 100]
        w = int(256 * randomFactors[0])
        h = int(256 * randomFactors[1])
        img = Image.new('RGB', (w, h), color=DatasetGenerator.generateBgCol(mode))
        fntChoice = self.fontRand(scriptChoice)
        d = ImageDraw.Draw(img)

        randY = randint(1, (h // 14) * 11)
        randX = randint(1, w // 25)
        randPosi = (randX, randY)

        spacings = [" ", "", " "]
        randomCases = [True, False, False]
        spaceEndings = ["", " ", ""]

        text_ = self.generateString(self.generateWords(self.words[scriptChoice], 3, 5,
                                                       randomCase=randomCases[scriptChoice]),
                                    space=spacings[scriptChoice]) + spaceEndings[scriptChoice]

        divisor = self.fontSizeDivisors[scriptChoice]
        font_ = ImageFont.truetype(fntChoice, randint(w // divisor[0], w // divisor[1]))

        d.text(randPosi, text_, font=font_, fill=DatasetGenerator.generateTextCol(mode))

        textWithoutEndSpace = text_[:-1]
        textSize = d.textsize(textWithoutEndSpace, font=font_)

        point1 = randPosi
        point2 = (min(randPosi[0] + textSize[0], w), randPosi[1] + textSize[1])
        if self.draw:
            d.rectangle([point1, point2], outline='red')

            labelText = self.labels[scriptChoice]
            labelFont = ImageFont.truetype('./dataset/fonts/Latin/SourceSansPro-Bold.ttf', 18)
            labelTextSize = d.textsize(labelText, font=labelFont)

            point3 = (point1[0], point1[1] - labelTextSize[1])
            point4 = (point1[0] + labelTextSize[0], point1[1])
            d.rectangle([point3, point4], fill='red')
            d.text(point3, labelText, font=labelFont, fill='white')

        img = DatasetGenerator.applyBlur(img, mode)

        # ==============================
        filename = "./dataset/output/" + self.scriptCodes[scriptChoice] + "_" + \
                   str(self.imgCount + self.countOffset).zfill(7) + "-" + self.version + ".jpg"
        img.save(filename)

        filefl = open("./dataset/filelist.txt", "a")
        filefl.write(str(filename) + "\n")
        filefl.close()

        self.countOffset += 1
        print_trace = False
        if print_trace:
            print("==> File " + filename + " processed successfully.")
            print("    TEXT FONT: " + str(fntChoice))
            print("    TEXT POSI: " + str(randPosi))
            print("    TEXT SIZE: " + str(textSize))
        self.generateAnnotation(filename, scriptChoice, point1, point2)

    def saveImgCount(self):
        fileic = open("./dataset/imgcount.txt", "w")
        fileic.write(str(self.imgCount + self.countOffset))
        fileic.close()

    def generateAllScripts(self, genAmount, mode=''):
        for choice in range(len(self.scriptCodes)):
            for i in range(genAmount):
                self.generateImage(choice, mode)
        print("End: " + str(self.countOffset) + " files processed.")
        self.saveImgCount()

    def set_version(self, version):
        self.version = version

#s = DatasetGenerator()
#s.generateAllScripts(18, 'bw')
