# coding=utf-8
import unipath
import unittest
from .management.commands.makethememessages import _get_package_entries
from .management.commands.makethememessages import ThemeTranslationsException


class ParsersTest(unittest.TestCase):
    def test_load_entries(self):
        data_dir = unipath.Path(__file__).parent.child('test_data', 'proper')
        entries = _get_package_entries(data_dir)

        self.assertEqual(len(entries), 19)
        messages = [entry.msgid for entry in entries]
        expected_messages = [
            u'theme1_string1',
            u'theme1_indexed0',
            u'theme1_indexed1',
            u'theme1_indexed_nested0',
            u'theme1_indexed_nested1',
            u'theme2_string1',
            u'theme2_indexed0',
            u'theme2_indexed1',
            u'theme2_indexed_nested0',
            u'theme2_indexed_nested1',
            u'With this template you can highlight your most important products and services. Choose this template if you want to highlight the products you are offering and and give more visibility to your catalog',
            u'Catalog',
            u'Highlight your products and give more visibility to your catalog',
            u'You currently do not have any product in your catalog. Remember that you have chosen a product focused theme. You can create new products in the {catalog_link} section',
            u'theme4_string1',
            u'theme4_indexed0',
            u'theme4_indexed1',
            u'theme4_indexed_nested0',
            u'theme4_indexed_nested1',

        ]
        self.assertEqual(messages, expected_messages)
        occurrences = [entry.occurrences for entry in entries]
        expected_ocurrences = [
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/Marcos, Alfredo, Matías^2/Catalog/0.0.1', u'1')],
            [(u'package_json/Marcos, Alfredo, Matías^2/Catalog/0.0.1', u'1')],
            [(u'package_json/Marcos, Alfredo, Matías^2/Catalog/0.0.1', u'1')],
            [(u'package_json/Marcos, Alfredo, Matías^2/Catalog/0.0.1', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
            [(u'package_json/None/Test translation theme metadata/None', u'1')],
        ]
        self.assertEqual(occurrences, expected_ocurrences)

    def test_load_entries_with_missing_json(self):
        data_dir = unipath.Path(__file__).parent.child('test_data', 'invalid')
        with self.assertRaises(ThemeTranslationsException):
            _get_package_entries(data_dir)


if __name__ == '__main__':
    unittest.main()
