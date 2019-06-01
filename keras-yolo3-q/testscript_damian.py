import unittest

import os


# NOTES
# i/o test: test the output based on input.
# exception test: test the type of exception based on wrong input format.

# TO DO
# code the tests in python unittest.
# please draw the testing tree too.
# write down the coverage.
# test the system using some test cases based on the coverage.
# record the result.

######################################################################################################
# from generate_dataset.py
######################################################################################################

# TEST 1. Have a sample file like words, check with the output list whether it contains all the words.
# coverage: all-edge, type: i/o
# wordDirs: paths to word pool file
# a word pool file consists of words delimited by newline
def importWords(wordDirs):
    words = []
    for dir in wordDirs:
        words.append([line.rstrip('\n') for line in open(dir, encoding='utf-8')])
    return words


# TEST 2. Remove every string in list which has no .otf or .ttf extension
# coverage: all-path, type: i/o
def removeNonFont(list):
    outList = []
    for font in list:
        if font[-4:] == ".otf" or font[-4:] == ".ttf":
            outList.append(font)
    return outList


# TEST 3. Check whether there are such file/directory in the specified path. If there is none, add. Else, leave it.
# coverage: node, type: i/o
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


######################################################################################################
# from scrimg_detect.py
######################################################################################################

# TEST 4. Import config and convert it into num_of_class (int) and class_mapping (dict)
# Coverage: all-path, type: i/o
# see utilities/config.txt
def import_config(path):
    f = open(path, 'r')
    classes = f.readlines()
    num_of_classes = len(classes)
    class_mapping = {}
    for c in classes:
        c = c.split()
        class_mapping[c[2]] = [c[0], int(c[1])]  # eg 'L' : 'latin' 0
    return num_of_classes, class_mapping


# TEST 5. Get language code from the mapping (dict).
# Coverage: edge, type: i/o, exception
# see import_config above for mapping format
def find_code(inp, mapping):
    for k, v in mapping.items():
        if str(inp) == str(v[0]) or str(inp) == str(v[1]) or inp == k:
            return k
    raise ValueError


# TEST 6. Get the division result of values in each categories in 2 dicts
# e.g. dict1 = {'L' : 0.4, 'K' : 0.7}, dict2 = {'L' : 0.1, 'K' : 0.1},
# return dict_res = {'L' : 4, 'K' : 7}
# Coverage: edge, type: None Exception test, i/o test
def divide_dict(dict1, dict2):
    dict_res = {}
    for k, v in dict1.items():
        try:
            dict_res[k] = dict1[k] / dict2[k]
        except ZeroDivisionError:
            dict_res[k] = 0
    return dict_res

##########################START OF THE TEST###############################
class TestSum(unittest.TestCase):

    # TEST 1. Have a sample file like words, check with the output list whether it contains all the words.
    # coverage: all-node, all-edge type: i/o
    # wordDirs: paths to word pool file
    # a word pool file consists of words delimited by newline
    def test_importWords(self):
        wordLists = ['./test_mock/wordlist_k.txt', './test_mock/wordlist_l.txt', './test_mock/wordlist_t.txt']
        l = importWords(wordLists)
        self.assertEqual(l, [['하나', '둘'], ['one', 'two'], ['เอก', 'โท']])

    # TEST 2. Remove every string in list which has no .otf or .ttf extension
    # coverage: all-path, type: i/o
    def test_removeNonFont(self):
        # 1-2-6
        fontList = []
        l = removeNonFont(fontList)
        self.assertEqual(l, [])

        # 1-2-3-4-2-6
        fontList = ['.DS_Store']
        l = removeNonFont(fontList)
        self.assertEqual(l, [])

        # 1-2-3-5-6
        fontList = ['x.ttf']
        l = removeNonFont(fontList)
        self.assertEqual(l, ['x.ttf'])

        # 1-2-3-4-5-6:
        fontList = ['x.otf']
        l = removeNonFont(fontList)
        self.assertEqual(l, ['x.otf'])

        # 1-2-3-4-2-3-5-6:
        fontList = ['.DS_Store', 'x.ttf']
        l = removeNonFont(fontList)
        self.assertEqual(l, ['x.ttf'])

        # 1-2-3-4-2-3-4-5-6:
        fontList = ['.DS_Store', 'x.otf']
        l = removeNonFont(fontList)
        self.assertEqual(l, ['x.otf'])

    # TEST 3. Check whether there are such file/directory in the specified path. If there is none, add. Else, leave it.
    # coverage: node, type: i/o
    def test_initializePaths(self):
        pass

    # TEST 4. Import config and convert it into num_of_class (int) and class_mapping (dict)
    # Coverage: all-path, type: i/o
    # see utilities/config.txt
    def import_config(self):
        pass

    # TEST 5. Get language code from the mapping (dict).
    # Coverage: edge, type: i/o
    # see import_config above for mapping format
    def find_code(self):
        pass

    # TEST 6. Get the division result of values in each categories in 2 dicts
    # e.g. dict1 = {'L' : 0.4, 'K' : 0.7}, dict2 = {'L' : 0.1, 'K' : 0.1},
    # return dict_res = {'L' : 4, 'K' : 7}
    # Coverage: edge, type: None Exception test, i/o test
    def mult_dict(self):
        pass

if __name__ == '__main__':
    unittest.main()
