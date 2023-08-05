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

__author__="Pablo ALINGERY"
__date__ ="$9 juin 2013 12:17:18$"

import unittest
from sitools2.clients.sdo_client_medoc import media_search
from datetime import datetime, timedelta
from sitools2.clients import constants

sitools2_url = constants.SITOOLS2_URL
functional_test = constants.FUNCTIONAL_TEST

d1 = datetime(2016, 8, 10, 0, 0, 0)
d2 = d1 + timedelta(days=1)


@unittest.skipUnless(functional_test,"Functional test "+ sitools2_url +" interface ")
class Testsearch(unittest.TestCase):
    
    def setUp(self):
        print ("####Test "+ sitools2_url +"_search #############################")

    def testSearch_sharp_720s_nrt(self):
        print ("#### hmi.sharp_720s_nrt ################################")

        sdo_data_list = media_search( 
        	server=sitools2_url,
        	dates = [d1,d2],
        	series = 'hmi.sharp_720s_nrt',
        	cadence = ['12 min'] )
        print(sdo_data_list[0:3])
        self.assertEqual( len(sdo_data_list), 861)

    def testSearch_sharp_cea_720s_nrt(self):
        print("#### hmi.sharp_cea_720s_nrt ################################")
        sdo_data_list = media_search(
            server = sitools2_url,
            dates = [d1, d2],
            series = 'hmi.sharp_cea_720s_nrt',
            cadence = ['12 min'])
        print(sdo_data_list[0:3])
        self.assertEqual(len(sdo_data_list), 861)

    def testSearch_ic_nolimbdark_720s_nrt(self):
        print("####hmi.ic_nolimbdark_720s_nrt #########################")
        sdo_data_list = media_search(
        	server = sitools2_url,
        	dates = [d1,d2],
        	series = 'hmi.ic_nolimbdark_720s_nrt',
        	cadence = ['12 min'] )
        print(sdo_data_list[0:3])
        self.assertEqual( len(sdo_data_list), 120)


    def testSearch_sharp_720s(self):
        print ("####hmi.sharp_720s #############################")
        sdo_data_list = media_search(
        	server = sitools2_url,
        	dates = [d1,d2],
        	series = 'hmi.sharp_720s',
        	cadence = ['12 min'] )
        print(sdo_data_list[0:3])
        self.assertEqual( len(sdo_data_list), 720)


    def testSearch_m_720s(self):
        print ("####hmi.m_720s #########################################")
        sdo_data_list = media_search(
        	server = sitools2_url,
        	dates = [d1,d2],
        	series = 'hmi.m_720s',
        	cadence = ['12 min'] )
        print(sdo_data_list[0:3])
        self.assertEqual( len(sdo_data_list), 94)

    def testSearch_sharp_cea_720s(self):
        print ("####hmi.sharp_cea_720s #############################")
        sdo_data_list = media_search(
        	server = sitools2_url,
        	dates = [d1,d2],
        	series = 'hmi.sharp_cea_720s',
        	cadence = ['12 min'] )
        print(sdo_data_list[0:3])
        self.assertEqual( len(sdo_data_list), 119)

    def testSearch_m_720s_nrt(self):
        print ("####hmi.m_720s_nrt #########################")
        sdo_data_list = media_search(
        	server = sitools2_url,
        	dates = [d1,d2],
        	series = 'hmi.m_720s_nrt',
        	cadence = ['12 min'] )
        print(sdo_data_list[0:3])
        self.assertEqual( len(sdo_data_list), 120)

if __name__ == "__main__":
    unittest.main()
