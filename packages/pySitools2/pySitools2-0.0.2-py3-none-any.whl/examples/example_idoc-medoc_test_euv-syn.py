#! /usr/bin/python

"""
Test euv-syn data
Idoc medoc web interface
"""

__author__ = "Pablo ALINGERY"

from sitools2.core.pySitools2 import *
from sitools2.clients import constants

sitools_url = constants.SITOOLS2_URL


def main():
    print("Loading SitoolsClient for", sitools_url)
    sitools_server = Sitools2Instance(sitools_url)
    print("sitools_server : %s " % sitools_server.list_project())

    ds1 = Dataset(sitools_url + "/webs_EUV-SYN_dataset")
    ds1.display()

    # date__ob
    # Format must be something like 2015-11-01T00:00:00.000 in version Sitools2 3.0 that will change
    param_query1 = [
        [ds1.fields_dict['obs_date']],
        ['2004-03-01T00:00:00.000', '2010-03-02T00:00:00.000'],
        'DATE_BETWEEN'
    ]

    q1 = Query(param_query1)
    # Q2 = Query(param_query2)
    # Q3 = Query(param_query3)

    # Ask recnum, sunum,series_name,date__obs, ias_location,ias_path

    o1 = [
        ds1.fields_dict['filename'], ds1.fields_dict['download'],
        ds1.fields_dict['index'], ds1.fields_dict['filename'],
        ds1.fields_dict['crea_date'], ds1.fields_dict['obs_date'],
        ds1.fields_dict['wavelength']
    ]

    # Sort date__obs ASC
    s1 = [[ds1.fields_dict['obs_date'], 'ASC']]

    #       for field in ds1.fields_dict :
    #               field.display()

    #        print "\nPrint Query  ..."
    q1.display()
    # Q2.display()
    # Q3.display()

    # result = ds1.search([q1], o1, s1)
    #    print(len(result), " item(s) found\n")
    result = ds1.search([q1], o1, s1, limit_to_nb_res_max=10)
    print(len(result), " item(s) found\n")
    if len(result) != 0:
        print("Results :\n")
        for i, data in enumerate(result):
            print("%d) %s" % (i + 1, data))

    print("Download just one EUV-SYN data\nIn progress please wait ...")
    print("item : \n%s" % result[1])
    dataset_pk = ds1.primary_key.name
    try:
        ds1.execute_plugin(plugin_name='pluginEITSYNtar', pkey_values_list=[result[1][dataset_pk]],
                           filename='first_download_EITSYN.tar'
                           )
    except ValueError as e:
        print("Issue downloading id_sitools_view : %s " % result[1][dataset_pk])
        print("args is: %s" % e.args)
        print("repr : %s" % e.__repr__())
    except HTTPError as e:
        print("Issue downloading id_sitools_view : %s " % result[1][dataset_pk])
        print("code is: %s" % e.code)
        print("message : %s" % e.msg)
    else:
        print("Download id_sitools_view : %s,file %s completed" % (result[1][dataset_pk], 'first_download_EITSYN.tar'))
    print("Try to download with urlretrieve")
    print("item : \n%s" % result[2])
    filename_item = (result[2]['filename'].split("/"))[-1]
    try:
        urlretrieve(result[2]['download'], filename_item)
    except HTTPError as e:
        print("Issue downloading id_sitools_view : %s " % result[2][dataset_pk])
        print("error code is: %s" % e.code)
        print("message : %s" % e.msg)
    else:
        print("Download id_sitools_view : %s , file %s completed" % (result[2][dataset_pk], filename_item))


if __name__ == "__main__":
    main()
