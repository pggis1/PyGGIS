#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from liblas import *
from math import *

#f_Las = file.File('/home/cyx/ggis/LibLas_Python/Autzen_Stadium/lidar.las', mode = 'r')
#f_Las = file.File('/home/cyx/ggis/LibLas_Python/Autzen_Stadium/lidar.las', mode = 'r')
#f_Las = file.File('/home/cyx/ggis/LibLas_Python/Autzen_Stadium/lidar.las', mode = 'r')
#f_Las = file.File('/home/cyx/ggis/LibLas_Python/las/las12_format1.las', mode = 'r')
#f_Las = file.File('/home/cyx/ggis/LibLas_Python/Las/las12_format0.las', mode = 'r')
#f_Las = file.File('/home/cyx/ggis/LibLas_Python/Las/las12_format1.las', mode = 'r')
#f_Las = file.File('/home/cyx/ggis/LibLas_Python/Las/las12_format2.las', mode = 'r')
f_Las = file.File('/home/cyx/ggis/LibLas_Python/Las/test2f.las', mode = 'r')
print 'Header'

h = f_Las.header

print 'h.major_version, h.minor_version = ', h.major_version, h.minor_version
print 'h.dataformat_id = ',h.dataformat_id
print 'h.min = ', h.min
print 'h.max = ', h.max
print 'h.scale = ', h.scale
print 'h.offset = ', h.offset
print 'h.point_records_count = ', h.point_records_count
print 'h.project_id = ', h.project_id
print 'h.guid = ', h.guid
s = h.srs
print 's.proj4 = ', s.proj4

print ''
print 'Points'

print 'Count = ',len(f_Las)
minX = maxX = None
minY = maxY = None
minY = maxY = None
minZ = maxZ = None
for p in f_Las:
    if minX:
        if minX > p.x:
            minX = p.x
        if maxX < p.x:
            maxX = p.x
        if minY > p.y:
            minY = p.y
        if maxY < p.y:
            maxY = p.y
        if minZ > p.z:
            minZ = p.z
        if maxZ < p.z:
            maxZ = p.z
        dlt = sqrt((p0x - p.x)*(p0x - p.x) + (p0y - p.y)*(p0y - p.y))
        p0x = p.x; p0y = p.y
        #print dlt,     
    else:
        minX = p.x; maxX = p.x;
        minY = p.y; maxY = p.y
        minZ = p.z; maxZ = p.z
        p0x = p.x; p0y = p.y
            
         
print u'ЛНУ=', ('%10.2f'%minX, '%10.2f'%minY), u'\n'
print u'ПВУ=', ('%10.2f'%maxX, '%10.2f'%maxY)
print u'minZ=', '%6.2f'%minZ, u'   maxZ=', '%6.2f'%maxZ

f_Las.close()






