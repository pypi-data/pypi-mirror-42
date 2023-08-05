#! /usr/bin/python
"""

"""

from sitools2.core.pySitools2 import *

__author__="Pablo ALINGERY"
__date__ ="$6 mai 2016 12:17:18$"

import unittest
from sitools2.clients.sdo_client_medoc import *
from sitools2.clients import constants

sitools2_url = constants.SITOOLS2_URL
functional_test = constants.FUNCTIONAL_TEST


@unittest.skipUnless(functional_test,"Functional Test "+ sitools2_url +" interface ")
class TestIdocMedocDsNbr(unittest.TestCase):        
    
    def setUp(self):
        pass

    def testNbrDsIdocMedoc(self):
        print ("\n####Test "+ sitools2_url +" NbrDatasets #############################")
        sitools_url = sitools2_url

        SItools1 = Sitools2Instance(sitools_url)
        prj_list = SItools1.list_project()
        print("Nombre de projets : ", len(prj_list))

        p1 = prj_list[0]
        print(p1)
        ds_list = p1.dataset_list()
        print ("Nbr datasets : %s" % len(ds_list))
        self.assertEqual( len(ds_list), 75)
if __name__ == "__main__":
    unittest.main()
