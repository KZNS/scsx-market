import unittest
import sys
sys.path.append('../')
from market import create_app
app = create_app()

class TestThis(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass
    
    def test_test(self):
        res = self.app.get('/hello',follow_redirects=True)
        self.assertEqual(res.status_code,200)
        res = self.app.post('/hello')