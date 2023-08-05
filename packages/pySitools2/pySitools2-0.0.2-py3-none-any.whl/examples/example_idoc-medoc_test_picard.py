#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test picard dataset
Idoc medoc web interface
"""

from sitools2.core.pySitools2 import *
from sitools2.clients import constants

sitools_url = constants.SITOOLS2_URL


def main():
    print("Loading SitoolsClient for", sitools_url)
    sitools2 = Sitools2Instance(sitools_url)
    print("sitoolsinstance : %s " % sitools2.list_project())

    ds1 = Dataset(sitools_url + "/webs_PICARD_dataset")
    ds1.display()

    # date__obs
    # Format must be something like 2015-11-01T00:00:00.000 in version Sitools2 3.0 that will change

    param_query1 = [[ds1.fields_dict['datetimeobs']],
                    ['2010-10-01T00:00:00.000', '2010-10-02T00:00:00.000'],
                    'DATE_BETWEEN'
                    ]

    q1 = Query(param_query1)
    # Q2 = Query(param_query2)
    # Q3 = Query(param_query3)

    # Ask recnum, sunum,series_name,date__obs, ias_location,ias_path

    o1 = [
        ds1.fields_dict['filename'], ds1.fields_dict['dir_fits'],
        ds1.fields_dict['instrume'], ds1.fields_dict['datetimeobs'],
        ds1.fields_dict['obs_mode'], ds1.fields_dict['obs_type'],
        ds1.fields_dict['lambda'], ds1.fields_dict['exposure'],
        ds1.fields_dict['id'], ds1.fields_dict['dir_preview'],
        ds1.fields_dict['lambda'], ds1.fields_dict['level_pro']
    ]

    # Sort date__obs ASC
    s1 = [[ds1.fields_dict['datetimeobs'], 'ASC']]

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

    print("Download just one PICARD data\nIn progress please wait ...")
    print("item : \n%s" % result[1])

    dataset_pk = ds1.primary_key.name
    print("id : %s" % result[1][dataset_pk])
    try:
        ds1.execute_plugin(plugin_name='pluginPICARDtar', pkey_values_list=[result[1][dataset_pk]],
                           filename='first_download_PICARD.tar')
    except ValueError as e:
        print("Issue downloading pk : %s " % result[1][dataset_pk])
        print("type is: %s" % e.args)
        print("Message : %s" % e.__repr__())
    except Exception as e:
        print("Issue downloading id_sitools_view : %s " % result[1][dataset_pk])
        print("Message : %s" % e.__repr__())

    else:
        print("Download id_sitools_view : %s completed" % result[1][dataset_pk])

    print("Try to download with dir_fits dir")
    print("item : \n%s" % result[2])
    filename_item = (result[2]['filename'].split("/"))[-1]
    try:
        urlretrieve(result[2]['dir_fits'], filename_item)
    except IOError as e:
        print("Issue downloading pk : %s " % result[2][dataset_pk])
        print("type is: %s" % e.__class__.__name__)
        print("Message : %s" % e.strerror)
    except Exception as e:
        print("Issue downloading pk : %s " % result[2][dataset_pk])
        print("type is: %s" % e.__class__.__name__)
        print("Message : %s" % e.__repr__())
    else:
        print("Download id_sitools_view : %s , file %s completed" % (result[2][dataset_pk], filename_item))


if __name__ == "__main__":
    main()
