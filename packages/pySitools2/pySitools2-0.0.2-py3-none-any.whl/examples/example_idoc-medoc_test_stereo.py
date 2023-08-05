#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test stereo data
Idoc medoc interface
"""

from sitools2.core.pySitools2 import *
from sitools2.clients import constants
from future.moves.urllib.request import urlretrieve

sitools_url = constants.SITOOLS2_URL


def main():
    print("Loading SitoolsClient for", sitools_url)
    sitools_instance = Sitools2Instance(sitools_url)
    print("sitools_instance : %s " % sitools_instance.list_project())

    ds1 = Dataset(sitools_url + "/webs_STEREO_dataset")
    ds1.display()

    # date__ob
    # Format must be something like 2015-11-01T00:00:00.000 in version Sitools2 3.0 that will change
    param_query1 = [
        [ds1.fields_dict['date_obs']],
        ['2010-06-01T00:00:00.000', '2010-06-02T00:00:00.000'],
        'DATE_BETWEEN']

    q1 = Query(param_query1)
    # Q2 = Query(param_query2)
    # Q3 = Query(param_query3)

    # Ask recnum, sunum,series_name,date__obs, ias_location,ias_path

    o1 = [
        ds1.fields_dict['filename'], ds1.fields_dict['filesize'],
        ds1.fields_dict['instrument'], ds1.fields_dict['date_obs'],
        ds1.fields_dict['secchisata'], ds1.fields_dict['secchisatb'],
        ds1.fields_dict['wavemin'], ds1.fields_dict['wavemax'],
        ds1.fields_dict['datatype'], ds1.fields_dict['download_path'],
        ds1.fields_dict['path'], ds1.fields_dict['id_sitools_view']
    ]

    # Sort date__obs ASC
    s1 = [[ds1.fields_dict['date_obs'], 'ASC']]

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

    print("Download just one STEREO data\nIn progress please wait ...")
    print("item : \n%s" % result[1])
    print("id : %s" % result[1]['id_sitools_view'])
    try:
        ds1.execute_plugin(
            plugin_name='pluginSTEREOtar',
            pkey_values_list=[result[1]['id_sitools_view']],
            filename='first_download_STEREO.tar'
        )
    except ValueError as e:
        print("Issue downloading id_sitools_view : %s " % result[1]['id_sitools_view'])
        print("args is: %s" % e.args)
        print("repr : %s" % e.__repr__())
    except Exception as e:
        print("Issue downloading id_sitools_view : %s " % result[1]['id_sitools_view'])
        print("Message : %s" % e.__repr__())

    else:
        print("Download id_sitools_view : %s ,file %s completed" % (result[1]['id_sitools_view'],
                                                                    'first_download_STEREO.tar'))

    print("Try to download with urlretrieve")
    print("item : \n%s" % result[2])
    filename_item = (result[2]['filename'].split("/"))[-1]
    try:
        urlretrieve(result[2]['download_path'], filename_item)
    except Exception as e:
        print("Issue downloading id_sitools_view : %s " % result[2]['id_sitools_view'])
        print("type is: %s" % e.args)
        print("Message : %s" % e.__repr__())
    else:
        print("Download id_sitools_view : %s , file %s completed" % (result[2]['id_sitools_view'], filename_item))


if __name__ == "__main__":
    main()
