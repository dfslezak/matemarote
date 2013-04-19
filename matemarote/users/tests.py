"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User


class SimpleTest(TestCase):
    fixtures = ['testdata.json']
    
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        print ("USUARIOS: %s" % (User.objects.count(),))
        self.assertEqual(1 + 1, 2)
