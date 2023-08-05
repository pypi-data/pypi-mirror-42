#! /usr/bin/python

#    SITools2 client for Python
#    Copyright (C) 2013 - Institut d'astrophysique spatiale
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses

__author__="Pablo ALINGERY"
__date__ ="$8 janvier 2015 19:38:58$"

import unittest
from sitools2.core.pySitools2 import *
from sitools2.clients import constants

sitools2_url = constants.SITOOLS2_URL
functional_test = constants.FUNCTIONAL_TEST

@unittest.skipUnless(functional_test, 'Functional test skipped')
class TestSitools2Core(unittest.TestCase):        
    
    def setUp(self):
        pass
    
    def testNbProjects(self):
        print ("####Test "+sitools2_url +" nbr projects ###############")
        sitools2 = Sitools2Instance(sitools2_url)
        projects = sitools2.list_project()
        print(projects)
        self.assertEqual( len(projects), 1)           

if __name__ == '__main__':
    unittest.main()

