#! /usr/bin/env python

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

__author__ = "Pablo ALINGERY"
__date__ = "$9 juin 2013 12:17:18$"

import unittest
from sitools2.clients.sdo_client_medoc import media_metadata_search
from sitools2.clients import constants

sitools2_url = constants.SITOOLS2_URL
functional_test = constants.FUNCTIONAL_TEST


@unittest.skipUnless(functional_test, "Functional Test " + sitools2_url + " interface ")
class Testidocmedoc(unittest.TestCase):        
    
    def setUp(self):
        pass

    def testMetadaSearch(self):
        print("\n####Test " + sitools2_url + " meta-data-search #######################")
        print("\n####hmi.sharp_cea_720s_nrt #################################")
        print("Test media_metadata_search")
        recnum_list = ['2075898', '2075899', '2075900', '2075902', '2075903', '2075904', '2075905', '2075940',
                       '2075938', '2075939']
        print(recnum_list)
        meta = media_metadata_search(keywords=['recnum', 'sunum', 'date__obs', 'quality', 'cdelt1', 'cdelt2', 'crval1'],
                                     series="hmi.sharp_cea_720s_nrt", recnum_list=recnum_list, server=sitools2_url)
        print(meta)

        self.assertEqual(len(meta), 10)


if __name__ == "__main__":
    unittest.main()
