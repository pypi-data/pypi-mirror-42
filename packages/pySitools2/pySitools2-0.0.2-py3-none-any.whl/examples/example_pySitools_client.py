#! /usr/bin/python
"""

@author: Pablo ALINGERY for IAS 28-08-2012
"""

from sitools2.core.pySitools2 import *


def main():

    #       sitools_url = 'http://sol-palinger:8182'
    #       sitools_url = 'http://sol-palinger-old:8182'
    #       sitools_url = 'http://sitools.akka.eu:8182'
    #       sitools_url = 'http://sitools.akka.eu:8184'
    #       sitools_url = 'http://medoc-sdo-test.ias.u-psud.fr'
    #        sitools_url = 'http://medoc-sdo.ias.u-psud.fr'
    #       sitools_url = 'http://medoc-dem.ias.u-psud.fr'
    #       sitools_url = 'http://idoc-herschel.ias.u-psud.fr'
    #       sitools_url = 'http://idoc-corotn2-public-v2.ias.u-psud.fr'
    sitools_url = 'http://idoc-medoc-test.ias.u-psud.fr'
    #       sitools_url = 'http://localhost:8184'

    print("Loading SitoolsClient for", sitools_url)
    sitools1 = Sitools2Instance(sitools_url)
    prj_list = sitools1.list_project()
    #       print "Nombre de projets : ",len(prj_list)
    ds_list = []
    for p in prj_list:
        p.display()
        for ds in p.dataset_list():
            ds_list.append(ds)

    if len(ds_list) != 0:
        print("%d dataset(s) found :" % len(ds_list))
        for i, dataset in enumerate(ds_list):
            print("%d) %s" % (i, dataset.name))
#        p1 = prj_list[0]
#        print p1
#       print "\nTarget project :\n\t",p1.name 
#        ds_lst = p1.dataset_list()
#       for ds in ds_lst :
#               print ds.name
    ds1 = ds_list[69]
    ds1.display()
    # display() or print works as well
    #       print ds1

    # date__ob
    # Format must be somthing like 2015-11-01T00:00:00.000 in version Sitools2 3.0

    param_query1 = [[ds1.fields_dict['date__obs']],
                    ['2015-11-01T00:00:00.000', '2015-11-01T01:00:00.000'],
                    'DATE_BETWEEN']
    #       param_query1 = [[ds1.fields_list[9]],['1123977851', '1123981271'],'NUMERIC_BETWEEN']
    # wave
    #       param_query2 = [[ds1.fields_list[5]],['94','131','171','193','211','304','335','1600','1700'],'IN']
    #       param_query2 = [[ds1.fields_list[5]],['335'],'IN']
    #       param_query2 = [[ds1.fields_list[5]],['304','335'],'NUMERIC_BETWEEN']
    #       param_query2 = [[ds1.fields_list[5]],['171'],'eq']
    # cadence
    #       param_query3 = [[ds1.fields_list[10]],['1 min'],'CADENCE']
    # exptime
    #        param_query4 = [[ds1.fields_list[8]],['2.900849'],'LTE']
    # series_name
    #       param_query2 = [[ds1.fields_list[3]],['hmi.m_720s'],'IN']
    param_query2 = [[ds1.fields_dict['series_name']], ['hmi.sharp_cea_720s_nrt'], 'IN']
    q1 = Query(param_query1)
    q2 = Query(param_query2)
    #        Q3 = Query(param_query3)
    #        Q4 = Query(param_query4)

    # Ask date__obs,get, wave, exptime,ias_location
    #       o1 = [ds1.fields_list[0],ds1.fields_list[4],ds1.fields_list[5],ds1.fields_list[7]]

    # Ask recnum, sunum,date__obs, ias_location
    o1 = [
        ds1.fields_dict['get'], ds1.fields_dict['get_segment'], ds1.fields_dict['recnum'],
        ds1.fields_dict['sunum'], ds1.fields_dict['date__obs']
    ]

    # Ask date__obs,get,recnum wave, exptime,ias_location
    #        o1 = [ds1.fields_list[1],ds1.fields_list[3],ds1.fields_list[4],ds1.fields_list[5],ds1.fields_list[7]]
    # Ask date__obs, exptime
    #       o1 = [ds1.fields_list[4], ds1.fields_list[8]]

    # Ask recnum
    #       o1 = [ds1.fields_list[1]]

    # Sort date__obs ASC, wave ASC, exptime DESC
    #       S1 = [[ds1.fields_list[5],'ASC'],[ds1.fields_list[4],'ASC'],[ds1.fields_list[8],'DESC']]
    # Sort date__obs ASC, exptime DESC
    #       S1 = [[ds1.fields_list[4],'ASC'],[ds1.fields_list[8],'DESC']]
    # Sort date__obs ASC, wave ASC
    #        S1 = [[ds1.fields_list[4],'ASC'],[ds1.fields_list[5],'ASC']]

    # Sort date__obs ASC
    S1 = [[ds1.fields_dict['date__obs'], 'ASC']]

    #       for field in ds1.fields_list :
    #               field.display()

    print("\nPrint Query  ...")
    q1.display()
    q2.display()
    #       Q3.display()
    #       Q4.display()

    #       print "toto :",ds1.fields_list[2].name
    #       result = ds1.search([q1,q2,Q3,Q4],o1,S1,nbr_to_display=10)
    #       result = ds1.search([q1,q2,Q3],o1,S1,limit_to_nb_res_max=10)
    result = ds1.search([q1, q2], o1, S1)
    #        result = ds1.search([q1,q2],o1,S1,limit_to_nb_res_max=10)
    if len(result) != 0:
        print("Results :")
        for i, data in enumerate(result):
            print("%d) %s" % (i + 1, data))

#       else :
#               sys.stdout.write("For the following queries :\n")
#               q1.display()
#              q2.display()
#               sys.stdout.write("No results found\n")
#        ds2=Dataset("http://sol-palinger-old:8182/webs_IAS_SDO_dataset")
#        ds2.display()
    recnum_list = []
    for record in result:
        recnum_list.append(str(record['recnum']))
    ds_hmi = Dataset(sitools_url + "/webs_hmi.sharp_cea_720s_nrt_dataset")

    # Old url for idoc-solar-portal-test for aia
    #        ds_aia=Dataset(sitools_url+"/webs_aia_dataset")
    ds_hmi.display()
    #        print recnum_list
    # recnum
    param_query_hmi = [[ds_hmi.fields_dict['recnum']], recnum_list, 'IN']
    Q_hmi = Query(param_query_hmi)
    Q_hmi.display()
    # quality

    O1_hmi = [
        ds_hmi.fields_dict['sunum'], ds_hmi.fields_dict['recnum'], ds_hmi.fields_dict['harpnum']
    ]
    print("output : ", ds_hmi.fields_list[114].name)
    S1_hmi = [[ds_hmi.fields_dict['harpnum'], 'ASC']]
    #       for field in ds_aia.fields_list :
    #               field.display()
    result_hmi = ds_hmi.search([Q_hmi], O1_hmi, S1_hmi)
    for data in result_hmi:
        print(data)

if __name__ == "__main__":
    main()
