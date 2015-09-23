import os
import unittest
import yaml
import json
import gitenberg.metadata.marc as marc
import pymarc

from gitenberg.metadata.pandata import Pandata
from gitenberg.metadata.pg_rdf import pg_rdf_to_yaml


TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), '../samples/pandata.yaml')
TESTDATA_MARCFILENAME = os.path.join(os.path.dirname(__file__), '../samples/testoutput.marc.xml')
TESTDATA_PGRDFFILENAME = os.path.join(os.path.dirname(__file__), '../samples/pg20728.rdf')
TESTDATA_YAMLFILENAME = os.path.join(os.path.dirname(__file__), '../samples/testoutput.yaml')
EDITIONTEST_FILENAME = os.path.join(os.path.dirname(__file__), '../samples/editions.yaml')

class Yaml2MarcTest(unittest.TestCase):
    def setUp(self):
        self.pandata = Pandata(TESTDATA_FILENAME)
        
    def test_pandata(self):
        print self.pandata
        self.assertEqual( self.pandata.gutenberg_issued , "2007-03-03")
        self.assertTrue( isinstance( self.pandata.creator , dict))
        self.assertTrue( isinstance( self.pandata.subjects[0] , tuple ))
        self.assertEqual( self.pandata.subjects[0][0] , u'lcsh' )

    def test_marc(self):
        record = marc.stub(self.pandata)
        open(TESTDATA_MARCFILENAME,"w+").write(pymarc.record_to_xml(record))
        for field in record.get_fields('650'):
            
            self.assertEqual(field.get_subfields('a')[0],  'Science fiction')
            break
        for field in record.get_fields('100'):
            self.assertEqual(field.get_subfields('a')[0],  'Piper, H. Beam')
            break
        for field in record.get_fields('700'):
            self.assertEqual(field.get_subfields('4')[0],  'ill')
            break

class Rdf2YamlTest(unittest.TestCase):
        
    def test_conversion(self):
        yaml = pg_rdf_to_yaml(TESTDATA_PGRDFFILENAME)
        open(TESTDATA_YAMLFILENAME, "w+").write(yaml)
        pandata = Pandata(TESTDATA_YAMLFILENAME)
        self.assertEqual(pandata._edition,'book')
        self.assertTrue(pandata.subjects[0][0] in ('lcsh','lcc'))

class PandataTest(unittest.TestCase):
    def test_smart_properties(self):
        pandata = Pandata(TESTDATA_FILENAME)
        #print pandata.metadata
        self.assertEqual(pandata.publication_date,'2007-03-03')
        pandata.metadata["gutenberg_issued"] = None
        self.assertNotEqual(pandata.publication_date,'2007-03-03')
        self.assertEqual(pandata._edition,'Space-Viking')
        self.assertTrue(pandata.subjects[0][0] in ('lcsh','lcc'))

    def test_load_from_url(self):
        pandata = Pandata('https://github.com/gitenberg-dev/metadata/raw/master/samples/pandata.yaml')
        self.assertEqual(pandata._edition,'Space-Viking')
    
    def test_editions(self):
        pandata = Pandata(EDITIONTEST_FILENAME)
        (ed1,ed2) = pandata.get_edition_list()
        self.assertEqual(ed1.publisher, "Project Gutenberg")
        self.assertEqual(ed2.publisher, "Recovering the Classics")
        self.assertEqual(ed2.isbn, "9781111122223")
        self.assertEqual(ed1.isbn, "")


if __name__ == '__main__':
    unittest.main()