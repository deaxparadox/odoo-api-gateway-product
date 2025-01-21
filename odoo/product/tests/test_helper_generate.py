from django.test import TestCase
from helpers import generate

class TestHelperGenerate(TestCase):
    def test_generate_uuid(self):
        u = generate.generate_uuid4()
        self.assertEqual(type(u), str)
        
    def test_generate_random_num_from(self):
        # both int
        n = generate.generate_rand_number_from(1, 5)
        self.assertEqual(type(n), int)
        
        # both float
        n = generate.generate_rand_number_from(1., 5.)
        self.assertEqual(type(n), float)
        
        # either int or float
        n = generate.generate_rand_number_from(1, 5.)
        self.assertEqual(type(n), float)
        n = generate.generate_rand_number_from(1., 5)
        self.assertEqual(type(n), float)