#!/usr/bin/env python
# -*- coding: utf-8 -*-
##Copyright 2008-2009 Thomas Paviot
##
##thomas.paviot@free.fr.fr
##
##pythonOCC is a computer program whose purpose is to provide a complete set
##of python bindings for OpenCasacde library.
##
##This software is governed by the CeCILL license under French law and
##abiding by the rules of distribution of free software.  You can  use, 
##modify and/ or redistribute the software under the terms of the CeCILL
##license as circulated by CEA, CNRS and INRIA at the following URL
##"http://www.cecill.info". 
##
##As a counterpart to the access to the source code and  rights to copy,
##modify and redistribute granted by the license, users are provided only
##with a limited warranty  and the software's author,  the holder of the
##economic rights,  and the successive licensors  have only  limited
##liability. 
##
##In this respect, the user's attention is drawn to the risks associated
##with loading,  using,  modifying and/or developing or reproducing the
##software by the user in light of its specific status of free software,
##that may mean  that it is complicated to manipulate,  and  that  also
##therefore means  that it is reserved for developers  and  experienced
##professionals having in-depth computer knowledge. Users are therefore
##encouraged to load and test the software's suitability as regards their
##requirements in conditions enabling the security of their systems and/or 
##data to be ensured and,  more generally, to use and operate it in the 
##same conditions as regards security. 
##
##The fact that you are presently reading this means that you have had
##knowledge of the CeCILL license and that you accept its terms.

#from __future__ import nested_scopes

#import OCC
from OCC import TopAbs, TopoDS, BRep, TopExp
from OCC.AIS import AIS_Shape
from OCC.TopoDS import TopoDS_Shape
from OCC.BRep import *
from OCC.BRepBuilderAPI import *
from OCC.BRepOffsetAPI import *
from OCC.BRepPrimAPI import *
from OCC.Display.OCCViewer import Viewer3d
from OCC.Geom import *
from OCC.Geom2d import *
from OCC.GeomAPI import *
from OCC.GeomAbs import *
#from OCC.KBE.TypesLookup import ShapeToTopology
from OCC.KBE.types_lut import ShapeToTopology
from OCC.Precision import *
from OCC.Quantity import *
from OCC.TColgp import *
from OCC.Utils.Topology import Topo
from OCC.gp import *
from regim import *
from utils import *
#from OCC.BRep.BRep_Tool import Curve
from OCC.Visual3d import Visual3d_Layer
from OCC.Aspect import *
from OCC import BRep
from OCC import Prs3d

import math
import sys
import os
import os.path
import sys
import wx
import types

# --------------------------------------------------
try:
    THISPATH = os.path.dirname(os.path.abspath(__file__))
except:
    THISPATH = os.path.dirname(os.path.abspath(sys.argv[0]))
if THISPATH.endswith("zip"):
    THISPATH = os.path.dirname(THISPATH)
# --------------------------------------------------

class GraphicsCanva3D(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
 
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_IDLE(self, self.OnIdle)
        wx.EVT_MOVE(self, self.OnMove)
        wx.EVT_SET_FOCUS(self, self.OnFocus)
        wx.EVT_KILL_FOCUS(self, self.OnLostFocus)
        wx.EVT_MAXIMIZE(self, self.OnMaximize)

        wx.EVT_LEFT_DOWN(self, self.OnLeftDown)
        wx.EVT_LEFT_UP(self, self.OnLeftUp)
        wx.EVT_RIGHT_DOWN(self, self.OnRightDown)
        wx.EVT_MIDDLE_DOWN(self, self.OnMiddleDown)
        wx.EVT_RIGHT_UP(self, self.OnRightUp)
        wx.EVT_MIDDLE_UP(self, self.OnMiddleUp)
        wx.EVT_MOTION(self, self.OnMotion)
        wx.EVT_KEY_DOWN(self,self.OnKeyDown)

        self._3dDisplay     = None
        self._inited        = False
        self.DynaZoom       = False
        self.WinZoom        = False
        self.DynaRotate     = False
        self.DynaPan        = False
        # GIS
        self.MakeErase      = False
        self.MakeLine       = False
        self.MakePLine      = False
        self.worldPt        = None     #Для использования в нити
        self.dragStartPos   = None
        self._drawbox       = None
        self._selection     = None
        self.color          = "Yellow"
        self.thickness      = 1
        self.pen            = wx.Pen(self.color, self.thickness, wx.SOLID)
        self._drawline      = []
        #self.m_hLayer       = None    #Для использования в нити на рабочем слое
        #self.dc=wx.ClientDC(self)
        self.EdStep         = None
        self.EdCmd          = None

        self.gumline_edge = None
        self.MakePoint = False

        if sys.platform=='win32':
            self.Init3dViewer()

    def Init3dViewer(self):
        self._3dDisplay = Viewer3d(self.GetHandle())
        self._3dDisplay.Create()
        self._inited = True
        #self._3dDisplay.SetBackgroundImage(os.path.join(THISPATH, "icons", "bgWhite.bmp"))
        self._3dDisplay.DisplayTriedron()
        ##self._3dDisplay.SetModeShaded()
        self._3dDisplay.SetModeWireFrame()
        self._3dDisplay.Context.SetTrihedronSize(10.0)

    def OnKeyDown(self,evt):
        key_code = evt.GetKeyCode()
        if key_code==87:#"W"
            self._3dDisplay.SetModeWireFrame()
        elif key_code==83:#"S"
            self._3dDisplay.SetModeShaded()
        elif key_code==65:#"A"
            self._3dDisplay.EnableAntiAliasing()
        elif key_code==66:#"B"
            self._3dDisplay.DisableAntiAliasing()
              
    def OnSize(self, event):
        if self._inited:
            self._3dDisplay.OnResize()

    def OnMaximize(self, event):
        if self._inited:
            self._3dDisplay.Repaint()
        
    def OnMove(self, event):
        if self._inited:
            self._3dDisplay.Repaint()

    def OnIdle(self, event):
        if self._inited:
            self._3dDisplay.Repaint()

    def Test(self):
        if self._inited:
            self._3dDisplay.Test()
        
    def OnFocus(self, event):
        if self._inited:
            self._3dDisplay.Repaint()
        
    def OnLostFocus(self, event):
        if self._inited:
            self._3dDisplay.Repaint()

    def OnPaint(self, event):
        #pass
        if self._inited:
            self._3dDisplay.Repaint()
        
    def ZoomAll(self):
        self._3dDisplay.FitAll()#Zoom_FitAll()

    def Repaint(self, evt):
        #pass
        if self._inited:
            self._3dDisplay.Repaint()

    def OnLeftDown(self, evt):
        """ Обработка левой кнопки мыши. 
        Здесь все, что требует указания на экране для выполнения функций ГГИС """
        
        # Расчет позиции точки в мировх координатах
        
        self.startPt = evt.GetPosition()
        xt, yt, zt, Pt,Ut,Vt = self._3dDisplay.GetView().GetObject().ConvertWithProj(self.startPt.x, self.startPt.y) #, Xw,Yw,Zw
        resPnt = [xt,yt,zt]
        self.worldPt = resPnt
        # Обслуживание привязок
        snap = self.frame.canva.snap.GetCurrentSelection()
        if snap == 0:       # нет привязки
            pass
        elif snap == 1:     # end
            self._3dDisplay.Select(self.startPt.x, self.startPt.y)
            sel_shape=self._3dDisplay.selected_shape
            pnts = getPoints(sel_shape)
            #print sel_shape, pnts
            if pnts:
                minP = pnts[0]
                minD = distance2d(resPnt, minP)
                for cur in pnts:
                    curD = distance2d(resPnt, cur)
                    if curD < minD:
                        minP = cur
                        minD = curD
                resPnt = minP   # result point
            pass
        elif snap == 2:    # near
            self._3dDisplay.Select(self.startPt.x, self.startPt.y)
            sel_shape = self._3dDisplay.selected_shape
            if sel_shape:
                pnts = getPoints(sel_shape)
                midleH = 0
                for pnt in pnts:
                    midleH += pnt[2]
                midleH = midleH/len(pnts)
                cur = gp_Pnt(resPnt[0],resPnt[1],midleH)
                      
                te = ShapeToTopology()
                bt = BRep.BRep_Tool()
                #print bt
                isP1 = False
                isNea = False
                for pnt in pnts:
                    if not isP1:
                        p1 = pnt
                        isP1 = True
                    else:
                        p2 = pnt
                        edge = BRepBuilderAPI_MakeEdge(gp_Pnt(p1[0], p1[1], p1[2]),
                                                       gp_Pnt(p2[0], p2[1], p2[2])).Edge()
                        curve = bt.Curve(edge)[0]
                        proj_P_C = GeomAPI_ProjectPointOnCurve(cur, curve)
                        proj = proj_P_C.NearestPoint()
                        if not isNea:
                            isNea = True
                            nea = proj
                            neaP1 = p1; neaP2 = p2
                        else:
                            if (nea.Distance(cur) > proj.Distance(cur)):
                                nea = proj
                                neaP1 = p1; neaP2 = p2
                        p1 = p2
                resPnt = [nea.X(),nea.Y(),nea.Z()]
                #print resPnt,[neaP1[0],neaP1[1],neaP1[2]],[neaP2[0],neaP2[1],neaP2[2]]           
            pass
        elif snap == 3:    # center
            self._3dDisplay.Select(self.startPt.x, self.startPt.y)
            sel_shape = self._3dDisplay.selected_shape
            if sel_shape:
                pnts = getPoints(sel_shape)
                midleH = 0
                for pnt in pnts:
                    midleH += pnt[2]
                midleH = midleH/len(pnts)
                cur = gp_Pnt(resPnt[0],resPnt[1],midleH)
                      
                te = ShapeToTopology()
                bt = BRep.BRep_Tool()
                #print bt
                isP1 = False
                isNea = False
                for pnt in pnts:
                    if not isP1:
                        p1 = pnt
                        isP1 = True
                    else:
                        p2 = pnt
                        edge = BRepBuilderAPI_MakeEdge(gp_Pnt(p1[0], p1[1], p1[2]),
                                                       gp_Pnt(p2[0], p2[1], p2[2])).Edge()
                        curve = bt.Curve(edge)[0]
                        proj_P_C = GeomAPI_ProjectPointOnCurve(cur, curve)
                        proj = proj_P_C.NearestPoint()
                        if not isNea:
                            isNea = True
                            nea = proj
                            neaP1 = p1; neaP2 = p2
                        else:
                            if (nea.Distance(cur) > proj.Distance(cur)):
                                nea = proj
                                neaP1 = p1; neaP2 = p2
                        p1 = p2
                #resPnt = [nea.X(),nea.Y(),nea.Z()]
                cx=min(neaP1[0],neaP2[0])+math.fabs(max(neaP1[0],neaP2[0])-min(neaP1[0],neaP2[0]))/2
                cy=min(neaP1[1],neaP2[1])+math.fabs(max(neaP1[1],neaP2[1])-min(neaP1[1],neaP2[1]))/2
                cz=min(neaP1[2],neaP2[2])+math.fabs(max(neaP1[2],neaP2[2])-min(neaP1[2],neaP2[2]))/2
                resPnt = [cx,cy,cz]
            pass
        elif snap == 4:    # tangent
            pass
        # Координаты точки в окно координат 
        self.frame.canva.coord.SetValue("%.1f,%.1f"%(resPnt[0],resPnt[1]))
        #self.frame.canva.coord.SetValue("%.2f,%.2f,%.2f"%(resPnt[0],resPnt[1],resPnt[2]))

        if self.MakeLine:
            self.frame.SetStatusText("Отрезок. Дай конец", 0)
            #self.frame.canva.lstPnt = self.frame.canva.lstPnt + [resPnt]
            self.worldPt = resPnt
            return

        if self.MakePLine:
            self.frame.SetStatusText("Полилиния. Дай далееﾵ", 0)
            #self.frame.canva.lstPnt = self.frame.canva.lstPnt + [resPnt]
            self.worldPt = resPnt
            return 
        
        if self.MakePoint:
            self.worldPt = resPnt
            self.frame.onCoord_yes(evt)
            return 

        self.dragStartPos = self.startPt        #evt.GetPosition()
        self._3dDisplay.MoveTo(self.dragStartPos.x,self.dragStartPos.y)     # cyx 
        self._3dDisplay.StartRotation(self.dragStartPos.x,self.dragStartPos.y)
        
        self._3dDisplay.Select(self.dragStartPos.x, self.dragStartPos.y)

        ### Вставить вершину в линию
        if (self.EdCmd == CMD_EdBrInsV) and (self.EdStep == 1):
            sel_shape=self._3dDisplay.selected_shape
            if not sel_shape:
                return
            # Получить цвет, тип линии, толщину и др. параметры линии
            selObj = self._3dDisplay.Context.SelectedInteractive()
            type=self.frame.getTypeByMenu()
            indexInfo = None;
            for i in range(len(self.drawList)):
                s1 = self.drawList[i][2]
                if s1:
                    if (s1.Shape().IsEqual(sel_shape)):     # Только в классе Shape есть метод IsEqual()
                        indexInfo = i
                        break
            if indexInfo<>None:
                if not self.drawList[indexInfo][0]==type:
                    self.frame.SetStatusText("Это не "+str(type_labels[type]), 2)
                    self.EdCmd = 0; self.EdStep = 0
                    # Восстановить старые привязки
                    self.frame.canva.snap.SetSelection(0)
                    return
            selColor = None
            if selObj.GetObject().HasColor():
                selColor = self._3dDisplay.Context.Color(selObj)
            #print("selColor=", selColor)
            # добавить resPnt к линии между neaP1 и neaP2
            newPnts = []
            for pnt in pnts:
                newPnts = newPnts + [pnt]
                if pnt == neaP1:
                     newPnts = newPnts + [resPnt]
            #print newPnts 

            # get params sel object
            self._3dDisplay.Context.Erase(selObj)           # Удалить старый
            plgn = BRepBuilderAPI_MakePolygon()             # Построить новый
            for pnt1 in newPnts:
                plgn.Add(gp_Pnt(pnt1[0], pnt1[1], pnt1[2]))
            #if closeP:
            #    plgn.Close()
            w = plgn.Wire()
            newShape = self._3dDisplay.DisplayColoredShape(w,'YELLOW', False)        #,'WHITE'
            # Установить цвет, тип,толщину и др.
            if selColor:
                self._3dDisplay.Context.SetColor(newShape,selColor,0)
            if indexInfo <> None:
                oldInfo = self.drawList[indexInfo]
                #print oldInfo
                oldInfo[2] = newShape.GetObject()
                oldInfo[-1] = True
                #print oldInfo
                self.drawList[indexInfo] = oldInfo          # Обновить список
            self.frame.SetStatusText("Готово!", 2)
            self.EdCmd = 0; self.EdStep = 0
            # Восстановить старые привязки
            self.frame.canva.snap.SetSelection(0)
            pass

        if (self.EdCmd == CMD_EdBrMoveV) and (self.EdStep == 1):
            # move vertex
            pass

        ### разорвать линию
        if (self.EdCmd == CMD_EdBrBrkV) and (self.EdStep == 1):
            sel_shape=self._3dDisplay.selected_shape
            if not sel_shape:
                return
            # Получить цвет, тип линии, толщину и др. параметры линии
            selObj = self._3dDisplay.Context.SelectedInteractive()
            type=self.frame.getTypeByMenu()
            indexInfo = None;
            for i in range(len(self.drawList)):
                s1 = self.drawList[i][2]
                if s1:
                    if (s1.Shape().IsEqual(sel_shape)):     # Только в классе Shape есть метод IsEqual()
                        indexInfo = i
                        break
            if indexInfo<>None:
                if not self.drawList[indexInfo][0]==type:
                    self.frame.SetStatusText("Это не "+str(type_labels[type]), 2)
                    self.EdCmd = 0; self.EdStep = 0
                    # Восстановить старые привязки
                    self.frame.canva.snap.SetSelection(0)
                    return
            selColor = None
            if selObj.GetObject().HasColor():
                selColor = self._3dDisplay.Context.Color(selObj)
            #print("selColor=", selColor)
            newPntsFirst = []
            newPntsSecond = []

            #найти местоположение разрыва
            index=0
            for i in range(len(pnts)):
                if pnts[i]==neaP1:
                    index=i
                    break
            #задать точки для половины до разрыва
            for i in range(index+1):
                newPntsFirst.append(pnts[i])
            newPntsFirst.append(resPnt) 
            #задать точки для половины после разрыва
            newPntsSecond.append(resPnt)
            for i in range(index+1,len(pnts)):
                newPntsSecond.append(pnts[i])

            #print newPntsFirst
            #print newPntsSecond
            # get params sel object
            self._3dDisplay.Context.Erase(selObj)           # Удалить старый

            plgn1 = BRepBuilderAPI_MakePolygon()             # Построить первую половину
            for pnt1 in newPntsFirst:
                plgn1.Add(gp_Pnt(pnt1[0], pnt1[1], pnt1[2]))
            #if closeP:
            #    plgn.Close()
            w1 = plgn1.Wire()
            newShape1 = self._3dDisplay.DisplayColoredShape(w1,'YELLOW', False)

            plgn2 = BRepBuilderAPI_MakePolygon()             # Построить вторую половину
            for pnt1 in newPntsSecond:
                plgn2.Add(gp_Pnt(pnt1[0], pnt1[1], pnt1[2]))
            #if closeP:
            #    plgn.Close()
            w2 = plgn2.Wire()
            newShape2 = self._3dDisplay.DisplayColoredShape(w2,'YELLOW', False)

            # Установить цвет, тип,толщину и др.
            if selColor:
                self._3dDisplay.Context.SetColor(newShape1,selColor,0)
                self._3dDisplay.Context.SetColor(newShape2,selColor,0)
            if indexInfo <> None:
                self.drawList[indexInfo][2] = newShape1.GetObject()
                self.drawList[indexInfo][-1] = True
                #print oldInfo
                #self.drawList[indexInfo] = oldInfo          # Обновить список
                #создать новый объект
                newInfo = []
                for i in range(len(self.drawList[indexInfo])):
                    newInfo.append(self.drawList[indexInfo][i])
                newInfo[1] = -1
                newInfo[2] = newShape2.GetObject()
                newInfo[-1]=True
                self.drawList=self.drawList+[newInfo]

            self.frame.SetStatusText("Готово!", 2)
            self.EdCmd = 0; self.EdStep = 0
            # Восстановить старые привязки
            self.frame.canva.snap.SetSelection(0)
            pass
        
        ### Удалить линию с экрана и из списка объектов, если есть
        if (self.EdCmd == CMD_EdBrDelB) and (self.EdStep == 1):
            # delete edge
            # s = None; Mod = True; Save As -> DELETE FROM edge
            sel_shape = self._3dDisplay.selected_shape
            if sel_shape:
                selObj = self._3dDisplay.Context.SelectedInteractive()
                type=self.frame.getTypeByMenu()
                indexInfo = None; 
                for i in range(len(self.drawList)):
                    s1 = self.drawList[i][2]
                    if s1:
                        if (s1.Shape().IsEqual(sel_shape)):
                            indexInfo = i
                            break
                if indexInfo <> None:
                    oldInfo = self.drawList[indexInfo]
                    if oldInfo[0]==type or type==-1:
                        oldInfo[2] = None
                        oldInfo[-1] = True
                        self.drawList[indexInfo] = oldInfo
                        self._3dDisplay.Context.Erase(selObj)
                        self.frame.SetStatusText("Удален", 2)
                    else:
                        self.frame.SetStatusText("Это не "+str(type_labels[type]), 2)
                else:
                    self._3dDisplay.Context.Erase(selObj)
                    self.frame.SetStatusText("Удален", 2)
                self.EdCmd = 0; self.EdStep = 0
            pass        
            
    def OnLeftUp(self, evt):
        if self.WinZoom:
            self.WinZoom = False
            dc = wx.ClientDC(self)
            dc.BeginDrawing()
            dc.SetPen(wx.Pen(wx.WHITE, 1, wx.DOT))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            if self._drawbox:
                r = wx.Rect(*self._drawbox)
                dc.DrawRectangleRect(r)
                myXmin, myYmin, myXd, myYd = self._drawbox
            if self._drawline:
                #dc.DrawLine(self._drawline)
                dc.DrawLine(self._drawline[0],self._drawline[1],self._drawline[2],self._drawline[3])
            dc.EndDrawing()
            ##myXmin, myYmin, myXd, myYd = self._drawbox
            self._3dDisplay.ZoomArea(myXmin, myYmin, myXmin+myXd, myYmin+myYd)
            self._drawbox = None
            #myView->WindowFitAll(myXmin, myYmin, myXmax, myYmax);
        if  self.MakeLine or self.MakePLine:
            # Удалить локальный контекст
            pass
        pass        #***************************************

    def OnRightUp(self, event):
        self._inited = True
        self.SetDynaCursor()
        self._3dDisplay.Repaint()
        self._drawbox = False
        if event.ControlDown() and event.ShiftDown():
            pt = event.GetPosition()
            if ((abs(self.dragStartPos.x - pt.x)>1) or (abs(self.dragStartPos.y - pt.y)>1)): 
                self._3dDisplay.Zoom_Window(self.dragStartPos.x, self.dragStartPos.y, pt.x, pt.y)

    def OnRightDown(self, event):
        self.dragStartPos = event.GetPosition()
        if (self.MakeLine or self.MakePLine):
            self.frame.onCoord_yes(event)
            return
        self._3dDisplay.StartRotation(self.dragStartPos.x,self.dragStartPos.y)        
        self.SetTogglesToFalse(None)

    def SetTogglesToFalse(self, event):
        self.DynaZoom = False
        self.WinZoom = False
        self.DynaPan = False
        self.DynaRotate = False
        #self.MakeLine = False
        #self.MakePLine = False
        
    def OnMiddleDown(self, event):
        self.dragStartPos = event.GetPosition()
        self._3dDisplay.StartRotation(self.dragStartPos.x,self.dragStartPos.y) 
        self.CentreDisplayToggle = True
        
    def OnMiddleUp(self, event):
        self.SetDynaCursor()
        if self.CentreDisplayToggle:
            self.dragStartPos = event.GetPosition()
            self._3dDisplay.SetCentre(self.dragStartPos.x, self.dragStartPos.y)

    def _winzoom(self, event):
        self._inited = False
        tolerance = 2
        pt = event.GetPosition()
        dx = pt.x - self.dragStartPos.x
        dy = pt.y - self.dragStartPos.y
        
        if abs(dx) <= tolerance and abs(dy) <= tolerance:
            return
        dc = wx.ClientDC(self)
        dc.BeginDrawing()
        dc.SetPen(wx.Pen(wx.WHITE, 1, wx.DOT))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetLogicalFunction(wx.XOR)
        if self._drawbox:
            r = wx.Rect(*self._drawbox)
            dc.DrawRectangleRect(r)

        r = wx.Rect(self.dragStartPos.x, self.dragStartPos.y , dx, dy)
        dc.DrawRectangleRect(r)
        dc.EndDrawing()
        self._drawbox = [self.dragStartPos.x, self.dragStartPos.y , dx, dy]

    def SetDynaCursor(self, iconfile=""):
        """Set the cursor for zoom, pan or rotate."""
        if iconfile:
            img = wx.Bitmap(iconfile)
            img_mask = wx.Mask(img, wx.Colour(255, 0, 255))
            img.SetMask(img_mask)
            cursor = wx.CursorFromImage(wx.ImageFromBitmap(img))
        else:
            cursor = wx.StockCursor(wx.CURSOR_DEFAULT)
        self.SetCursor(cursor)


    def _dynazoom(self,event):
        self.SetDynaCursor(os.path.join(THISPATH, "icons", "zoom_cur.bmp"))
        pt = event.GetPosition()
        self._3dDisplay.Repaint()
        self._3dDisplay.DynamicZoom(abs(self.dragStartPos.x), abs(self.dragStartPos.y), abs(pt.x), abs(pt.y))
        self.dragStartPos.x = pt.x 
        self.dragStartPos.y = pt.y

    def _dynarotate(self, event):
        self.SetDynaCursor(os.path.join(THISPATH, "icons", "rotate_cur.bmp"))
        pt = event.GetPosition()
        dx = pt.x - self.dragStartPos.x
        dy = pt.y - self.dragStartPos.y
        self._3dDisplay.Rotation(pt.x,pt.y)

    def _dynapan(self, event):
        self.SetDynaCursor(os.path.join(THISPATH, "icons", "pan_cur.bmp"))
        pt = event.GetPosition()
        dx = pt.x - self.dragStartPos.x
        dy = pt.y - self.dragStartPos.y
        self.dragStartPos.x = pt.x 
        self.dragStartPos.y = pt.y
        self._3dDisplay.Repaint()
        self._3dDisplay.Pan(dx,-dy)
        
    def OnMotion(self, event):
        self.CentreDisplayToggle = False
        if self.DynaZoom and event.Dragging():
            self._dynazoom(event)
        if self.WinZoom and event.Dragging():
            self._winzoom(event)
        if self.DynaRotate and event.Dragging():
            self._dynarotate(event)
        if self.DynaPan and event.Dragging():
            self._dynapan(event)
        if not event.Dragging() or (not event.RightIsDown() and not event.MiddleIsDown()):
            view = self._3dDisplay.GetView().GetObject()            
            # view = <OCC.V3d.V3d_View; proxy of <Swig Object of type 'V3d_View *' at 0xa2d3a60> >
            pt = event.GetPosition()
            #if (self.GumLine and self.worldPt):
            if (self.GumLine and len(self.lstPnt)>0):
                pntDspl = view.Convert(self.lstPnt[-1][0], self.lstPnt[-1][1], self.lstPnt[-1][2])
                
                dc=wx.ClientDC(self)
                dc.BeginDrawing()
                dc.SetPen(wx.Pen(wx.BLACK, 1, wx.SOLID))##     BLACK_DASHED_PEN ##DOT
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.SetLogicalFunction(wx.COPY)
                if self._drawline:
                    #dc.DrawLine(self._drawline)
                    dc.DrawLine(self._drawline[0],self._drawline[1],self._drawline[2],self._drawline[3])
                dc.DrawLine(pntDspl[0],pntDspl[1], pt.x,pt.y)
                self._drawline = [pntDspl[0],pntDspl[1], pt.x,pt.y]
                dc.EndDrawing()
                
                resPnt = self._3dDisplay.GetView().GetObject().ConvertWithProj(pt.x, pt.y) #, Xw,Yw,Zw
                Z = float(self.coordZ.GetValue())
                edge = BRepBuilderAPI_MakeEdge(gp_Pnt(self.lstPnt[-1][0], self.lstPnt[-1][1], self.lstPnt[-1][2]),gp_Pnt(resPnt[0], resPnt[1], Z+0*resPnt[2])).Edge()
                if self.gumline_edge:
                    self._3dDisplay.Context.Erase(self.gumline_edge)
                shape=OCC.AIS.AIS_Shape(edge)
                shape.UnsetSelectionMode()
                self.gumline_edge = shape.GetHandle()
                self._3dDisplay.Context.SetColor(self.gumline_edge,OCC.Quantity.Quantity_NOC_BLACK,0)
                self._3dDisplay.Context.Display(self.gumline_edge, False)
                #self.gumline_edge=self.DisplayCustomShape(edge, color='BLACK', update=False, line_type = 1, line_thickness = 1,toggle=False)

                #view_mgr = display.View.View().GetObject().ViewManager()
                #layer = Visual3d_Layer(view_mgr, Aspect_TOL_UNDERLAY, False)
                #if (self.m_hLayer == None):
                #    view_mgr = self._3dDisplay.View.View().GetObject().ViewManager()
                #    #print view_mgr = <OCC.Visual3d.Handle_Visual3d_ViewManager; proxy of <Swig Object of type 'Handle_Visual3d_ViewManager *' at 0xb005240> >
                #    #self.m_hLayer = Visual3d_Layer(view_mgr, Aspect_TOL_UNDERLAY, False)
                #    self.m_hLayer = Visual3d_Layer(view_mgr, Aspect_TOL_OVERLAY, False)                
                #    print self.m_hLayer #= <OCC.Visual3d.Visual3d_Layer; proxy of <Swig Object of type 'Visual3d_Layer *' at 0xaaff180> >
                #    h,w = (640,480)
                #    #h,w = self._3dDisplay.View.Window().GetObject().Size()
                #    print h,w
                #    self.m_hLayer.SetViewport(h,w); 
                #    #self.m_hLayer.SetColor (Quantity_Color(Quantity_NOC_WHITE))
                #    #self.m_hLayer.SetLineAttributes(Aspect_TOL_DOT, 1.0); 

                #self.m_hLayer.Clear(); 
                #self.m_hLayer.Begin(); 
                #self.m_hLayer.BeginPolyline(); 
                #self.m_hLayer.AddVertex(pntDspl[0],pntDspl[1]); 
                #self.m_hLayer.AddVertex(pt.x,pt.y);                 
                #self.m_hLayer.End(); 
                #print 'end'
                #self._3dDisplay.Test()
                #print 'test'
                #view.Redraw();
                #self._3dDisplay.Repaint()
                #print 'repaint'
                #return
            else:
                dc=wx.ClientDC(self)
                dc.SetLogicalFunction(wx.COPY)                
            self._3dDisplay.MoveTo(pt.x,pt.y)   # Уход в ОСС для обработки выбора около точки
            # отобразить координаты в статусной строке
            view = self._3dDisplay.GetView().GetObject()
            xt, yt, zt, Pt,Ut,Vt = view.ConvertWithProj(pt.x,pt.y) #, Xw,Yw,Zw
            self.frame.SetStatusText("%.0f,%.0f"%(xt,yt), 1)
            #self.frame.canva.coord.SetValue("%.2f,%.2f"%(xt,yt))
        elif event.Dragging() and event.RightIsDown() and event.ControlDown() and event.ShiftDown():
            # Zoom win
            #self._winzoom(event)
            pass    
        elif (event.Dragging() and event.RightIsDown() and event.ControlDown()) or \
                (event.Dragging() and event.RightIsDown() and event.MiddleIsDown()):
            # Dyna Zoom
            self._dynazoom(event)
            
        elif (event.Dragging() and event.MiddleIsDown()) or \
                (event.Dragging() and event.RightIsDown() and event.ShiftDown()):
            # Rotate
            self._dynarotate(event)
            
        elif event.Dragging() and event.RightIsDown():
            # Pan
            self._dynapan(event)
        
    def SaveAsImage(self, filename):
        """Save the current canvas view to an image file."""
        self._3dDisplay.ExportToImage(filename)


    def DisplayCustomShape(self, shapes, color='YELLOW', update=True, line_type = 0, line_thickness = 1,toggle=True, ):
        ais_shapes = []

        if isinstance(color, str):
            dict_color = {'WHITE':OCC.Quantity.Quantity_NOC_WHITE,
                          'BLUE':OCC.Quantity.Quantity_NOC_BLUE1,
                          'RED':OCC.Quantity.Quantity_NOC_RED,
                          'GREEN':OCC.Quantity.Quantity_NOC_GREEN,
                          'YELLOW':OCC.Quantity.Quantity_NOC_YELLOW,
                          # new
                          'CYAN':OCC.Quantity.Quantity_NOC_CYAN1,
                          'WHITE':OCC.Quantity.Quantity_NOC_WHITE,
                          'BLACK':OCC.Quantity.Quantity_NOC_BLACK,
                          'ORANGE':OCC.Quantity.Quantity_NOC_ORANGE, }
            color = dict_color[color]
        elif isinstance(color, OCC.Quantity.Quantity_Color):
            pass
        else:
            raise ValueError('color should either be a string ( "BLUE" ) or a Quantity_Color(0.1, 0.8, 0.1) got %s' % color)

        if issubclass(shapes.__class__, TopoDS_Shape):
            shapes = [shapes]
            SOLO = True
        else:
            SOLO = False
            
        if line_type==0:
            line_type=OCC.Aspect.Aspect_TOL_SOLID
        else:
            line_type=OCC.Aspect.Aspect_TOL_DASH
        
        for shape in shapes:
            shape_to_display=OCC.AIS.AIS_Shape(shape)
            if toggle==False:
                shape_to_display.UnsetSelectionMode()
            shape_to_display.SetContext(self._3dDisplay.Context.GetHandle())
            LineType=Prs3d.Prs3d_LineAspect(color, line_type, line_thickness);

            Drawer=shape_to_display.Attributes().GetObject()
            Drawer.SetWireAspect(LineType.GetHandle())
            Drawer.SetLineAspect(LineType.GetHandle())
            shape_to_display.SetAttributes(Drawer.GetHandle())
 
            shape_to_display=shape_to_display.GetHandle()
            ais_shapes.append(shape_to_display)
            if update:
                self._3dDisplay.Context.Display(shape_to_display, True)
                self._3dDisplay.FitAll()
            else:
                self._3dDisplay.Context.Display(shape_to_display, False)  
        if SOLO:
            return ais_shapes[0]
        else:
            return ais_shapes

if __name__=="__main__":
    from OCC.BRepPrimAPI import *
    class AppFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, -1, "wxDisplay3d sample", style=wx.DEFAULT_FRAME_STYLE,size = (640,480))
            self.canva = GraphicsCanva3D(self)
            #S = BRepPrimAPI_MakeTorus(400,100)
            #shape = S.Shape()
            #self.canva._3dDisplay.DisplayShape(S.Shape())
    app = wx.PySimpleApp()
    wx.InitAllImageHandlers()
    frame = AppFrame(None)
    frame.Show(True)
    app.SetTopWindow(frame)
    app.MainLoop()            
