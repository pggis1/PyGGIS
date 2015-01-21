#!/usr/bin/env python
# -*- coding: utf-8 -*-
##Copyright 2010, 2011 Владимир Суханов 
######################################################
#                      Main for Triang
######################################################

from liblas import *
from triang import *
global mCol, Pnts, startTime
from time import *
from math import *
#import wx

lasdir = "."

def Delone(LstPnt):     ## [[x,y,x], . . . . ]
    global startTime
    Pnts = []    
    p00 = LstPnt[0]
    minx = p00[0]; maxx = minx
    miny = p00[1]; maxy = miny
    Np = 0; Z0 = 0
    print "Чтение Las (сек) = ", time() - startTime
    startTime = time()
    for p00 in LstPnt:
        if (p00[0] < minx):  minx = p00[0]
        if (p00[0] > maxx):  maxx = p00[0]
        if (p00[1] < miny):  miny = p00[1]
        if (p00[1] > maxy):  maxy = p00[1]
        Np = Np + 1;
        Z0 = Z0 + p00[2]
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

# main

name_las = '/home/cyx/ggis/LibLas_Python/Autzen_Stadium/lidar'
#name_las = '/home/cyx/ggis/LibLas_Python/Las/las12_format0'
#name_las = '/home/cyx/ggis/LibLas_Python/Las/las12_format1'
#name_las = '/home/cyx/ggis/LibLas_Python/Las/las12_format2'
fLas = file.File(name_las+'.las', mode = 'r')


print "Las file = ", fLas.filename
h = fLas.header
print "h.major_version, h.minor_version = ", [h.major_version, h.minor_version]
print "h.dataformat_id = ", [h.dataformat_id]        
print "h.min = ", [h.min]
print "h.max = ", [h.max]
print "h.scale = ", [h.scale]
print "h.offset = ", [h.offset]
#print "h.project_id = ", [h.project_id]
#print "h.guid = ", [h.guid]
print "h.point_records_count", h.point_records_count
print " =============== "
if (h.point_records_count == 0):
    fLas.close()
    exit()
i = 0
x0 = n0 = 728500; n1 = 728550
y0 = 4676349
dlt = 0.1
dxMin = dxMax = dyMin = dyMax = pred = None
print "Start Las"
startTime = time()
lstPnt = []
for p in fLas:
    lstPnt.append([p.x - h.min[0], p.y - h.min[1], p.z])

dg = Delone(lstPnt)
print "Сохраняем триангуляцию "

import pickle
dg_file = open(name_las+".dg", mode = 'w')
pick = pickle.Pickler(dg_file)
#pick.dump(dg)
#pick.dump(mCol)
#dg_file.close()
len_mCol = len(mCol)
l_hash = 2*len_mCol
print "len_mCol = ", len_mCol, "l_hash = ", l_hash
pick.dump(len_mCol)

print "Создается таблица heshCol"
hashCol = []
for i in range(l_hash):
    hashCol.append(-1)
startTime = time()
i_my = 0
for col in mCol:
    hash_my = int(round(fmod(id(col), l_hash)))
    #hash_my = fmod(abs(hash(col)), l_hash)
    while (hashCol[hash_my] <> -1): 
        hash_my = int(round(fmod(hash_my+1, l_hash)))
    hashCol[hash_my] = i_my
    i_my = i_my + 1
print "Таблица heshCol создана за ", time() - startTime 

startTime = time()
i_my = 0
for col in mCol:
    pt = col.GetOrg()
    if pt is not None:
        org = [pt.x, pt.y, pt.z, pt.isInf]
    else: org = None
    #get adresses
    O_next = col.GetOnext()
    h_Onext = int(round(fmod(id(O_next), l_hash)))
    while (mCol[hashCol[h_Onext]] <> O_next): 
        h_Onext = int(round(fmod(h_Onext+1, l_hash)))
        if (hashCol[h_Onext] == -1):
            print "Hash ERROR Onext"
            exit()
    i_Onext = hashCol[h_Onext]  # adress in mCol
    
    rot = col.GetRot()
    h_rot = int(round(fmod(id(rot), l_hash)))
    while (mCol[hashCol[h_rot]] <> rot): 
        h_rot = int(round(fmod(h_rot+1, l_hash)))
        if (hashCol[h_rot] == -1):
            print "Hash ERROR Rot"
            exit()
    i_Rot = hashCol[h_rot]      # adress in mCol
    
    edge_Col = [org, i_Onext, i_Rot]
    pick.dump(edge_Col)
    i_my = i_my + 1
    if (fmod(i_my,1000) < 1):
        print i_my, time() - startTime 
        
dg_file.close()    
print "Триангуляция сохранена в файле : " + name_las+".dg за ", time() - startTime 


