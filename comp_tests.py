import os
import comp
import unittest
import tempfile

class CompTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, comp.app.config['DATABASE'] = tempfile.mkstemp()
        comp.app.config['TESTING'] = True
        self.app = comp.app.test_client()
        comp.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(comp.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
