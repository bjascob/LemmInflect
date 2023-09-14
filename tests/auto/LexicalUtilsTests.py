import unittest
from lemminflect.core import LexicalUtils


class LexicalUtilsTests(unittest.TestCase):

    def test_applyCapsStyle_lower(self):
        self.assertEqual(LexicalUtils.applyCapsStyle('have', 'lower'), 'have')
        self.assertEqual(LexicalUtils.applyCapsStyle('Have', 'lower'), 'have')
        self.assertEqual(LexicalUtils.applyCapsStyle('HAVE', 'lower'), 'have')


    def test_applyCapsStyle_first_upper(self):
        self.assertEqual(LexicalUtils.applyCapsStyle('have', 'first_upper'), 'Have')
        self.assertEqual(LexicalUtils.applyCapsStyle('Have', 'first_upper'), 'Have')
        self.assertEqual(LexicalUtils.applyCapsStyle('HAVE', 'first_upper'), 'Have')


    def test_applyCapsStyle_all_upper(self):
        self.assertEqual(LexicalUtils.applyCapsStyle('have', 'all_upper'), 'HAVE')
        self.assertEqual(LexicalUtils.applyCapsStyle('Have', 'all_upper'), 'HAVE')
        self.assertEqual(LexicalUtils.applyCapsStyle('HAVE', 'all_upper'), 'HAVE')

    
    def test_applyCapsStyle_invalid_style(self):
        with self.assertRaises(ValueError) as e:
            LexicalUtils.applyCapsStyle('have', 'invalid_style')
        self.assertTrue('Invalid caps style = invalid_style' in str(e.exception))

    
    def test_getCapsStyle(self):
        self.assertEqual(LexicalUtils.getCapsStyle('have'), 'lower')
        self.assertEqual(LexicalUtils.getCapsStyle('havE'), 'lower')
        self.assertEqual(LexicalUtils.getCapsStyle('Have'), 'first_upper')
        self.assertEqual(LexicalUtils.getCapsStyle('HAve'), 'first_upper')
        self.assertEqual(LexicalUtils.getCapsStyle('HAVE'), 'all_upper')

    
    def test_categoryToUPos(self):
        self.assertEqual(LexicalUtils.categoryToUPos('noun'), 'NOUN')
        self.assertEqual(LexicalUtils.categoryToUPos('modal'), 'AUX')


    def test_uposToCategory(self):
        self.assertEqual(LexicalUtils.categoryToUPos('NOUN'), 'noun')
        self.assertEqual(LexicalUtils.categoryToUPos('PROPN'), 'noun')
