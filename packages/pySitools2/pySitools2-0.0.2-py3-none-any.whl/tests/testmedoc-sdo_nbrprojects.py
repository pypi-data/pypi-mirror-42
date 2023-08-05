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

__author__="Jean-Christophe Malapert"
__date__ ="$9 juin 2013 11:38:58$"

import unittest
from sitools2.core.pySitools2 import *

@unittest.skip("Functional Test medoc-sdo interface")
class TestSitools2Core(unittest.TestCase):        
    
    def setUp(self):
        pass
    
    def testNbProjects(self):
        print ("####Test media nbr projects #################################")
        sitools2 = Sitools2Instance('http://medoc-sdo.ias.u-psud.fr')
        projects = sitools2.list_project()
        self.assertEqual( len(projects), 2)           
    

if __name__ == '__main__':
    unittest.main()
