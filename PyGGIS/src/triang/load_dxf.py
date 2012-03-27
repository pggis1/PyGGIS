#!/usr/bin/env python
# -*- coding: utf-8 -*-
##Copyright 2011 Владимир Суханов 
######################################################
#                      Main for load Triang
######################################################

from triang import *
global mCol, Pnts, startTime, panel
from time import *
from math import *
#import pickle
from liblas import file, point, header 
#from inpLAS import *        # Задание на построение модели уарьера

def Delone(LstPnt):     ## [[x,y,x], . . . . ]
    global startTime, panel
    Pnts = []    
    p00 = LstPnt[0]
    minx = p00[0]; maxx = minx
    miny = p00[1]; maxy = miny
    minz = p00[2]; maxz = minz
    Np = 0; Z0 = 0
    startTime = time()
    for p00 in LstPnt:
        if (p00[0] < minx):  minx = p00[0]
        if (p00[0] > maxx):  maxx = p00[0]
        if (p00[1] < miny):  miny = p00[1]
        if (p00[1] > maxy):  maxy = p00[1]
        if (p00[2] < minz):  minz = p00[2]
        if (p00[2] > maxz):  maxz = p00[2]
        Np = Np + 1;
        Z0 = Z0 + p00[2]
    
    panel = (minx,miny,minz, maxx,maxy,maxz, )
    minx = minx - 1000000#
    maxx = maxx + 1000000#
    miny = miny - 1000000#
    maxy = maxy + 1000000#
    Z0 = Z0 / Np      #  уровень дальних точек = среднему
    Dy = maxy - miny
    Dx = Dy * 0.577351
    dx1 = (maxx - minx) / 2 + Dx
    dy1 = dx1 * 1.73206
  
    P0 = CPoint(minx - Dx, maxy, Z0)              # зап
    P1 = CPoint(maxx + Dx, maxy, Z0)              # вост
    P2 = CPoint((maxx - minx) / 2, maxy - dy1, Z0)# юг
    P0.isInf = True
    P1.isInf = True
    P2.isInf = True
    Pnts.append(P2) # первые 3 точки - дальние
    Pnts.append(P0)
    Pnts.append(P1)
    P0 = None
    P1 = None
    P2 = None
    
    print "Pnts = "
#    for p in Pnts: 
#        print [p.x, p.y, p.z]
#    print "LstPnt = ", LstPnt
    print "Подготовка графа (сек) = ", time() - startTime
    startTime = time()
    nV = 0
    delonGraph = DelaunayGraph(Pnts)
    Pnts = []
    for p00 in LstPnt:       
        Dx = p00[0]; Dy = p00[1]; dz = p00[2]; 
        P = CPoint(Dx, Dy, dz)
        delonGraph.InsertPoint(P)
        nV = nV + 1
        if (fmod(nV,1000) < 1):
            print nV, time() - startTime
        
    print "Всего: ", nV, time() - startTime
    # Провести контроль пересечений и двойных смежных кромок
    # проверить правильность переброски кромки в одной паре трг
    # проблема 4-уг-ка бабочки: как провести диагональ, по телу или крыльям?
    # Call dg.filterBr
    # ========================================================
    return delonGraph
    # delone


name_dxf = '/home/cyx/ggis/LibLas_Python/Dxf/Cyx05.dxf.utf'
filter = ['BORTL','BORTH']
startTime = time()
dxf_file = open(name_dxf, 'rt')
lstPnt = []
newPnt = False
waitCoordx = False
waitCoordy = False
waitCoordz = False
cnt = 0
for line in dxf_file:
    cnt = cnt + 1
    if (newPnt and waitCoordx):   
        waitCoordx = False
        x = float(line)
        pnt.append(x)
        continue
    if (newPnt and waitCoordy):   
        waitCoordy = False
        y = float(line)
        pnt.append(y)
        continue
    if (newPnt and waitCoordz):   
        waitCoordz = False
        z = float(line)
        pnt.append(z)
        lstPnt.append(pnt)
        newPnt = False
        continue
    if (newPnt and (line.find(' 10')<>-1)):   
        waitCoordx = True
        continue
    if (newPnt and (line.find(' 20')<>-1)):   
        waitCoordy = True
        continue
    if (newPnt and (line.find(' 30')<>-1)):   
        waitCoordz = True
        continue
    if line.find('AcDb3dPolylineVertex')<>-1:
        #print cnt, line
        pnt = []
        newPnt = True
        continue

dxf_file.close()
print "lstPnt создан за ", time() - startTime 

#for pnt in lstPnt:
#    print pnt
#lstPnt =[[10.0,10.0,0.0],[10.0,20.0,0.0],[20.0,15.0,0.0],[20.0,5.0,-10.0],[15,16,10]   ]
dg = Delone(lstPnt)  
  
#printDiagram()

name_las = '/home/cyx/ggis/LibLas_Python/Las/CyxTst'

#print panel
startTime = time()
xMin = panel[0] - 5
yMin = panel[1] - 5
zMin = panel[2] - 5
xMax = panel[3] + 5
yMax = panel[4] + 5    
zMax = panel[5] + 5    

dx = 0.5
dy = 0.5
print "Создание заголовка"
# Запись файла
#from liblas import header 
h = header.Header()         # Формируем заголовок
### Support storing time values 
h.major_version   = 1
h.minor_version   = 2
h.dataformat_id =  2
h.min =  [xMin, yMin, zMin]
h.max =  [xMax, yMax, zMax]
h.scale =  [0.01, 0.01, 0.01]
h.offset =  [0.0, 0.0, 0.0]
#h.point_records_count =  int(((xMax-xMin)/dx) * ((yMax-yMin)/dy))

#h.project_id =  "00000000-0000-0000-0000-000000000000"
#h.guid =  "00000000-0000-0000-0000-000000000000"
#s.proj4 = ''
print "Запись в файл LAS"
las_file = file.File(name_las+".las", mode = 'w', header=h) # Открыли файл на запись с заголовком

x = xMin; cnt = 0
while x <= xMax:
    y = yMin;
    while y <= yMax:
        z = GetZ(x,y)
        #print [x,y,z]
        pt = point.Point()  
        pt.x = x; pt.y = y; pt.z = z
        las_file.write(pt)   # write point to las
        cnt = cnt + 1
        y = y + dy
    #print cnt
    x = x + dx

las_file.close()

print "Создали файл LAS за ", time() - startTime, "сек. Число точек = ", cnt

