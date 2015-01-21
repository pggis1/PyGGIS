# -*- coding: utf-8 -*-
import wx
import psycopg2
from regim import *


class LoadDialog(wx.Dialog):
    """Класс диалога задания объектов из базы данных"""

    def __init__(self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE):
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)
        self.this = pre.this
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "Введите параметры загрузки БД")
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        # Остальные окна
        dataBox = wx.BoxSizer(wx.HORIZONTAL)
        # Горизонты
        horBox = wx.BoxSizer(wx.VERTICAL)
        horBox.Add(wx.StaticText(self, -1, "Горизонты"), 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        connection = psycopg2.connect("dbname=" + POSTGR_DBN + " user=" + POSTGR_USR)
        db_cursor = connection.cursor()
        db_cursor.execute("select id_hor,point from horizons")
        horizons = db_cursor.fetchall()
        self.horizons_list = []
        self.horizons_ids = []
        for hor in horizons:
            self.horizons_ids = self.horizons_ids + [hor[0]]
            self.horizons_list = self.horizons_list + [str(hor[1])]
        self.chkHors = wx.CheckListBox(self, -1, (20, 20), (120, 200), self.horizons_list, wx.LB_MULTIPLE)

        for i in xrange(len(self.horizons_ids)):
            self.chkHors.Check(i, True)
        horBox.Add(self.chkHors, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        dataBox.Add(horBox, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        # Конец горизонтов
        # Геометрия
        geomBox = wx.BoxSizer(wx.VERTICAL)
        geomBox.Add(wx.StaticText(self, -1, "Объекты"), 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.geomList = ["Бровки", "Тела", "Скважины", "Изолинии"]
        self.chkGeoms = wx.CheckListBox(self, -1, (20, 20), (120, 150), self.geomList, wx.LB_MULTIPLE)
        geomBox.Add(self.chkGeoms, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        dataBox.Add(geomBox, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        # Конец геометрии
        # Изолинии
        db_cursor.execute("select min(heigth), max(heigth) from topograph")
        res = db_cursor.fetchone()
        self.minH = res[0]
        self.maxH = res[1]
        izoBox = wx.BoxSizer(wx.VERTICAL)
        izoBox.Add(wx.StaticText(self, -1, "Поверхность"), 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        izoBox.Add(wx.StaticText(self, -1, "Интервал высот"), 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.chkInterval = wx.TextCtrl(self, -1, str((self.minH, self.maxH)), size=(250, -1))
        izoBox.Add(self.chkInterval, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        dataBox.Add(izoBox, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        # Конец изолиний

        sizer.Add(dataBox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # Buttons
        cmdBox = wx.BoxSizer(wx.HORIZONTAL)
        btnOk = wx.Button(self, wx.ID_OK, "Принять")
        btnOk.SetDefault()
        btnOk.SetHelpText("Загрузить объекты из БД")
        self.Bind(wx.EVT_BUTTON, self.onBtnOk, id=btnOk.GetId())
        cmdBox.Add(btnOk, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        btnCancel = wx.Button(self, wx.ID_CANCEL, "Отменить")
        btnCancel.SetHelpText("Отменить и выйти")
        cmdBox.Add(btnCancel, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.onBtnCancel, id=btnCancel.GetId())
        sizer.Add(cmdBox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.resDict = dict()
        
    def onBtnOk(self, event):
        self.resDict = dict()
        # сформировать словарь
        lstHor = []
        for indHor in xrange(0, len(self.horizons_list)):
            if self.chkHors.IsChecked(indHor):
                lstHor = lstHor + [self.horizons_ids[indHor]]
        self.resDict['horIds'] = lstHor
        
        lstObj = []
        for indObj in xrange(0, len(self.geomList)):
            if self.chkGeoms.IsChecked(indObj):
                lstObj = lstObj + [indObj]        
        self.resDict['objList'] = lstObj
        
        try:
            self.resDict['izoLst'] = eval(self.chkInterval.GetValue())
        except SyntaxError:
            self.resDict['izoLst'] = (self.minH, self.maxH)
        self.EndModal(0)
        
    def onBtnCancel(self, event):
        self.resDict = dict()
        self.EndModal(0)
        
    def result(self):
        return self.resDict