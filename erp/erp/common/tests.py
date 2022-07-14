from django.test import TestCase
from erp.common.helpers import epochdate


class HelpersTestCase(TestCase):
    def test_functions(self):
        """All helpers are working properly"""
        self.assertEqual(epochdate(1023456427), ('2002-06-07', '13:27:07'))  # Localized!
