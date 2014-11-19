#!/usr/bin/env python
# -*- coding: utf-8 -*-
##Copyright 2011 Владимир Суханов 
######################################################
#                      Исходные данные для построения модели Las 
######################################################

n = 5               # число горизонтов
X00 = 5000.0        # центр
Y00 = 5000.0        #
Z00 = - 100.0       # начальная отметка
Hust = 15           # высота уступа
Ugl = 60*3.14/180.0 # угол наклона откоса
DLT_l = 5.0         # приращение по длине сегмента
D2_D1 = 0.5         # эксцентриситет
R = 50.0            # ширина площадки
R10 = 150.0         # начальный радиус
# Имя файла без расширения
name_las = '/home/cyx/ggis/LibLas_Python/Las/test2f'
#name_las = '/home/cyx/ggis/LibLas_Python/Las/las12_format0'
#name_las = '/home/cyx/ggis/LibLas_Python/Las/las12_format1'
#name_las = '/home/cyx/ggis/LibLas_Python/Las/las12_format2'
