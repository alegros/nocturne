import os
import unittest
import tempfile

from compendium import Compendium

class CompendiumTestCase(unittest.TestCase):
    def setUp(self):
        self.cmp = Compendium()

    '''Tests to check the consistancy and proper ordering of the collections of the compendium.
    Tests names are : 'test_cmp_' + collection_to_check
    '''
    def test_cmp_races(self):
        self.assertTrue(self.cmp.races['Night'][9] == 'Lilith')
        self.assertTrue(self.cmp.races['Brute'][4] == 'Shiki-Ouji')

    def test_cmp_demons(self):
        self.assertTrue(self.cmp.demons['Pixie'].lv == 2)

    def test_cmp_rules(self):
        pass

    def test_cmp_fiends(self):
        pass

    def test_cmp_evolutions(self):
        pass

    def test_cmp_specials(self):
        pass

    def test_cmp_elements_set(self):
        pass

    def test_cmp_affinities_set(self):
        pass

    def test_cmp_demons_list(self):
        pass

    def test_cmp_races_list(self):
        pass

    '''Fusion tests
    '''
    def test_fuse(self):
        '''Checks a basic fusion and a fusions without a result'''
        pass

    def test_fuse_element(self):
        '''Checks the fusion of two demons of the same family into an element'''
        pass

    def test_fuse_mitama(self):
        '''Checks the fusion of two elements into a mitama'''
        pass
    
    '''Reverse fusion tests
    Tests for all possible outcomes of find_parents
    given children with various fusion types (fs_type).
    Names are : test_find_parents_x where x is a fusion_type'''
    def test_find_parents_0(self):
        '''Demons obtainable via basic fusions'''
        pass

    def test_find_parents_1(self):
        '''Demons obtainable via mythologic fusions, or fusions with
        a mythological background that does not follow the standard rules.'''
        pass

    def test_find_parents_2(self):
        '''Evolutions'''
        pass

    def test_find_parents_3(self):
        '''Fiend fusions. What races to fuse and kagutsuhi phase required.'''
        pass

    def test_find_parents_element(self):
        '''How to obtain an element'''
        pass

    def test_find_parents_mitama(self):
        '''How to obtain a mitama'''
        pass

    def test_find_parents_races(self):
        '''Basically a test on the content of cmp.rules'''
        pass

if __name__ == '__main__':
    unittest.main()

'''
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
'''
