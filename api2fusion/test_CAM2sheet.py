import unittest, os
from unittest import *
from spreadsheet import *
import pygsheets


class TestCAM2sheet(unittest.TestCase):
    def setUp(self):
        self.service_file = 'service.json'
        self.assertTrue(os.path.isfile(self.service_file), \
                        msg='Service file is not in same directory or not named properly')


    def test___init__(self):

        #invalid service file name
        self.assertRaises(FileNotFoundError, CAM2sheet, service_file='service1', operation='open')

        #invlaid ID
        self.assertRaises(TypeError, CAM2sheet, id=123)

        #invalid name
        self.assertRaises(TypeError, CAM2sheet, name=[])




    def test_open(self):

        # gc = pygsheets.authorize(service_file=self.service_file)

        # wks = sheet.open()

        pass

    def test_create(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass

    def test_get_ids(self):
        pass

# if __name__ == '__main__':
#     unittest.main()


