import datetime as dt
import sitools2.clients.sdo_client_medoc as md
server = 'http://medoc-sdo.ias.u-psud.fr'
ls = md.media_search(
    server=server, series='aia.lev1', waves=['193'], cadence=['10m'],
    dates=[dt.datetime(2018, 1, 1, 0, 0, 0), dt.datetime(2018, 1, 1, 1, 0, 0)])
kw = md.media_metadata_search(media_data_list=ls, keywords=['recnum', 'cdelt1', 'cdelt2'], server=server)
assert(len(ls) == len(kw))
print(kw[0])

import datetime as dt
import sitools2.clients.sdo_client_medoc as md
server = 'http://idoc-medoc.ias.u-psud.fr'
ls = md.media_search(
    server=server, series='hmi.m_720s', cadence=['12m'],
    dates=[dt.datetime(2018, 1, 1, 0, 0, 0), dt.datetime(2018, 1, 1, 1, 0, 0)])
kw = md.media_metadata_search(media_data_list=ls, keywords=['recnum', 'cdelt1', 'cdelt2'], server=server)
assert(len(ls) == len(kw))
print(kw[0])
