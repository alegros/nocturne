import os
import comp
import unittest
import tempfile
from nocturne import *
from queries import *

class CompTestCase(unittest.TestCase):
    def setUp(self):
        #self.db_fd, comp.app.config['DATABASE'] = tempfile.mkstemp()
        comp.app.config['TESTING'] = True
        self.app = comp.app.test_client()

    """def tearDown(self):
        os.close(self.db_fd)
        os.unlink(comp.app.config['DATABASE'])"""
        
    def testGetDemon(self):
        rv = self.app.get('/demonList')
        self.assertTrue("Fallen - Flauros (68)" in rv.data)
        self.assertTrue("Tyrant - Beelzebub (Fly) (95)" in rv.data)
        self.assertTrue("Fiend - Hell Biker (42)" in rv.data)
    
    def testPostDemon(self):
        rv = self.app.post('/demonList', data=dict(demon='Pixie'))
        for line in CompTestCase.pixieData:
            self.assertTrue(line in rv.data)
    
    def test_from_db_row(self):
        pass
    
    pixieData = ["Pixie", "(Fairy) level 2 (2400 maccas)"\
        ,"HP 36"\
        ,"MP 24"\
        ,"Strength 3"\
        ,"Vitality 4"\
        ,"Magic 6"\
        ,"Agility 2"\
        ,"Luck 7"\
        ,"Resist:Elec"\
        ,"Dia"\
        ,"Zio"\
        ,"Seduce [3]"\
        ,"Rakunda [4]"\
        ,"Posumdi [5]"\
        ,"Wing Buffet [6]"\
        ,"In English mythology, they are fairies of the forest that love to play tricks on people. They can also be a hard worker when necessary."]

if __name__ == '__main__':
    unittest.main()
