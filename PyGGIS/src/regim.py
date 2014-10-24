#!/usr/bin/env python
# -*- coding: utf-8 -*-
##Copyright 2009, 2010 Владимир Суханов 
##
##cyx-fat@e1.ru
##
""" Настройки и константы ГГИС """

MW_SIZE     = (1024, 768)        # Размеры главного окна
CANVAS_SIZE = (300, 100)         # Размеры канвы
HELP_SIZE   = (500, 500)         # Размеры окна помощи
MNU_OPEN    = ("&Открыть", "Открыть STEP файл")
MNU_SAVEAS  = ("Сохранить как &картинку\tAlt-I", "Сохраняет текущий экран как картинку.")
MNU_SCRIPT  = ("Выполнить скрипт", "Выполнить сторонний скрипт в этой сессии.")
MNU_EXIT    = ("&Выйти", "Exit application")
MNU_FILE    = "&Файл"
MNU_TOP     = ("Сверху\tAlt-1", "Вид сверху")
MNU_BOTTOM  = ("Снизу\tAlt-2", "Виду снизу")
MNU_LEFT    = ("Слева\tAlt-3", "Вид слева")
MNU_RIGHT   = ("Справа\tAlt-4", "Вид справа")
MNU_FRONT   = ("Спереди\tAlt-5", "Вид спереди")
MNU_REAR    = ("Сзади\tAlt-6", "Вид сзади")
MNU_ISO     = ("Изометрическая проекция\tAlt-7", "Изометрическая проекция")
MNU_ZOOMALL = ("Приблизить &всё\tAlt-A", "Приблизить всё")
MNU_ZOOMWIN = ("Приблизить &область\tAlt-W", "Приблизить область")
MNU_VIEW    = "&Вид"
MNU_VERTEX  = (u'Vertex', 'Select vertices.')
MNU_EDGE    = (u'Edge', 'Select edges.')
MNU_FACE    = (u'Face', 'Select faces.')
MNU_NEUTRAL = (u'Neutral', 'Switch back to global shapes selction.')
MNU_SELECTION = "&Selection"
MNU_WARE    = (u'Wireframe', 'Switch to wireframe mode.')
MNU_SHADED  = (u'Shaded', 'Switch to shaded mode.')
MNU_QHLR    = (u'Quick HLR', 'Switch to Quick Hidden Line Removal mode.')
MNU_EXHLR   = (u'Exact HLR', 'Switch to Exact Hidden Line Removal mode.')
MNU_AALIASon = (u'Включить антиалайзинг', 'Включить антиалайзинг.')
MNU_AALIASof = (u'Выключить антиалайзинг', 'Выключить антиалайзинг.')
MNU_DISMODE = u"&Отображение"
MNU_CRAXIS  = (u'Оси', 'Create axis')
MNU_CRLINE2 = (u'Отрезок', 'Create line 2D.')
MNU_CRPIT   = (u'Демо карьер', 'Demo Pit')
MNU_EXPLORE = (u'Просмотр', 'Просмотр геометрии')
MNU_ERASE = (u'Удалить', 'Удалить элемент')
MNU_CREATE      = "Рисование"
MNU_ABOUT       = ("&О программе", "")
MNU_HELP        = "&Помощь"
MNU_CRDEMODB    =(u'СоздатьБД', 'Демо карьер в БД')
MNU_CLOAD       =(u'Загрузить БД', 'Загрузить БД')
MNU_LIDAR       = (u'Загрузить LIDAR', u'Загрузить LIDAR')
MNU_CSAVE       = (u'Сохранить в БД', u'Сохранить в БД')
MNU_EDIT        = "Редактирование"
MNU_EdBrMoveV   =(u'Переместить', 'Перенести вершину объекта')
MNU_EdBrInsV    =(u'Вставить точку', 'Вставить точку в объект')
MNU_EdBrDelV    =(u'Удалить точку', 'Удалить точку на объекте')
MNU_EdBrBrkV    =(u'Разорвать объект', 'Разорвать объект в точке')
MNU_EdBrDelB    =(u'Удалить объект', 'Удалить объект')
CMD_EdBrMoveV   = 101
CMD_EdBrInsV    = 102
CMD_EdBrDelV    = 103
CMD_EdBrBrkV    = 104
CMD_EdBrInsV    = 105
CMD_EdBrBrkV    = 106
CMD_EdBrDelB    = 107
CMD_EdBrSelB    = 108
CMD_EdBrCutE    = 109
CMD_EdBrMoveP   = 110
CMD_EdBrMerge   = 111
CMD_AddText     = 112

CurrentText     = "<координаты>"
#CMD_EdBr????    = 108
POSTGR_DBN     =   u'postgres'
POSTGR_USR     =   u'postgres'

type_labels=['бровка','тело','скважина','изолиния',]

menu_types=[
    ['edge','start_edge','edge_OnEdBrDelB','edge_OnEdBrBrkV','edge_OnEdBrInsV','edge_OnEdBrDelV','edge_OnEdBrMoveV','edge_OnEdBrMerge','make_cut_query','start_way_pline','cut_levels'],
    ['body','start_body','body_OnEdBrDelB'],
    ['drill','start_drill','drill_OnEdBrDelB','drill_OnEdBrMoveP'],
    ['isoline','start_isoline','isoline_OnEdBrDelB','isoline_OnEdBrInsV','isoline_OnEdBrDelV','isoline_OnEdBrMoveV']
]

menu_titles={
    'main': u'Главное меню',
    'add': u'Задание',
    'edge': u'Бровки',
    'start_edge': u'Создание Бровки',
    'edge_OnEdBrDelB': u'Удалить Бровку',
    'edge_OnEdBrBrkV': u'Разбить Бровку',
    'edge_OnEdBrInsV': u'Вставить Точку',
    'edge_OnEdBrDelV': u'Удалить Точку',
    'edge_OnEdBrMoveV': u'Перем. Точку',
    'edge_OnEdBrMerge': u'Обеденить Бров.',
    'body': u'Тела',
    'start_body': u'Создание тела',
    'body_OnEdBrDelB': u'Удалить Тело',
    'isoline': u'Рельеф',
    'start_isoline': u'Создание изолинии',
    'isoline_OnEdBrDelB': u'Удалить Изолинию',
    'isoline_OnEdBrInsV': u'Вставить Точку',
    'isoline_OnEdBrDelV': u'Удалить Точку',
    'isoline_OnEdBrMoveV': u'Перед. Точку',
    'drill': u'Скважины',
    'start_drill': u'Задать скважину',
    'drill_OnEdBrMoveP': u"Перемест.скважину",
    'drill_OnEdBrDelB': u'Удалить Скважину',
    'ways': u'Съезды',
    'start_way_pline': u'Задание съезда',
    'edit': u'Корректировка',
    'cut': u'Прирезка',
    'start_cut_pline': u'Задание Прирезки',
    'make_cut_query': u'ПодтвердПрирезку',
    'cut_OnEdBrSelB': u'Задание Начала',
    'cut_levels': u'Поур.Прирезка',
    'start_cut_levels_pline': u'Задание Прирезки',
}