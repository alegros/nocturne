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
        self.assertTrue(CompTestCase.pixieData[0] not in rv.data)
    
    def testPostDemon(self):
        rv = self.app.post('/demonList', data=dict(demon='Pixie'))
        for line in CompTestCase.pixieData:
            self.assertTrue(line in rv.data)
    
    pixieData = ["<p><b>Pixie</b>(Fairy) level 2 (2400 maccas)</p>"\
        ,"<span id='hp'>HP 36</span>"\
        ,"<span id='mp'>MP 24</span>"\
        ,"<span id='str'>Strength 3</span>"\
        ,"<span id='vit'>Vitality 4</span>"\
        ,"<span id='mag'>Magic 6</span>"\
        ,"<span id='agi'>Agility 2</span>"\
        ,"<span id='lck'>Luck 7</span>"\
        ,"<span id='aff'>Resist:Elec</span>"\
        ,"<span id='spell'>Dia</span>"\
        ,"<span id='spell'>Zio</span>"\
        ,"<span id='spell'>Seduce [3]</span>"\
        ,"<span id='spell'>Rakunda [4]</span>"\
        ,"<span id='spell'>Posumdi [5]</span>"\
        ,"<span id='spell'>Wing Buffet [6]</span>"\
        ,"<p>In English mythology, they are fairies of the forest that love to play tricks on people. They can also be a hard worker when necessary. </p>"]

if __name__ == '__main__':
    unittest.main()
