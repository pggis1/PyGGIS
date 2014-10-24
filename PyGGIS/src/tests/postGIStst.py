#!/usr/bin/env python
# -*- coding: utf-8 -*-
##Copyright 2009 Владимир Суханов 
##
##cyx-fat@e1.ru
##
##Тесты для горной ГИС

import psycopg2
from regim import * 
#import shapely
#import shapely.wkt
#import shapely.wkb
def parsGeometry(geom):
    coords = geom[geom.find('(')+1:geom.find(')')]
    #print(coords)
    lstCoords = coords.split(',')
    #print(lstCoords)
    lstXYZ=[]
    for pnt in lstCoords:
        pntXYZ=[]
        xyz=pnt.split(' ')
        for val in xyz:
            if val.isdigit():
                pntXYZ = pntXYZ + [float(val)]
        #print(pntXYZ)
        lstXYZ = lstXYZ + [pntXYZ]
    #print(lstXYZ)
    return lstXYZ
# Автономный тест
geom = 'LINESTRING(350 250  ,550 250,550 450 260,350 450 260,350 250 260)'
print parsGeometry(geom)

# Тестирование запроса из БД 
conn = psycopg2.connect("dbname="+POSTGR_DBN+" user="+POSTGR_USR)
curs=conn.cursor()
#curs.execute("select * from org_tech")
#rows = curs.fetchall()
#rows
#for rec in rows:
#	print(str(rec[0])); print(str(rec[1])); print(str(rec[2]))
#curs.execute("select geom from topograph")
#curs.execute("select ST_AsText(geom) from topograph")
curs.execute("select ST_AsEWKT(geom) from topograph")
#curs.execute("select ST_AsEWKB(geom) from topograph")
rows = curs.fetchall()
rows
for rec in rows:
    print(type(rec[0]))
    print(rec[0])
    line1 = parsGeometry(str(rec[0]))
    print(line1)


"""    
curs.execute("select ST_AsEWKB(geom) from topograph")
rows = curs.fetchall()
rows
for rec in rows:
    print(type(rec[0]), rec[0])
    #line1 = shapely.wkb.loads(str(rec[0]))
    line1 = parsGeometry(str(rec[0]))
    print(line1)
    print('---------------------------------------------')    


print('======================================')    
from ctypes import c_char_p
from shapely.geos import lgeos, allocated_c_char_p, ReadingError
from shapely.geometry.base import BaseGeometry,geometry_type_name

def geom_factory(g, parent=None):
    # Abstract geometry factory for use with topological methods below
    if not g:
        raise ValueError("No Shapely geometry can be created from null value")
    ob = BaseGeometry()
    geom_type = geometry_type_name(g)
    # TODO: check cost of dynamic import by profiling
    mod = __import__(
        'shapely.geometry', 
        globals(), 
        locals(), 
        [geom_type],
        )
    print(geom_type)
    print(mod)
    ob.__class__ = getattr(mod, geom_type)
    ob.__geom__ = g
    ob.__p__ = parent
    ob._ndim = 3 # callers should be all from 2D worlds
    return ob


# Pickle-like convenience functions

def loads(data):
    #from shapely.geometry.base import geom_factory
    geom = lgeos.GEOSGeomFromWKT(c_char_p(data))
    if not geom:
        raise ReadingError, \
        "Could not create geometry because of errors while reading input."
    return geom_factory(geom)
    #return geom

curs.execute("select ST_AsEWKT(geom) from topograph")
#curs.execute("select ST_AsEWKB(geom) from topograph")
rows = curs.fetchall()
rows
for rec in rows:
    print(type(rec[0]), rec[0])
    print(c_char_p(rec[0]))
    line1 = loads(rec[0])
    print(line1.__class__, line1.__geom__, line1._ndim)
    print(line1.to_wkt())
    print('---------------------------------------------')
"""        
