import unittest

from to_test import importWords

class TestSum(unittest.TestCase):
    def test_importWords(self):
        wordLists = ['./test_mock/wordlist_k.txt', './test_mock/wordlist_l.txt', './test_mock/wordlist_t.txt']
        print(importWords(wordLists))
        self.assertEqual(importWords(wordLists), [['하나', '둘'],['one', 'two'],['เอก', 'โท']])

if __name__ == '__main__':
    unittest.main()