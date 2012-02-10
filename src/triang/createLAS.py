#!/usr/bin/env python
# -*- coding: utf-8 -*-
##Copyright 2011 Владимир Суханов 
######################################################
#            Построение файла Las
######################################################

#from triang import *
global hors, startTime
from time import *
from math import *
#import pickle
from liblas import file, point, header 

from inpLAS import *        # Задание на построение модели уарьера

#name_las = '/home/cyx/ggis/LibLas_Python/Las/test2f'
#name_las = '/home/cyx/ggis/LibLas_Python/Las/las12_format0'
#name_las = '/home/cyx/ggis/LibLas_Python/Las/las12_format1'
#name_las = '/home/cyx/ggis/LibLas_Python/Las/las12_format2'

#n = 5       # число горизонтов
#X00 = 5000  # центр
#Y00 = 5000  #
#Z00 = - 100  # начальная отметка

#Hust = 15   # высота уступа
#Ugl = 60*3.14/180.0    # угол наклона откоса
#DLT_l = 5   # приращение по длине сегмента
#D2_D1 = 0.5 # эксцентриситет
#R = 50      # ширина площадки
#R10 = 150   # начальный радиус

print "Построение модели карьера с записью в файл ", name_las
startTime = time()
hors = [[[X00,Y00,Z00],0]]   # [[центр карьера], радиус верхней бровки]
print "Планирование горизонтов"       
for i in range(0, n):       # По уступам горизонтов
    rDn = R10 + i * R       # Радиус нижней бровки
    zDn = Z00 + (i * Hust)  # Отметка нижней бровки
    hors.append([[X00,Y00,zDn], rDn])    # Нижняя бровка
    rUp = rDn + Hust/tan(Ugl) # Радиус верхней бровки
    zUp = zDn + Hust        # Отметка верхней бровки
    hors.append([[X00,Y00,zUp], rUp])    # Верхняя бровка
#print hors

def getZp(x,y):
    br1 = hors[0]
    
    for br2 in hors[1:]:
        xc1,yc1,zc1 = br1[0]
        r1 = br1[1]
        xc2,yc2,zc2 = br2[0]
        r2 = br2[1]
        rxy = sqrt(pow((x - xc1), 2) + pow(((y-yc1)/D2_D1), 2))
        if (rxy>=r1) and (rxy<r2):
            zxy = zc1 + ((zc2 - zc1) * (rxy - r1) / (r2 - r1))
            return zxy
        br1 = br2
    return zc2      # отметка верхней площадки

xMin = X00 - (n+2) * (R + Hust)
xMax = X00 + (n+2) * (R + Hust)
yMin = Y00 - (n+2) * (R + Hust)*D2_D1
yMax = Y00 + (n+2) * (R + Hust)*D2_D1
zMin = Z00
zMax = Z00 + n * Hust
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
# f = file.File('junk.las', mode="w", header=h) 
x = xMin; cnt = 0
while x <= xMax:
    y = yMin;
    while y <= yMax:
        z = getZp(x,y)
        pt = point.Point()  
        pt.x = x; pt.y = y; pt.z = z
        las_file.write(pt)   # write point to las
        cnt = cnt + 1
        y = y + dy
    #print cnt
    x = x + dx

las_file.close()

print "Создали файл LAS за ", time() - startTime, "сек. Число точек = ", cnt

