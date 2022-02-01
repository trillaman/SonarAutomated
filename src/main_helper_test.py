import unittest
from main_helper import *


class TestHelper(unittest.TestCase):
    def test_set_slashes(self):
        self.assertEqual(set_slashes("/home/trilla/sonar_automated/test"), '\\home\\trilla\\sonar_automated\\test')

    def test_get_filename(self):
        self.assertEqual(get_filename('\\home\\trilla\\sonar_automated\\test.txt'), 'test')

    def test_get_file_extension(self):
        self.assertEqual(get_file_extension('\\home\\trilla\\sonar_automated\\test.txt'), 'txt')
    '''
    def test_get_project_name(self):
        self.assertEqual(SonarModule.get_project_name(self, './wp-plugins-extracted/amp'), 'amp')
    '''