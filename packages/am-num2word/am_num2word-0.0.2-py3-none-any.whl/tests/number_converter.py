# -*- coding: utf-8 -*-
import unittest
from am_num2number import Number2WordsConverter


class Number2WordConverterTest(unittest.TestCase):
    def test_to_words(self):
        converter = Number2WordsConverter(0)
        self.assertEqual(converter.to_words(), "ዜሮ")
        converter = Number2WordsConverter(10)
        self.assertEqual(converter.to_words(), "አስር")
        converter = Number2WordsConverter(19)
        self.assertEqual(converter.to_words(), "አስራ ዘጠኝ")
        converter = Number2WordsConverter(200)
        self.assertEqual(converter.to_words(), "ሁለት መቶ")
        
        converter = Number2WordsConverter(350)
        self.assertEqual(converter.to_words(), "ሶስት መቶ አምሳ")


 