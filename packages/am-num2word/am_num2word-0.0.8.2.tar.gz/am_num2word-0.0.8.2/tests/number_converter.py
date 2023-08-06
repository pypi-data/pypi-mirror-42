# -*- coding: utf-8 -*-
import unittest
from am_num2word import Number2WordsConverter


class Number2WordConverterTest(unittest.TestCase):
    def test_to_words(self):
        
        
        converter:Number2WordsConverter = Number2WordsConverter(23203)
        self.assertEqual(converter.to_words(), "ሃያ ሶስት ሺህ ሁለት መቶ ሶስት")
        converter:Number2WordsConverter = Number2WordsConverter(437343)
        self.assertEqual(converter.to_words(),
                         "አራት መቶ ሰላሳ ሰባት ሺህ ሶስት መቶ አርባ ሶስት")
        converter: Number2WordsConverter = Number2WordsConverter(43050703)
        self.assertEqual(converter.to_words(),
                         "አርባ ሶስት ሚሊዮን ሃምሳ ሺህ ሰባት መቶ ሶስት")

    def test_to_coma_separated(self):
        converter: Number2WordsConverter = Number2WordsConverter(0)
        self.assertEqual(converter.coma_separated, "0")
        
    def test_to_words_single_digit(self):
        converter: Number2WordsConverter = Number2WordsConverter(0)
        self.assertEqual(converter.to_words(), "ዜሮ")
        converter: Number2WordsConverter = Number2WordsConverter(1)
        self.assertEqual(converter.to_words(), "አንድ")
        converter: Number2WordsConverter = Number2WordsConverter(2)
        self.assertEqual(converter.to_words(), "ሁለት")
        converter: Number2WordsConverter = Number2WordsConverter(9)
        self.assertEqual(converter.to_words(), "ዘጠኝ")
    def test_to_words_double_digit(self):
        converter: Number2WordsConverter = Number2WordsConverter(10)
        self.assertEqual(converter.to_words(), "አስር")
        converter: Number2WordsConverter = Number2WordsConverter(19)
        self.assertEqual(converter.to_words(), "አስራ ዘጠኝ")
    def test_to_words_hundreds(self):
        converter: Number2WordsConverter = Number2WordsConverter(200)
        self.assertEqual(converter.to_words(), "ሁለት መቶ")

        converter: Number2WordsConverter = Number2WordsConverter(350)
        self.assertEqual(converter.to_words(), "ሶስት መቶ ሃምሳ")
        
        converter: Number2WordsConverter = Number2WordsConverter(999)
        self.assertEqual(converter.to_words(), "ዘጠኝ መቶ ዘጠና ዘጠኝ")


    def test_to_words_thousends(self):
        converter: Number2WordsConverter = Number2WordsConverter(5000)
        self.assertEqual(converter.to_words(), "አምስት ሺህ")

        converter: Number2WordsConverter = Number2WordsConverter(1400)
        self.assertEqual(converter.to_words(), "አንድ ሺህ አራት መቶ")

        converter: Number2WordsConverter = Number2WordsConverter(8670)
        self.assertEqual(converter.to_words(), "ስምንት ሺህ ስድስት መቶ ሰባ")

        converter: Number2WordsConverter = Number2WordsConverter(12970)
        self.assertEqual(converter.to_words(), "አስራ ሁለት ሺህ ዘጠኝ መቶ ሰባ")
        
        converter: Number2WordsConverter = Number2WordsConverter(972140)
        self.assertEqual(converter.to_words(), "ዘጠኝ መቶ ሰባ ሁለት ሺህ አንድ መቶ አርባ")

        converter: Number2WordsConverter = Number2WordsConverter(500232)
        self.assertEqual(converter.to_words(), "አምስት መቶ ሺህ ሁለት መቶ ሰላሳ ሁለት")

        converter: Number2WordsConverter = Number2WordsConverter(501232)
        self.assertEqual(converter.to_words(), "አምስት መቶ አንድ ሺህ ሁለት መቶ ሰላሳ ሁለት")

    def test_to_words_millions(self):
        converter: Number2WordsConverter = Number2WordsConverter(1000000)
        self.assertEqual(converter.to_words(), "አንድ ሚሊዮን")
        converter: Number2WordsConverter = Number2WordsConverter(1000001)
        self.assertEqual(converter.to_words(), "አንድ ሚሊዮን አንድ")
        converter: Number2WordsConverter = Number2WordsConverter(1000010)
        self.assertEqual(converter.to_words(), "አንድ ሚሊዮን አስር")
        
        converter: Number2WordsConverter = Number2WordsConverter(1000520)
        self.assertEqual(converter.to_words(), "አንድ ሚሊዮን አምስት መቶ ሃያ")
        
        converter: Number2WordsConverter = Number2WordsConverter(1001520)
        self.assertEqual(converter.to_words(), "አንድ ሚሊዮን አንድ ሺህ አምስት መቶ ሃያ")

        converter: Number2WordsConverter = Number2WordsConverter(1071520)
        self.assertEqual(converter.to_words(), "አንድ ሚሊዮን ሰባ አንድ ሺህ አምስት መቶ ሃያ")

        converter: Number2WordsConverter = Number2WordsConverter(1671520)
        self.assertEqual(converter.to_words(),
                         "አንድ ሚሊዮን ስድስት መቶ ሰባ አንድ ሺህ አምስት መቶ ሃያ")

    def test_float_numbers(self):
        converter: Number2WordsConverter = Number2WordsConverter(1000000.0)
        self.assertEqual(converter.to_words(), "አንድ ሚሊዮን ነጥብ ዜሮ")
        converter: Number2WordsConverter = Number2WordsConverter(1000001.12)
        self.assertEqual(converter.to_words(), "አንድ ሚሊዮን አንድ ነጥብ አንድ ሁለት")
        converter: Number2WordsConverter = Number2WordsConverter(1000010.4566, 3)
        self.assertEqual(converter.to_words(), "አንድ ሚሊዮን አስር ነጥብ አራት አምስት ሰባት")

        converter: Number2WordsConverter = Number2WordsConverter(1000010.4566, 4)
        self.assertEqual(converter.to_words(),
                         "አንድ ሚሊዮን አስር ነጥብ አራት አምስት ስድስት ስድስት")
    def test_negative_Numbers(self):
        converter: Number2WordsConverter = Number2WordsConverter(-1000520)
        self.assertEqual(converter.to_words(), "ነጌትቭ አንድ ሚሊዮን አምስት መቶ ሃያ")

        converter: Number2WordsConverter = Number2WordsConverter(-1001520)
        self.assertEqual(converter.to_words(),
                         "ነጌትቭ አንድ ሚሊዮን አንድ ሺህ አምስት መቶ ሃያ")

        converter: Number2WordsConverter = Number2WordsConverter(-1071520)
        self.assertEqual(converter.to_words(),
                         "ነጌትቭ አንድ ሚሊዮን ሰባ አንድ ሺህ አምስት መቶ ሃያ")

        converter: Number2WordsConverter = Number2WordsConverter(-1671520)
        self.assertEqual(converter.to_words(),
                         "ነጌትቭ አንድ ሚሊዮን ስድስት መቶ ሰባ አንድ ሺህ አምስት መቶ ሃያ")
