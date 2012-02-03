#!/usr/bin/env python
# -*- coding: utf-8 -*-
##Copyright 2009, 2010 Владимир Суханов 
##
##cyx-fat@e1.ru
##
""" Настройки и константы ГГИС """

MW_SIZE     = (1024,768)        # Размеры главного окна
CANVAS_SIZE = (300,100)         # Размеры канвы
HELP_SIZE   = (500,500)         # Размеры окна помощи
MNU_OPEN    = ("&Open", "Open a STEP file")
MNU_SAVEAS  = ("Save as &image\tAlt-I", "Saves the current view as an image.")
MNU_SCRIPT  = ("Execute Script", "Execute a Python script in the current session.")
MNU_EXIT    = ("&Exit", "Exit application")
MNU_FILE    = "&File"
MNU_TOP     = ("Top\tAlt-1", "Top View")
MNU_BOTTOM  = ("Bottom\tAlt-2", "Bottom View")
MNU_LEFT    = ("Left\tAlt-3", "Left View")
MNU_RIGHT   = ("Right\tAlt-4", "Right View")
MNU_FRONT   = ("Front\tAlt-5", "Front View")    
MNU_REAR    = ("Rear\tAlt-6", "Rear View")
MNU_ISO     = ("Iso\tAlt-7", "Iso View")
MNU_ZOOMALL = ("Zoom &All\tAlt-A", "Zoom All")
MNU_ZOOMWIN = ("Zoom &Win\tAlt-W", "Zoom Window")
MNU_VIEW    = "&View"
MNU_VERTEX  = (u'Vertex', 'Select vertices.')
MNU_EDGE    = (u'Edge', 'Select edges.')
MNU_FACE    = (u'Face', 'Select faces.')
MNU_NEUTRAL = (u'Neutral', 'Switch back to global shapes selction.')
MNU_SELECTION = "&Selection"
MNU_WARE    = (u'Wireframe', 'Switch to wireframe mode.')
MNU_SHADED  = (u'Shaded', 'Switch to shaded mode.')
MNU_QHLR    = (u'Quick HLR', 'Switch to Quick Hidden Line Removal mode.')
MNU_EXHLR   = (u'Exact HLR', 'Switch to Exact Hidden Line Removal mode.')
MNU_AALIASon = (u'AntiAliasing On', 'Enable antialiasing.')
MNU_AALIASof = (u'Antialiasing Off', 'Disable antialiasing.')
MNU_DISMODE = "&Display mode"
MNU_CRAXIS  = (u'Оси', 'Create axis')
MNU_CRLINE2 = (u'Отрезок', 'Create line 2D.')
MNU_CRPIT   = (u'Демо карьер', 'Demo Pit')
MNU_EXPLORE = (u'Просмотр', 'Просмотр геометрии')
MNU_ERASE = (u'Удалить', 'Удалить элемент')
MNU_CREATE      = "Рисование"
MNU_ABOUT       = ("&About", "")
MNU_HELP        = "&Help"
MNU_CRDEMODB    =(u'СоздатьБД', 'Демо карьер в БД')
MNU_CLOAD       =(u'Загрузить БД', 'Загрузить БД')
MNU_LIDAR       = (u'Загрузить LIDAR', u'Загрузить LIDAR')
MNU_CSAVE       = (u'Сохранить в БД', u'Сохранить в БД')
MNU_EDIT        = "Редактирование"
MNU_EdBrMoveV   =(u'Переместить', 'Перенести вершину бровки')
MNU_EdBrInsV    =(u'Вставить точку', 'Вставить точку в бровку')
MNU_EdBrDelV    =(u'Удалить точку', 'Удалить точку на бровке')
MNU_EdBrBrkV    =(u'Разорвать бровку', 'Разорвать бровку в точке')
MNU_EdBrDelB    =(u'Удалить бровку', 'Удалить бровку')
CMD_EdBrMoveV   = 101
CMD_EdBrInsV    = 102
CMD_EdBrDelV    = 103
CMD_EdBrBrkV    = 104
CMD_EdBrInsV    = 105
CMD_EdBrBrkV    = 106
CMD_EdBrDelB    = 107
#CMD_EdBr????    = 108
POSTGR_DBN     =   u'postgres'
POSTGR_USR     =   u'postgres'



