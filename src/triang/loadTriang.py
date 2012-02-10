#!/usr/bin/env python
# -*- coding: utf-8 -*-
##Copyright 2011 Владимир Суханов 
######################################################
#                      Main for load Triang
######################################################

from triang import *
global mCol, Pnts, startTime
from time import *
from math import *
import pickle


name_las = '/home/cyx/ggis/LibLas_Python/Autzen_Stadium/lidar'
#name_las = '/home/cyx/ggis/LibLas_Python/Las/las12_format0'
#name_las = '/home/cyx/ggis/LibLas_Python/Las/las12_format1'
#name_las = '/home/cyx/ggis/LibLas_Python/Las/las12_format2'

startTime = time()
dg_file = open(name_las+".dg", mode = 'r')
#pick = pickle.Pickler(dg_file)
len_mCol = pickle.load(dg_file)     # Число ребер графа

print "Создается таблица heshPoint и mCol"
hashPoint = []
for i in range(len_mCol):       # Заполнение пустыми ссылками
    hashPoint.append(-1)
    
i_Pnt = 0
lstPnt = []     # список точек
mCol = []       # список ребер
for i_Edge in range(len_mCol):
    edge_l = pickle.load(dg_file)           # Чтение ребра
    pnt = edge_l[0]                         # распаковка точки [x,y,z.inf]
    if pnt<>None:
        cPnt = CPoint(pnt[0], pnt[1], pnt[2])   # Создали объект точки
        cPnt.isInf = pnt[3]                     # признак бесконечной
        hash_Pnt =  int(round(fmod(hash("" + str(int(pnt[0])) + str(int(pnt[1]))), len_mCol)))    # хеш по координатам x,y
        need_add = True
        while (hashPoint[hash_Pnt] <> -1):      # пока не пустая ссылка (уже есть точка по этому адресу)
            hPnt = lstPnt[hashPoint[hash_Pnt]]  # что есть в таблице
            if (PeqP(cPnt, hPnt)):              # если наша
                need_add = False
                break
            else:
                hash_Pnt = int(round(fmod(hash_Pnt+1, len_mCol)))   # не наша точка, ищем дальше
        if need_add:        
            lstPnt.append(cPnt)                 # добавили в список точек в позицию i_Pnt
            hashPoint[hash_Pnt] = i_Pnt
            hPnt = cPnt
            i_Pnt = i_Pnt + 1
    else: hPnt = None
    # lstPnt[hashPoint[hash_Pnt]] - CPoint
    edge = Edge()                   # создали объект для ребра
    edge.SetOrg(hPnt)               # CPoint
    edge.SetOnext(edge_l[1])        # Номер в mCol
    edge.SetRot(edge_l[2])          # Номер в mCol
    mCol.append(edge)               # Добавили в список ребер

# замена номеров на значения
for col in mCol:
    i_onext = col.GetOnext()
    i_rot = col.GetRot()
    col.SetOnext(mCol[i_onext])
    col.SetRot(mCol[i_rot])    
    
print "Таблица mCol создана за ", time() - startTime 
print "len(lstPnt) = ", i_Pnt, len(lstPnt), " len(mCol) = ", len(mCol)
print "Время создания триангуляции из файла = ", time() - startTime 

startTime = time()
