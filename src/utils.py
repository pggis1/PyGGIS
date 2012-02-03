#!/usr/bin/env python
# -*- coding: utf-8 -*-
##Copyright 2009, 2010 Владимир Суханов 
"""
Утилиты и функции для ГГИС: 
LoadDlg, getPoints, parsGeometry, makeLINESTRING, distance2d
"""

import wx
import psycopg2
import OCC
#from OCC import STEPControl, StlAPI, IGESControl, TopoDS, BRep, BRepTools
#from OCC.AIS import AIS_Shape
#from OCC.BRepBuilderAPI import *
#from OCC.gp import *
from regim import *
#import OCC.KBE
#from OCC.KBE.TypesLookup import ShapeToTopology
from OCC.KBE.types_lut import ShapeToTopology
from utils import *
from math import *
from scipy import *
from scipy import linalg

def GetRowsTbl(tableName, where=""):
    conn = psycopg2.connect("dbname="+POSTGR_DBN+" user="+POSTGR_USR)
    curs = conn.cursor()
    query = "select * from " + tableName
    if where:
        query = query + " where " + where
    curs.execute(query)
    rows = curs.fetchall()
    return rows

class LoadDlg(wx.Dialog):
    """Класс диалога задания объектов из базы данных"""
    def __init__(self,parent,ID,title,
                 size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)
        self.this = pre.this        
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self,-1,"Введите параметры загрузки БД")
        sizer.Add(label,0,wx.ALIGN_CENTRE|wx.ALL,5)        
        # Остальные окна        
        dataBox = wx.BoxSizer(wx.HORIZONTAL)
        # Горизонты
        horBox = wx.BoxSizer(wx.VERTICAL)
        horBox.Add(wx.StaticText(self,-1,"Горизонты"),0,wx.ALIGN_CENTRE|wx.ALL,5)
        conn = psycopg2.connect("dbname="+POSTGR_DBN+" user="+POSTGR_USR)
        curs=conn.cursor()
        curs.execute("select id_hor,point from horizons")
        hors = curs.fetchall()
        self.horList = []
        self.horIds = []
        for hor in hors:
            self.horIds = self.horIds + [hor[0]]
            self.horList = self.horList + [str(hor[1])]
        self.chkHors = wx.CheckListBox(self, -1, (20, 20), (120, 200), self.horList, wx.LB_MULTIPLE)
        for i in range(len(self.horIds)):
            self.chkHors.Check(i, True)
        horBox.Add(self.chkHors,0,wx.ALIGN_CENTRE|wx.ALL,5)  
        dataBox.Add(horBox,0,wx.ALIGN_CENTRE|wx.ALL,5)
        # Конец горизонтов
        # Геометрия
        geomBox = wx.BoxSizer(wx.VERTICAL)
        geomBox.Add(wx.StaticText(self,-1,"Объекты"),0,wx.ALIGN_CENTRE|wx.ALL,5)
        self.geomList = ["Бровки", "Тела", "Скважины", "Изолинии"]
        self.chkGeoms = wx.CheckListBox(self, -1, (20, 20), (120, 150), self.geomList, wx.LB_MULTIPLE)
        geomBox.Add(self.chkGeoms,0,wx.ALIGN_CENTRE|wx.ALL,5)         
        dataBox.Add(geomBox,0,wx.ALIGN_CENTRE|wx.ALL,5)
        # Конец геометрии      
        # Изолинии
        curs.execute("select min(heigth), max(heigth) from topograph")
        res = curs.fetchone()
        self.minH = res[0]
        self.maxH = res[1]
        izoBox = wx.BoxSizer(wx.VERTICAL)
        izoBox.Add(wx.StaticText(self,-1,"Поверхность"),0,wx.ALIGN_CENTRE|wx.ALL,5)
        izoBox.Add(wx.StaticText(self,-1,"Интервал высот"),0,wx.ALIGN_CENTRE|wx.ALL,5)
        self.chkInterval = wx.TextCtrl(self, -1, str((self.minH,self.maxH)), size=(250, -1))
        izoBox.Add(self.chkInterval,0,wx.ALIGN_CENTRE|wx.ALL,5)         
        dataBox.Add(izoBox,0,wx.ALIGN_CENTRE|wx.ALL,5)
        # Конец изолиний     
        
        sizer.Add(dataBox,0,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
        # Buttons
        cmdBox = wx.BoxSizer(wx.HORIZONTAL)
        btnOk = wx.Button(self, wx.ID_OK, "Принять")
        btnOk.SetDefault()
        btnOk.SetHelpText("Загрузить объекты из БД")
        self.Bind(wx.EVT_BUTTON, self.onBtnOk, id=btnOk.GetId())
        cmdBox.Add(btnOk,0,wx.ALIGN_CENTRE|wx.ALL,5)
        
        btnCancel = wx.Button(self, wx.ID_CANCEL, "Отменить")
        btnCancel.SetHelpText("Отменить и выйти")
        cmdBox.Add(btnCancel,0,wx.ALIGN_CENTRE|wx.ALL,5)
        self.Bind(wx.EVT_BUTTON, self.onBtnCancel, id=btnCancel.GetId())
        sizer.Add(cmdBox,0,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.resDict = dict()
        
    def onBtnOk(self, event):
        self.resDict = dict()
        # сформировать словарь
        lstHor = []
        for indHor in range(0,len(self.horList)):
            if self.chkHors.IsChecked(indHor):
                lstHor = lstHor + [self.horIds[indHor]]
        self.resDict['horIds'] = lstHor
        
        lstObj = []
        for indObj in range(0,len(self.geomList)):
            if self.chkGeoms.IsChecked(indObj):
                lstObj = lstObj + [indObj]        
        self.resDict['objList'] = lstObj
        
        try:
            self.resDict['izoLst'] = eval(self.chkInterval.GetValue())
        except Exception:
            self.resDict['izoLst'] = (self.minH,self.maxH)
        self.EndModal(0)
        
    def onBtnCancel(self, event):
        self.resDict = dict()
        self.EndModal(0)
        
    def result(self):
        return self.resDict
# End of class LoadDlg

def parsGeometry(geom):
    """Разобрать координаты геометрического объекта"""
    coords = geom[geom.find('(')+1:geom.find(')')]
    lstCoords = coords.split(',')
    lstXYZ=[]
    for pnt in lstCoords:
        pntXYZ=[]
        xyz=pnt.split(' ')
        for val in xyz:
            if val.isdigit():
                pntXYZ = pntXYZ + [float(val)]
        lstXYZ = lstXYZ + [pntXYZ]
    return lstXYZ
        
def getPoints(shape):
    """Получить точки выбранного объекта"""
    result = []
    if shape:
        ex=OCC.TopExp.TopExp_Explorer()            
        ex.Init(shape,OCC.TopAbs.TopAbs_VERTEX)            
        te = ShapeToTopology()
        bt = OCC.BRep.BRep_Tool()
        result = []
        while True:
            sv=ex.Current()
            vv=te(sv)
            p1=OCC.BRep.BRep_Tool.Pnt(vv)
            p1 = [p1.X(),p1.Y(),p1.Z()]
            #print('Точка: '+str([p1.X(),p1.Y(),p1.Z(),]))
            if (len(result)==0) or (p1 <> result[-1]):
                result = result + [p1]
            sv=ex.Next()
            if not ex.More():
                break
    return result

def makeLINESTRING(pnts):
    geom = "GeomFromEWKT('SRID=-1;LINESTRING("
    j = 0
    for p in pnts:
        if (j > 0):
            geom = geom + ","
        j = 1
        geom = geom + "%.0f %.0f %.0f"%(p[0],p[1],p[2])
    geom = geom + ")')"
    return geom

def distance2d(p1,p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

def distance3d(p1,p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]) + (p1[2]-p2[2])*(p1[2]-p2[2]))


def getMNK(cloud, offset=[0,0] ):    #  [[x,y,z],...]
    """ Поиск линейной аппроксимации облака точек cloud = [[x,y,z], ...]
    z = b0 + b1*x + b2*y
    результат коэффициенты полинома:
    B = [ b0 ,  b1 , b2 ]
    b0 = B[0,0]; b1 = B[1,0]; b2 = B[2,0] 
    [b0,b1,b2]  
    """
    res = []
    xc = offset[0]; yc = offset[1]
    nCloud = len(cloud)
    if nCloud < 3 :
        #print "Нет решения для ", cloud 
        return res
    sz = 0.0; zz = 0.0; zx = 0.0; zy = 0.0; sx = 0.0; sy = 0.0; xx = 0.0; yy = 0.0; xy = 0.0
    for point in cloud:
        x,y,z = point
        x = x - xc; y = y - yc
        sx = sx + x
        sy = sy + y
        sz = sz + z
        zz = zz + z*z
        zx = zx + z*x
        zy = zy + z*y
        xx = xx + x*x
        yy = yy + y*y
        xy = xy + x*y
    D = matrix([[sz], [zx], [zy]])
    A = matrix([[nCloud, sx, sy], [sx, xx, xy], [sy, xy, yy] ])
    try:
        res = linalg.solve(A, D); 
        res = [res[0,0],res[1,0],res[2,0]]
    except:
        res = []
        #print "Нет решения для ", cloud   
    return res

def getGrad(pnt, cloud):
    grad = [0.0,0.0]
    n = 0
    for p in cloud:
        if p <> pnt:
            dist = distance2d(pnt,p)
            if dist > 0.001:
                grP = (p[2]-pnt[2])/dist
                grPx = grP * (p[0]-pnt[0]) / dist
                grPy = grP * (p[1]-pnt[1]) / dist
                grad[0] = grad[0] + grPx
                grad[1] = grad[1] + grPy
                n = n + 1
    if n>0:
        grad[0] = grad[0] / n
        grad[1] = grad[1] / n            
    return grad            
                
def getNear(pnt, cloud):
    near = []
    if cloud:
        near = cloud[0]
        for p in cloud[1:]:
            if distance2d(pnt,p) < distance2d(pnt,near):
                near = p
    return near            


#Points coords configuration dialog
class CoordsDlg(wx.Dialog):
    def __init__(self,parent,ID,title,coords=[],
                 size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, (570,300), style)
        self.this = pre.this        

	self.panel2 = wx.BoxSizer(wx.HORIZONTAL)
	
	AddLineBtn=wx.Button(self, -1, "Добавить точку")
	self.Bind(wx.EVT_BUTTON, self.OnAddLine, AddLineBtn)
        self.panel2.Add(AddLineBtn)

	DelLineBtn=wx.Button(self, -1, "Удалить точку")
	self.Bind(wx.EVT_BUTTON, self.OnDelLines, DelLineBtn)
        self.panel2.Add(DelLineBtn)

	self.panel3 = wx.BoxSizer(wx.HORIZONTAL)
	CloseBtn=wx.Button(self, -1, "Закрыть без сохранения")
	self.Bind(wx.EVT_BUTTON, self.OnClose, CloseBtn)
        self.panel3.Add(CloseBtn)
	SaveBtn=wx.Button(self, -1, "Сохранить")
	self.Bind(wx.EVT_BUTTON, self.OnSave, SaveBtn)
        self.panel3.Add(SaveBtn)

	self.panel1 = wx.BoxSizer(wx.VERTICAL)
	self.grid=wx.grid.Grid(self, -1,size=(570,260),name = "Coords")
	self.grid.CreateGrid(1,3,1)
	self.grid.SetColLabelValue(0,"x")
	self.grid.SetColLabelValue(1,"y")
	self.grid.SetColLabelValue(2,"z")
	#self.Bind(wx.grid.EVT_GRID_CELL_CHANGE,self.OnCellChange,self.grid)
	self.panel1.Add(self.grid,0, wx.EXPAND)
	self.panel1.Add(self.panel2, 0, wx.EXPAND)

	self.superMainPanel = wx.BoxSizer(wx.VERTICAL)
	self.superMainPanel.Add(self.panel1)
	self.superMainPanel.Add(self.panel3)
	self.SetSizer(self.superMainPanel)
        self.SetAutoLayout(1)
        self.superMainPanel.Fit(self)
	
	self.grid.ClearGrid()
	self.grid.DeleteRows(0,self.grid.GetNumberRows(),True)
	for i in range(len(coords)):
	    self.grid.AppendRows(1,True)
	    for j in range(3):
		if coords[i][j]=='':
		    self.grid.SetCellValue(i,j,'0')
		else:
		    self.grid.SetCellValue(i,j,str(coords[i][j]))

	self.save=False		
	
    def OnAddLine(self,event):
	self.grid.AppendRows(1,True)

    def OnDelLines(self,event):
	self.grid.DeleteRows(self.grid.GetNumberRows()-1,1,True)

    def OnClose(self,event):
	self.Close()

    def OnSave(self,event):
	self.save=True
	self.Close()

    def ret(self):
	result=[]
	for i in range(self.grid.GetNumberRows()):
	    result.append([0,0,0])
	    for j in range(3):
		if not self.grid.GetCellValue(i,j)=='':
		    result[i][j]=float(self.grid.GetCellValue(i,j))
	return result                 
                
                 
