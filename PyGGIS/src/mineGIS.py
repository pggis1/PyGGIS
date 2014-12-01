#!/usr/bin/env python
# -*- coding: utf-8 -*-
##Copyright 2008-2009 Andy Haywood
##
##thomas.paviot@free.fr
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

## (c) 2009-2012 Владимир Суханов (адаптация для горной ГИС) OCE 0.8.0, pythonOCC 0.5
""" Главное окно приложения ГГИС """
import sys
import os
import os.path
from addons import browser
#import urllib
from math import *

try:
    THISPATH = os.path.dirname(os.path.abspath(__file__))
    IS_EXE = False
except:
    THISPATH = os.path.dirname(os.path.abspath(sys.argv[0]))
    IS_EXE = True
if THISPATH.endswith("zip"):
    THISPATH = os.path.dirname(THISPATH)
    IS_EXE = True

import wx
import wx.aui
import wx.py
from wxDisplay import GraphicsCanva3D
from OCC import STEPControl, StlAPI, IGESControl, TopoDS, BRep, BRepTools
from OCC.AIS import AIS_Shape
from OCC.BRepBuilderAPI import *
from OCC.BRepPrimAPI import *
from OCC.BRepPrim import *
from OCC.TopTools import *
from OCC.gp import *
import psycopg2
from regim import *
from utils import *
from ggisFun import *

VERSION = "0.01"

def CreateMaskedBitmap(fname, h=16, w=16):
    '''Ceate a masked bitmap where the mask colour is pink.'''
    try:
        img = wx.Bitmap(fname)
        img.SetHeight(h)
        img.SetWidth(w)
        img_mask = wx.Mask(img, wx.Colour(255, 0, 255))
        img.SetMask(img_mask)
        return img
    except:
        return None


def CreatePng(fname, h=16, w=16):
    '''Ceate a png .'''
    try:
        img = wx.Bitmap(fname, wx.BITMAP_TYPE_PNG)
        img.SetHeight(h)
        img.SetWidth(w)
        return img
    except:
        return None


def CreateGif(fname, h=16, w=16):
    '''Ceate a gif.'''
    try:
        img = wx.Bitmap(fname, wx.BITMAP_TYPE_GIF)
        return img
    except:
        return None


def CreateXpm(fname, h=16, w=16):
    '''Ceate a xpm.'''
    try:
        img = wx.Bitmap(fname, wx.BITMAP_TYPE_XPM)
        img.SetHeight(h)
        img.SetWidth(w)
        return img
    except:
        return None


def GetRecentFiles(fname):
    '''Open a text file which contains details of the previously opened files.'''
    if os.path.isfile(fname):
        f = open(fname, 'r')
        files = f.read()
        f.close()
        result = []
        for f in files.split('\n'):
            if os.path.isfile(f):
                result.append(f)
        return result
    else: return []


def SaveRecentFiles(filelist, fname):
    '''Save the recent file list to the text file.'''
    if filelist:
        f = open(fname, 'w')
        counter = 0
        for filename in filelist:
            if os.path.isfile(filename) and counter < 10:
                f.write("%s\n" % filename)
                counter += 1
        f.flush
        f.close


def SaveLayout(maximised, position, size, perspective, fname):
    """Save the application window layout to a file."""
    f = open(fname, 'w')
    f.write("%s\n" % str(maximised))
    f.write("%s\n" % str(position))
    f.write("%s\n" % str(size))
    f.write(perspective)
    f.flush()
    f.close()


def LoadLayout(fname):
    """Read the application layout from a file."""
    try:
        f = open(fname, 'r')
        data = f.read().split("\n")
        maximised = eval(data[0])
        position = list(eval(data[1]))
        if position[0] < 0:
            position[0] = 0
        if position[1] < 0:
            position[1] = 0
        size = list(eval(data[2]))
        if size[0] < 100:
            size[0] = 100
        if size[1] < 100:
            size[1] = 100
        perspective = data[3]
        f.close()
        return maximised, position, size, perspective
    except:
        pass


def YesNo(parent, question, caption='Yes or No?'):
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result


class AppFrame(wx.Frame):
    def __init__(self, parent):
        """

        """
        wx.Frame.__init__(self, parent, - 1, "pyOCC ГГИС %s" % VERSION,
                          style=wx.DEFAULT_FRAME_STYLE, size=MW_SIZE)

        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        self._recentfiles = GetRecentFiles(os.path.join(THISPATH, "recentfiles"))

        #nb = wx.aui.AuiNotebook(self, -1, style = wx.NB_BOTTOM ,
        nb = wx.Notebook(self, -1, style = wx.NB_LEFT ,
                                size = wx.DefaultSize
                                #,size = self.GetSize()
                                )
        self.notebook = nb

        self.panel1 = wx.Panel(nb, -1, style=wx.CLIP_CHILDREN)  # Геометрия карьера
        nb.AddPage(self.panel1, 'К')

        self.panel1.win = wx.Panel(self.panel1, -1, size = wx.DefaultSize)

        topsizer_K = wx.BoxSizer(wx.HORIZONTAL)
        #topsizer_K_left = wx.BoxSizer( wx.VERTICAL );
        topsizer_K_left = wx.StaticBoxSizer( wx.StaticBox( self.panel1.win, -1, u"Проекция" ), wx.VERTICAL)
        topsizer_K_right = wx.BoxSizer(wx.VERTICAL)
        topsizer_K_right_top = wx.StaticBoxSizer(wx.StaticBox( self.panel1.win, -1, u"Сверху" ), wx.VERTICAL)
        topsizer_K_right_front = wx.StaticBoxSizer(wx.StaticBox( self.panel1.win, -1, u"Спереди" ), wx.VERTICAL)
        self.canva = GraphicsCanva3D(self.panel1.win, True)
        self.canva_top = GraphicsCanva3D(self.panel1.win)
        self.canva_front = GraphicsCanva3D(self.panel1.win)

        #projText=wx.StaticText(self.panel1.win, -1, u'Проекция', wx.DefaultPosition, wx.DefaultSize, 0)
        #topText=wx.StaticText(self.panel1.win, -1, u'Сверху', wx.DefaultPosition, wx.DefaultSize, 0)
        #leftText=wx.StaticText(self.panel1.win, -1, u'Спереди', wx.DefaultPosition, wx.DefaultSize, 0)

        #topsizer_K_left.Add(projText, 0, wx.ALL, 1)
        topsizer_K_left.Add(self.canva, 1, wx.EXPAND|wx.ALL, 0)

        #topsizer_K_right.Add(topText, 0, wx.ALL, 1)
        topsizer_K_right_top.Add(self.canva_top, 1, wx.EXPAND|wx.ALL, 0)
        #topsizer_K_right.Add(leftText, 0, wx.ALL, 1)
        topsizer_K_right_front.Add(self.canva_front, 1, wx.EXPAND|wx.ALL, 0)

        topsizer_K_right.Add(topsizer_K_right_top, 1, wx.EXPAND|wx.ALL, 0)
        topsizer_K_right.Add(topsizer_K_right_front, 1, wx.EXPAND|wx.ALL, 0)
        topsizer_K.Add(topsizer_K_left, 60, wx.EXPAND|wx.ALL, 1)
        topsizer_K.Add(topsizer_K_right, 40, wx.EXPAND|wx.ALL, 1)

        self.panel1.win.SetSizer(topsizer_K)
        self._mgr.AddPane(self.panel1.win, wx.aui.AuiPaneInfo().Name("Canvas").Caption("Canvas").MaximizeButton().BestSize(wx.Size(CANVAS_SIZE[0], CANVAS_SIZE[1])).MinSize(wx.Size(CANVAS_SIZE[0], CANVAS_SIZE[1])).CenterPane())

        self.panel2 = wx.Panel(nb, -1, style=wx.CLIP_CHILDREN)  # Панель для настройки параметров
        nb.AddPage(self.panel2, 'О')
        #topsizer_O = wx.BoxSizer( wx.VERTICAL );
        #self.panel2.win = wx.Window(self.panel2, -1,
        #                            #size = wx.DefaultSize,
        #                            size = self.GetSize(),
        #                            style = wx.SIMPLE_BORDER)    # size = wx.DefaultSize,
        #topsizer_O.Add(self.panel2.win,
        #             1,             # make vertically stretchable
        #             wx.EXPAND |    # make horizontally stretchable
        #             wx.ALL,        # and make border all around
        #             2 )            # set border width to 2
        #self.panel2.SetSizer( topsizer_O )    # use the sizer for layout
        self.createOptionsPane()

        self.panel3 = wx.Panel(nb, -1, style=wx.CLIP_CHILDREN)  # Для сообщений протокола
        nb.AddPage(self.panel3, 'С')
        topsizer_M = wx.BoxSizer( wx.VERTICAL)
        self.msgWin = wx.TextCtrl(self.panel3, -1, size=wx.DefaultSize,
                                  style=wx.TE_MULTILINE|#wx.TE_READONLY|
                                  wx.HSCROLL|wx.TE_RICH2|wx.TE_WORDWRAP )
        topsizer_M.Add(self.msgWin,
                     1,             # make vertically stretchable
                     wx.EXPAND |    # make horizontally stretchable
                     wx.ALL,        # and make border all around
                     2 )            # set border width to 2
        self.panel3.SetSizer(topsizer_M)    # use the sizer for layout
        self.msgWin.AppendText("Сегодня: " +
                  time.strftime("%d.%m.%Y %H:%M", time.localtime(time.time())) + "\n")

        self.panel4 = wx.Panel(nb, -1, style=wx.CLIP_CHILDREN)  # Для интерпретаатора питона
        nb.AddPage(self.panel4, 'П')
        topsizer_P = wx.BoxSizer(wx.VERTICAL)
        intronote = "Interactive Python Shell for pythonOCC."
        py = wx.py.shell.Shell(self.panel4, - 1, introText=intronote, size=(800,700))
        py.interp.locals["self"] = self             # Для доступа из интерпретатора
        py.interp.locals["canvas"] = self.canva     # Для доступа из интерпретатора
        py.interp.locals["canvas_top"] = self.canva_top     # Для доступа из интерпретатора
        py.interp.locals["canvas_front"] = self.canva_front     # Для доступа из интерпретатора
        self.pyshell = py
        topsizer_P.Add(py, flag=wx.EXPAND)
        self.panel4.SetSizer(topsizer_P)    # use the sizer for layout

        self.tb1 = self.CreateRightToolbar()
        self.tb2 = self.CreateGgisToolbar()
        self._mgr.AddPane(self.tb1, wx.aui.AuiPaneInfo().Name("View").Caption("View").ToolbarPane().Top().TopDockable(True).BottomDockable(True))
        self._mgr.AddPane(self.tb2, wx.aui.AuiPaneInfo().Name("GGIS").Caption("GGIS").ToolbarPane().Top().TopDockable(True).BottomDockable(True))
        #Кнопочное меню / ButtonMenu
        self.buttonMenu=[
                #['',wx.NewId(),u'Главное меню',self.NavigateMenu,None,'main'],
                ['add',wx.NewId(),u'Главное меню',self.NavigateMenu,None,'main'],
                ['add',wx.NewId(),u'---',None,None,'main'],
                ['edge',wx.NewId(),u'Главное меню',self.NavigateMenu,None,'main'],
                ['edge',wx.NewId(),u'---',None,None,'main'],
                ['body',wx.NewId(),u'Главное меню',self.NavigateMenu,None,'main'],
                ['body',wx.NewId(),u'---',None,None,'main'],
                ['isoline',wx.NewId(),u'Главное меню',self.NavigateMenu,None,'main'],
                ['isoline',wx.NewId(),u'---',None,None,'main'],
                ['drill',wx.NewId(),u'Главное меню',self.NavigateMenu,None,'main'],
                ['drill',wx.NewId(),u'---',None,None,'main'],
                ['ways',wx.NewId(),u'Главное меню',self.NavigateMenu,None,'main'],
                ['ways',wx.NewId(),u'---',None,None,'main'],
                ['edit',wx.NewId(),u'Главное меню',self.NavigateMenu,None,'main'],
                ['edit',wx.NewId(),u'---',None,None,'main'],
                ['cut',wx.NewId(),u'Главное меню',self.NavigateMenu,None,'main'],
                ['cut',wx.NewId(),u'---',None,None,'main'],
                ['main',wx.NewId(),u'Задание',self.NavigateMenu,None,'add'],
                        ['add',wx.NewId(),u'Бровка',self.NavigateMenu,None,'edge'],
                                ['edge',wx.NewId(),u'Начать',self.OnEdgePLine,None,'start_edge'],
                                        ['start_edge',wx.NewId(),u'ОтменитьПосл',self.OnEdgeUndo,None,'edge'],
                                        ['start_edge',wx.NewId(),u'Закончить',self.OnEdgeEnd,None,'edge'],
                                        ['start_edge',wx.NewId(),u'Замкнуть',self.OnEdgeClose,None,'edge'],
                                        ['start_edge',wx.NewId(),u'Отмена',self.OnEdgeCancel,None,'edge'],
                                #['edge',wx.NewId(),u'Продолжить',self.OnEdgeContinue,None,'continue_edge'],
                                #        ['continue_edge',wx.NewId(),u'ОтменитьПосл',self.NavigateMenu,None],
                                #        ['continue_edge',wx.NewId(),u'Закончить',self.OnEdgeEnd,None,'edge'],
                                #        ['continue_edge',wx.NewId(),u'Замкнуть',self.OnEdgeClose,None,'edge'],
                                #        ['continue_edge',wx.NewId(),u'Отмена',self.OnEdgeCancel,None,'edge'],
                                ['edge',wx.NewId(),u'---'],
                                ['edge',wx.NewId(),u'ПостПлощ',self.OnEdgeOffset,None],
                                ['edge',wx.NewId(),u'---'],
                                ['edge',wx.NewId(),u'ОбъеденитьБровки',self.OnEdBrMerge,None,'edge_OnEdBrMerge'],
                                    ['edge_OnEdBrMerge',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'edge'],
                                ['edge',wx.NewId(),u'УдалитьБровку',self.OnEdBrDelB,None,'edge_OnEdBrDelB'],
                                    ['edge_OnEdBrDelB',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'edge'],
                                ['edge',wx.NewId(),u'РазбитьБровку',self.OnEdBrBrkV,None,'edge_OnEdBrBrkV'],
                                    ['edge_OnEdBrBrkV',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'edge'],
                                ['edge',wx.NewId(),u'ВставитьТочку',self.OnEdBrInsV,None,'edge_OnEdBrInsV'],
                                    ['edge_OnEdBrInsV',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'edge'],
                                ['edge',wx.NewId(),u'УдалитьТочку',self.OnEdBrDelV,None,'edge_OnEdBrDelV'],
                                    ['edge_OnEdBrDelV',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'edge'],
                                ['edge',wx.NewId(),u'ПеремесТочку',self.OnEdBrMoveV,None,'edge_OnEdBrMoveV'],
                                    ['edge_OnEdBrMoveV',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'edge'],

                        ['add',wx.NewId(),u'Тело',self.NavigateMenu,None,'body'],
                                ['body',wx.NewId(),u'Начать',self.OnEdgePLine,None,'start_body'],
                                        ['start_body',wx.NewId(),u'ОтменитьПосл',self.OnEdgeUndo,None,'body'],
                                        ['start_body',wx.NewId(),u'Закончить',self.OnEdgeClose,None,'body'],
                                        ['start_body',wx.NewId(),u'Отмена',self.OnEdgeCancel,None,'body'],
                                ['body',wx.NewId(),u'---'],
                                ['body',wx.NewId(),u'УдалитьТело',self.OnEdBrDelB,None,'body_OnEdBrDelB'],
                                    ['body_OnEdBrDelB',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'body'],

                        ['add',wx.NewId(),u'Рельеф',self.NavigateMenu,None,'isoline'],
                                ['isoline',wx.NewId(),u'Начать',self.OnEdgePLine,None,'start_isoline'],
                                        ['start_isoline',wx.NewId(),u'ОтменитьПосл',self.OnEdgeUndo,None,'isoline'],
                                        ['start_isoline',wx.NewId(),u'Закончить',self.OnEdgeClose,None,'isoline'],
                                        ['start_isoline',wx.NewId(),u'Отмена',self.OnEdgeCancel,None,'isoline'],
                                ['isoline',wx.NewId(),u'---'],
                                ['isoline',wx.NewId(),u'УдалитьИзолинию',self.OnEdBrDelB,None,'isoline_OnEdBrDelB'],
                                    ['isoline_OnEdBrDelB',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'isoline'],
                                ['isoline',wx.NewId(),u'ВставитьТочку',self.OnEdBrInsV,None,'isoline_OnEdBrInsV'],
                                    ['isoline_OnEdBrInsV',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'isoline'],
                                ['isoline',wx.NewId(),u'УдалитьТочку',self.OnEdBrDelV,None,'isoline_OnEdBrDelV'],
                                    ['isoline_OnEdBrDelV',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'isoline'],
                                ['isoline',wx.NewId(),u'ПеремесТочку',self.OnEdBrMoveV,None,''],
                                    ['isoline_OnEdBrMoveV',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'isoline'],

                        ['add',wx.NewId(),u'Скважина',self.NavigateMenu,None,'drill'],
                                ['drill',wx.NewId(),u'Задать',self.OnDrillStart,None,'start_drill'],
                                        ['start_drill',wx.NewId(),u'Создать',self.OnDrillAdd,None,'drill'],
                                        ['start_drill',wx.NewId(),u'Отмена',self.OnEdgeCancel,None,'drill'],
                                ['drill',wx.NewId(),u'УдалитьСкважину',self.OnEdBrDelB,None,'drill_OnEdBrDelB'],
                                    ['drill_OnEdBrDelB',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'drill'],
                                ['drill',wx.NewId(),u'ПереместитьСкважину',self.OnEdBrMoveP,None,'drill_OnEdBrMoveP'],
                                    ['drill_OnEdBrMoveP',wx.NewId(),u'Применить',self.OnDrillMoveOk,None,'drill'],
                                    ['drill_OnEdBrMoveP',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'drill'],

                        ['add',wx.NewId(),u'Съезды',self.NavigateMenu,None,'ways'],
                                ['ways',wx.NewId(),u'ОпрПолилинию',self.OnEdgePLine,None,'start_way_pline'],
                                    ['start_way_pline',wx.NewId(),u'ОтменитьПосл',self.OnEdgeUndo,None,'ways'],
                                    ['start_way_pline',wx.NewId(),u'Закончить',self.OnWayPLineYes,None,'ways'],
                                    ['start_way_pline',wx.NewId(),u'Отмена',self.OnEdgeCancel,None,'ways'],

                ['main',wx.NewId(),u'Корректировка',self.NavigateMenu,None,'edit'],
                        ['edit',wx.NewId(),u'Еденичная прирезка',self.NavigateMenu,None,'cut'],
                            ['cut',wx.NewId(),u'УстНачало',self.OnEdBrSelB,None,'cut_OnEdBrSelB'],
                                 ['cut_OnEdBrSelB',wx.NewId(),u'Назад',self.OnEdCmdCancel,None,'cut'],
                            ['cut',wx.NewId(),u'ОпрПолилинию',self.OnCutPLine,None,'start_cut_pline'],
                                ['start_cut_pline',wx.NewId(),u'ОтменитьПосл',self.OnEdgeUndo,None,'cut'],
                                ['start_cut_pline',wx.NewId(),u'Закончить',self.OnCutPLineEnd,None,'make_cut_query'],
                                    ['make_cut_query',wx.NewId(),u'Применить',self.OnCutPLineYes,None,'cut'],
                                    ['make_cut_query',wx.NewId(),u'Отмена',self.OnEdgeCancel,None,'cut'],
                                ['start_cut_pline',wx.NewId(),u'Отмена',self.OnEdgeCancel,None,'cut'],
                            ['cut',wx.NewId(),u'Отмена',self.NavigateMenu,None,'edit'],

                        ['edit',wx.NewId(),u'Поуровневая прирезка',self.OnCutNavigateMenu,None,'cut_levels'],
                            ['cut_levels',wx.NewId(),u'ОпрПолилинию1',self.OnCutPLine1,None,'start_cut_levels_pline'],
                            ['cut_levels',wx.NewId(),u'ОпрПолилинию2',self.OnCutPLine2,None,'start_cut_levels_pline'],
                            ['cut_levels',wx.NewId(),u'ОпрПолилинию3',self.OnCutPLine3,None,'start_cut_levels_pline'],
                                ['start_cut_levels_pline',wx.NewId(),u'ОтменитьПосл',self.OnEdgeUndo,None,'cut_levels'],
                                ['start_cut_levels_pline',wx.NewId(),u'Закончить',self.OnCutPLineYes,None,'cut_levels'],
                                ['start_cut_levels_pline',wx.NewId(),u'Отмена',self.OnEdgeCancel,None,'cut_levels'],
                            ['cut_levels',wx.NewId(),u'Построить',self.OnCutPLineYesMany,None,'edit'],
                            ['cut_levels',wx.NewId(),u'Отмена',self.OnEdgeCancel,None,'edit'],

                        ['edit',wx.NewId(),u'РедактТчк',self.OnCEdit,None,'cedit'],
                ['',wx.NewId(),u'---',None,None,'main'],
                ['',wx.NewId(),u'Debug',self.OnDebug,None],
                ['',wx.NewId(),u'Длинна',self.OnLenth,None],
                ['',wx.NewId(),u'Обратить',self.OnInvert,None],
                ['',wx.NewId(),u'Обновить',self.OnRefresh,None],
                ['',wx.NewId(),u'Очистить',self.OnErase,None],
                ['',wx.NewId(),u'СохранитьБД',self.OnSaveDB,None],
                ['',wx.NewId(),u'Добавить текст',self.OnAddText,None],
                ['',wx.NewId(),u'Сетка',self.OnShowGrid,None],
                ]

        self.menu_now = 'main'
        self.tb3 = self.CreateMenu()
        self.NavigateMenu()
        self._mgr.AddPane(self.tb3, wx.aui.AuiPaneInfo().Name("Builder").Caption("Построитель карьеров").ToolbarPane().Left().LeftDockable())

        self._mgr.Update()
        #self._mgr.GetPane("Help").MinSize((-1,-1)) # now make it so that the help pane can be resized

        self.DefaultPerspective = self._mgr.SavePerspective()
        # Load Layout
        tmp = LoadLayout(os.path.join(THISPATH, "layout"))
        if tmp:
            maximised, position, size, perspective = tmp
            self.LoadedPerspective = perspective
            self._mgr.LoadPerspective(self.LoadedPerspective)
            self._mgr.Update()
            self.SetSize(size)
            self.SetPosition(position)
            if maximised:
                self.Maximize()
        self.statusbar = self.CreateStatusBar(3, wx.ST_SIZEGRIP)
        # Creating Menu
        menuBar = wx.MenuBar()
        FileMenu = wx.Menu()

        '''file_id = wx.NewId()
        FileMenu.Append(file_id, MNU_OPEN[0], MNU_OPEN[1])
        self.Bind(wx.EVT_MENU, self.OnOpen, id=file_id)'''

        load_id = wx.NewId()
        FileMenu.Append(load_id, MNU_CLOAD[0], MNU_CLOAD[1])
        self.Bind(wx.EVT_MENU, self.OnLoadDB, id=load_id)

        save_id = wx.NewId()
        FileMenu.Append(save_id, MNU_CSAVE[0], MNU_CSAVE[1])
        self.Bind(wx.EVT_MENU, self.OnSaveDB, id=save_id)

        FileMenu.AppendSeparator()
        saveasbmp_id = wx.NewId()
        FileMenu.Append(saveasbmp_id, MNU_SAVEAS[0], MNU_SAVEAS[1])
        self.Bind(wx.EVT_MENU, self.SaveAsImage, id=saveasbmp_id)
        FileMenu.AppendSeparator()

        execpy_id = wx.NewId()
        FileMenu.Append(execpy_id, MNU_SCRIPT[0], MNU_SCRIPT[1])
        self.Bind(wx.EVT_MENU, self.ExecPyFile, id=execpy_id)
        FileMenu.AppendSeparator()

        exit_id = wx.NewId()
        FileMenu.Append(exit_id, MNU_EXIT[0], MNU_EXIT[1])
        self.Bind(wx.EVT_MENU, self.OnExit, id=exit_id)

        self.filehistory = wx.FileHistory()
        self.filehistory.UseMenu(FileMenu)
        #print self._recentfiles
        if len(self._recentfiles) > 0:
            for f in reversed(self._recentfiles):
                self.filehistory.AddFileToHistory(f)
        self.Bind(wx.EVT_MENU_RANGE, self.OnClickRecentFile, id=wx.ID_FILE1, id2=wx.ID_FILE9)

        menuBar.Append(FileMenu, MNU_FILE)
        # View menu
        viewmenu = wx.Menu()
        restoreperspectiveID = wx.NewId()
        viewmenu.Append(restoreperspectiveID, u'Восстановить\tAlt+r', u'Восстановить стандартное положение панелей.')
        self.Bind(wx.EVT_MENU, self.OnRestoreDefaultPerspective, id=restoreperspectiveID)
        viewmenu.AppendSeparator()
        v_Top = wx.NewId()
        viewmenu.Append(v_Top, MNU_TOP[0], MNU_TOP[1])
        self.Bind(wx.EVT_MENU, lambda event: self.SetView(event, self.canva._3dDisplay.View_Top), id=v_Top)
        v_Bottom = wx.NewId()
        viewmenu.Append(v_Bottom, MNU_BOTTOM[0], MNU_BOTTOM[1])
        self.Bind(wx.EVT_MENU, lambda event: self.SetView(event, self.canva._3dDisplay.View_Bottom), id=v_Bottom)
        v_Left = wx.NewId()
        viewmenu.Append(v_Left, MNU_LEFT[0], MNU_LEFT[1])
        self.Bind(wx.EVT_MENU, lambda event: self.SetView(event, self.canva._3dDisplay.View_Left), id=v_Left)
        v_Right = wx.NewId()
        viewmenu.Append(v_Right, MNU_RIGHT[0], MNU_RIGHT[1])
        self.Bind(wx.EVT_MENU, lambda event: self.SetView(event, self.canva._3dDisplay.View_Right), id=v_Right)
        v_Front = wx.NewId()
        viewmenu.Append(v_Front, MNU_FRONT[0], MNU_FRONT[1])
        self.Bind(wx.EVT_MENU, lambda event: self.SetView(event, self.canva._3dDisplay.View_Front), id=v_Front)
        v_Rear = wx.NewId()
        viewmenu.Append(v_Rear, MNU_REAR[0], MNU_REAR[1])
        self.Bind(wx.EVT_MENU, lambda event: self.SetView(event, self.canva._3dDisplay.View_Rear), id=v_Rear)
        v_Iso = wx.NewId()
        viewmenu.Append(v_Iso, MNU_ISO[0], MNU_ISO[1])
        self.Bind(wx.EVT_MENU, lambda event: self.SetView(event, self.canva._3dDisplay.View_Iso), id=v_Iso)
        z = wx.NewId()
        viewmenu.Append(z, MNU_ZOOMALL[0], MNU_ZOOMALL[1])
        self.Bind(wx.EVT_MENU, self._zoomall, id=z)
        menuBar.Append(viewmenu, MNU_VIEW)

        # Selection menu
        '''selection_menu = wx.Menu()
        s_vertex = wx.NewId()
        selection_menu.Append(s_vertex, MNU_VERTEX[0], MNU_VERTEX[1])
        self.Bind(wx.EVT_MENU, self.OnSelectionVertex, id=s_vertex)
        s_edge = wx.NewId()
        selection_menu.Append(s_edge, MNU_EDGE[0], MNU_EDGE[1])
        self.Bind(wx.EVT_MENU, self.OnSelectionEdge, id=s_edge)
        s_face = wx.NewId()
        selection_menu.Append(s_face, MNU_FACE[0], MNU_FACE[1])
        self.Bind(wx.EVT_MENU, self.OnSelectionFace, id=s_face)
        s_neutral = wx.NewId()
        selection_menu.Append(s_neutral, MNU_NEUTRAL[0], MNU_NEUTRAL[1])
        self.Bind(wx.EVT_MENU, self.OnSelectionNeutral, id=s_neutral)
        menuBar.Append(selection_menu, MNU_SELECTION)'''

        # DisplayMode menu
        displaymode_menu = wx.Menu()
        d_wireframe = wx.NewId()
        '''displaymode_menu.Append(d_wireframe, MNU_WARE[0], MNU_WARE[1])
        self.Bind(wx.EVT_MENU, self.OnDisplayModeWireframe, id=d_wireframe)
        d_shaded = wx.NewId()
        displaymode_menu.Append(d_shaded, MNU_SHADED[0], MNU_SHADED[1])
        self.Bind(wx.EVT_MENU, self.OnDisplayModeShaded, id=d_shaded)
        displaymode_menu.AppendSeparator()
        d_qhlr = wx.NewId()
        displaymode_menu.Append(d_qhlr, MNU_QHLR[0], MNU_QHLR[1])
        self.Bind(wx.EVT_MENU, self.OnDisplayModeQHLR, id=d_qhlr)
        d_ehlr = wx.NewId()
        displaymode_menu.Append(d_ehlr, MNU_EXHLR[0], MNU_EXHLR[1])
        self.Bind(wx.EVT_MENU, self.OnDisplayModeEHLR, id=d_ehlr)
        displaymode_menu.AppendSeparator()'''
        d_aon = wx.NewId()
        displaymode_menu.Append(d_aon, MNU_AALIASon[0], MNU_AALIASon[1])
        self.Bind(wx.EVT_MENU, self.OnAntialiasingOn, id=d_aon)
        d_aoff = wx.NewId()
        displaymode_menu.Append(d_aoff, MNU_AALIASof[0], MNU_AALIASof[1])
        self.Bind(wx.EVT_MENU, self.OnAntialiasingOff, id=d_aoff)
        menuBar.Append(displaymode_menu, MNU_DISMODE)

        #=========================================================
        # Меню для демонстрации создания примитивов  === add cyx
        construct_menu = wx.Menu()
        c_axis = wx.NewId()
        construct_menu.Append(c_axis, MNU_CRAXIS[0], MNU_CRAXIS[1])
        self.Bind(wx.EVT_MENU, self.OnCAxis, id=c_axis)

        c_topograph = wx.NewId()
        construct_menu.Append(c_topograph, MNU_CRDEMODB[0], MNU_CRDEMODB[1])
        self.Bind(wx.EVT_MENU, self.OnCreateDB, id=c_topograph)

        c_pit = wx.NewId()
        construct_menu.Append(c_pit, MNU_CRPIT[0], MNU_CRPIT[1])
        self.Bind(wx.EVT_MENU, self.OnDemoPit, id=c_pit)

        c_lidar = wx.NewId()
        construct_menu.Append(c_lidar, MNU_LIDAR[0], MNU_LIDAR[1])
        self.Bind(wx.EVT_MENU, self.OnLidar, id=c_lidar)

        c_etalon = wx.NewId()
        construct_menu.Append(c_etalon, "Эталон", "Эталон")
        self.Bind(wx.EVT_MENU, self.OnEtalon, id=c_etalon)

        #c_explore = wx.NewId()
        #construct_menu.Append(c_explore, MNU_EXPLORE[0], MNU_EXPLORE[1])
        #self.Bind(wx.EVT_MENU, self.OnCExplore, id=c_explore)

        #c_erase = wx.NewId()
        #construct_menu.Append(c_erase, MNU_ERASE[0], MNU_ERASE[1])
        #self.Bind(wx.EVT_MENU, self.OnCErase, id=c_erase)

        menuBar.Append(construct_menu, MNU_CREATE)

        #=========================================================
        # Меню для редактирования элементов  === add cyx
        edit_menu = wx.Menu()

        e_explore = wx.NewId()
        edit_menu.Append(e_explore, MNU_EXPLORE[0], MNU_EXPLORE[1])
        self.Bind(wx.EVT_MENU, self.OnCExplore, id=e_explore)

        e_edit = wx.NewId()
        edit_menu.Append(e_edit, 'Редактировать елемент', 'Вызвать окно редактора координат')
        self.Bind(wx.EVT_MENU, self.OnCEdit, id=e_edit)

        e_EdBrInsV = wx.NewId()
        edit_menu.Append(e_EdBrInsV, MNU_EdBrInsV[0], MNU_EdBrInsV[1])
        self.Bind(wx.EVT_MENU, self.OnEdBrInsV, id=e_EdBrInsV)

        e_EdBrMoveV = wx.NewId()
        edit_menu.Append(e_EdBrMoveV, MNU_EdBrMoveV[0], MNU_EdBrMoveV[1])
        self.Bind(wx.EVT_MENU, self.OnEdBrMoveV, id=e_EdBrMoveV)

        e_EdBrDelV = wx.NewId()
        edit_menu.Append(e_EdBrDelV, MNU_EdBrDelV[0], MNU_EdBrDelV[1])
        self.Bind(wx.EVT_MENU, self.OnEdBrDelV, id=e_EdBrDelV)

        e_EdBrBrkV = wx.NewId()
        edit_menu.Append(e_EdBrBrkV, MNU_EdBrBrkV[0], MNU_EdBrBrkV[1])
        self.Bind(wx.EVT_MENU, self.OnEdBrBrkV, id=e_EdBrBrkV)

        e_EdBrDelB = wx.NewId()
        edit_menu.Append(e_EdBrDelB, MNU_EdBrDelB[0], MNU_EdBrDelB[1])
        self.Bind(wx.EVT_MENU, self.OnEdBrDelB, id=e_EdBrDelB)


        menuBar.Append(edit_menu, MNU_EDIT)
        #==========================================================
        # About menu
        about_menu = wx.Menu()
        a_id = wx.NewId()
        about_menu.Append(a_id, MNU_ABOUT[0], MNU_ABOUT[1])
        self.Bind(wx.EVT_MENU, self.OnAbout, id=a_id)
        menuBar.Append(about_menu, MNU_HELP)

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self._refreshui()
        #==========================================================
        # Установки статусной строки
        self.SetStatusWidths([500, 200, -1])
        self.SetStatusText("Приглашение", 0)
        self.SetStatusText("Координаты курсора", 1)
        self.SetStatusText("Результат", 2)
        self.InitCanva(self.canva)
        self.InitCanva(self.canva_top)
        self.InitCanva(self.canva_front)

    def SetView(self, event, perspective_func):
        """Call self.canva._3dDisplay.View_*() and ZoomAll"""
        perspective_func()
        self.canva.ZoomAll()

    def InitCanva(self, canva):
        canva.frame = self
        canva.GumLine = False
        canva.MakeLine = False
        canva.MakePLine = False
        canva.MakePoint = False
        canva.startPt = False
        canva.drawList = []
        canva.tmpEdge = None

    def CreateMenu(self):
        return wx.ToolBar(self.panel1, - 1, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_VERTICAL )

    def NavigateMenu(self, event=None, menuname='main'):
        if event is not None:
            if not isinstance(event.EventObject, wx.Button):
                return
            for i, v in enumerate(self.buttonMenu):
                if v[1] == event.EventObject.GetId() and (v[0] == self.menu_now or v[0] == ''):
                    menuname = v[5]
                    self.menu_now = menuname
                    break
        else:
            self.menu_now = menuname
        self.tb3.ClearTools()
        self.tb3.AddControl(wx.StaticText(self.tb3, wx.NewId(), menu_titles[menuname], wx.DefaultPosition, wx.DefaultSize, 0))
        self.tb3.AddSeparator()
        for i,v in enumerate(self.buttonMenu):
            if v[0] == menuname or v[0] == '':
                if v[2] == u'---':
                    self.tb3.AddSeparator()
                else:
                    self.buttonMenu[i][4] = wx.Button(self.tb3, v[1], v[2],size=(150,30))
                    self.tb3.AddControl(self.buttonMenu[i][4])
                    self.Bind(wx.EVT_BUTTON, self.buttonMenu[i][3], self.buttonMenu[i][4])
        self.tb3.Fit()

    def OnGridSlider(self, event, slider):
        RemoveGrid(self)
        DrawGrid(self, 9, 400, self.canva.usedHorizons[slider.GetValue()])

    def GridSlider(self, event):
        if self.canva.Grid_DoOnce:
            GridMenuTitle = wx.StaticText(self.panel1, -1, menu_titles['grid_title'], (20, 460), wx.DefaultSize, name="GridTitle")
            GridMenuEdges = wx.StaticText(self.panel1, -1, menu_titles['edge'], (40, 495), wx.DefaultSize, name="GridEdges")
            GridSlider = wx.Slider(self.panel1, -1, 0, 0, len(self.canva.usedHorizons)-1, (5, 480), (30, 100), wx.VERTICAL, name="GridSlider")
            self.Bind(wx.EVT_SLIDER, lambda evn: self.OnGridSlider(evn, GridSlider))
        else:
            for child in self.panel1.GetChildren():
                if child.GetName().startswith("Grid"):
                    child.Destroy()


    def getTypeByMenu(self):
        for i, v in enumerate(menu_types):
            if self.menu_now in menu_types[i]:
                return i
        return -1

    def OnEdCmdCancel(self,event):
        CancelOp(self)
        self.NavigateMenu(event)

    def OnDrillStart(self,event):
        Point(self)
        self.NavigateMenu(event)

    def OnDrillAdd(self,event):
        Coord_yes(self,True)
        self.NavigateMenu(event)

    def OnEdgePLine(self,event):
        self.OnPLine(event)
        self.NavigateMenu(event)

    def OnEdgeCancel(self,event):
        self.OnCancel(event)
        self.NavigateMenu(event)

    def OnEdgeEnd(self, event):
        Coord_yes(self, True)
        self.NavigateMenu(event)

    def OnEdgeClose(self, event):
        Coord_yes(self, True, True)
        self.NavigateMenu(event)

    def OnWayPLineYes(self, event):
        s1 = self.canva.tmpEdge.GetObject().Shape()

        pnts = getPoints(s1)
        plgn = BRepBuilderAPI_MakePolygon()
        hall = 0
        plgn.Add(gp_Pnt(pnts[0][0], pnts[0][1], pnts[0][2]))
        for i in xrange(1, len(pnts)):
            l = distance3d(pnts[-1], pnts[i])
            h = l*math.sin(math.radians(float(self.wayAngle.Value)))
            hall += h
            plgn.Add(gp_Pnt(pnts[i][0], pnts[i][1], pnts[i][2]-hall))
        #plgn.Add(gp_Pnt(pnts[-1][0], pnts[-1][1], pnts[-1][2]-h))
        s1 = plgn.Wire()

        w1 = make_offset(s1,int(self.wayWidth.GetValue())/2,round=False,close=False)
        pnts = getPoints(w1)
        self.OnPLine(event)
        self.canva.lstPnt=pnts
        Coord_yes(self,True)

        w2 = make_offset(s1, int(self.wayWidth.GetValue())/-2, round=False, close=False)
        pnts = getPoints(w2)
        self.OnPLine(event)
        self.canva.lstPnt=pnts
        Coord_yes(self,True)

        self.OnCancel(event)

        self.NavigateMenu(event)

    def OnWayCreate(self, event):
        pnts = getPoints(self.canva.drawList[self.canva.tempIndex][2].Shape())
        print pnts
        print self.canva.tempPointIndex
        width = int(self.wayWidth.Value)
        l = int(self.wayLen.Value)
        angle = int(self.wayAngle.Value)


        newPnts = []
        for i in range(self.canva.tempPointIndex,len(pnts)):
            newPnts.append(pnts[i])
        for i in range(self.canva.tempPointIndex):
            newPnts.append(pnts[i])


        plgn = BRepBuilderAPI_MakePolygon()

        i = 0
        while l > 0:
            try:
                pnt1 = newPnts[i]
                i += 1
                d = distance2d(pnt1,newPnts[i])
                l -= d
                print d
                plgn.Add(gp_Pnt(pnt1[0], pnt1[1], pnt1[2]*0+10))
            except IndexError:
                break

        self.canva._3dDisplay.DisplayColoredShape(plgn.Wire(), OCC.Quantity.Quantity_Color(0.5,0.7,0.5,0), False)

        pass

    def OnDrillMoveOk(self, event):
        x = self.canva.worldPt[0]
        y = self.canva.worldPt[1]
        z = self.canva.worldPt[2]

        dept=self.canva.drawList[self.canva.tempIndex][9]

        skv = BRepPrim_Cylinder(gp_Pnt(x,y,z-dept), 0.1, dept)
        skv = skv.Shell()
        s1 = self.canva._3dDisplay.DisplayColoredShape(skv, 'YELLOW', False)

        self.canva.Erase(self.canva.drawList[self.canva.tempIndex][2].GetHandle())

        oldInfo = self.canva.drawList[self.canva.tempIndex]
        #print oldInfo
        oldInfo[2] = s1.GetObject()
        oldInfo[6] = x
        oldInfo[7] = y
        oldInfo[8] = z
        oldInfo[-1] = True
        #print oldInfo
        self.canva.drawList[self.canva.tempIndex] = oldInfo

        self.OnCancel(event)
        self.NavigateMenu(event)

    def OnEdgeOffset(self, event):
        s1 = self.canva._3dDisplay.selected_shape
        if not s1:
            return
        w = make_offset(s1,int(self.ploshWidth.GetValue()))
        pnts = getPoints(w)
        self.OnPLine(event)
        self.canva.lstPnt=pnts
        Coord_yes(self,True)
        #s1=self.canva._3dDisplay.DisplayColoredShape(s1, OCC.Quantity.Quantity_Color(0.9,0.9,0.5,0), False)
        """x=100
        for i in range(10):
            w=make_offset(s1,x,x)
            s1=self.canva._3dDisplay.DisplayColoredShape(w, OCC.Quantity.Quantity_Color(0.9,0.5,0.5,0), False).GetObject().Shape()
            w=make_offset(s1,x*2,0)
            s1=self.canva._3dDisplay.DisplayColoredShape(w, OCC.Quantity.Quantity_Color(0.5,0.5,0.9,0), False).GetObject().Shape()"""

    def OnEdgeContinue(self, event):
        sel_shape = self.canva._3dDisplay.selected_shape
        if sel_shape:
            object_type=self.getTypeByMenu()
            indexInfo = None;
            for i in range(len(self.canva.drawList)):
                s1 = self.canva.drawList[i][2]
                if s1:
                    if (s1.Shape().IsEqual(sel_shape) and self.canva.drawList[i][0] == object_type):
                        indexInfo = i
                        break
            if indexInfo is None:
                return

            selObj = self.canva._3dDisplay.Context.SelectedInteractive()
            self.canva.Erase(selObj)
            pnts = getPoints(sel_shape)
            self.canva.lstPnt=pnts
            self.OnPLine(event)
            self.NavigateMenu(event)

    def OnEdgeUndo(self, event):
        if len(self.canva.lstPnt) > 2:
            self.canva.coord.SetValue(str(self.canva.lstPnt[-2][0])+','+str(self.canva.lstPnt[-2][1])+','+str(self.canva.lstPnt[-2][2]))
            self.canva.lstPnt = self.canva.lstPnt[:-2]
            Coord_yes(self)
        elif len(self.canva.lstPnt) == 2:
            self.canva.coord.SetValue(str(self.canva.lstPnt[0][0])+','+str(self.canva.lstPnt[0][1])+','+str(self.canva.lstPnt[0][2]))
            self.canva.lstPnt = []
            Coord_yes(self)
            if self.canva.tmpEdge:
                self.canva.Erase(self.canva.tmpEdge)
                self.canva.tmpEdge = None
        else:
            self.OnEdgeCancel(event)

    def OnErase(self, event):
        """
        Erase query
        """
        needSave = False
        for element in self.canva.drawList:
            needSave = needSave or element[-1]
        if needSave:
            dlg = wx.MessageDialog(self, u"Сохранить изменения перед очисткой?", u'Были изменены элементы карьера', wx.YES | wx.NO | wx.CANCEL | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_YES:
                SaveDB(self)
            elif result == wx.ID_CANCEL:
                return
        self.canva.EraseAll()
        self.canva.drawList = []

    def OnCutNavigateMenu(self, event):
        self.CutPlines=[[],[],[]]
        self.NavigateMenu(event)

    def OnCutPLine1(self, event):
        self.OnCutPLine(event,0)
        pass
    def OnCutPLine2(self, event):
        self.OnCutPLine(event,1)
        pass
    def OnCutPLine3(self, event):
        self.OnCutPLine(event,2)
        pass

    def OnCutPLine(self, event, num=None):
        self.canva.snap.SetSelection(0)
        self.cutPlineId=num
        self.OnPLine(event)
        if self.canva.tempPoint:
            resPnt=self.canva.tempPoint
            self.canva.coord.SetValue("%.1f,%.1f"%(resPnt[0],resPnt[1]))
            self.canva.coordZ.SetValue("%.1f"%(resPnt[2]))
            Coord_yes(self)
        self.NavigateMenu(event)

    def OnCutPLineYesMany(self, event):
        self.OnCutPLineYes(event,True)

    def OnCutPLineYes(self,event, force=False):
        """
        PLine(self)
        self.canva.lstPnt=pnts
        Coord_yes(self,True)
        self.canva.Erase(self.canva.drawList[self.canva.tempIndex][2].GetHandle())
        self.canva.drawList[self.canva.tempIndex][2]=None
        self.canva.drawList[self.canva.tempIndex][-1]=True
        self.OnCancel(event)
        """
        if self.cutPlineId==None:
            pnts=getPoints(self.canva.tmpEdge.GetObject().Shape())
            self.canva.Erase(self.canva.drawList[self.canva.tempIndex][2].GetHandle())
            self.canva.Erase(self.canva.tmpEdge)
            for i,v in enumerate(self.egde_typeList):
                if v[0]==self.canva.drawList[self.canva.tempIndex][4]:
                    edge_type=self.egde_typeList[i]
                    break
            plgn = BRepBuilderAPI_MakePolygon()
            for pnt1 in pnts:
                plgn.Add(gp_Pnt(pnt1[0], pnt1[1], pnt1[2]))
            w = plgn.Wire()
            for i in range(len(self.colorList)):
                if self.colorList[i][0]==edge_type[3]:
                    r=int(str(self.colorList[i][2]))/255.0
                    g=int(str(self.colorList[i][3]))/255.0
                    b=int(str(self.colorList[i][4]))/255.0
                    s1=self.canva._3dDisplay.DisplayColoredShape(w, OCC.Quantity.Quantity_Color(r,g,b,0), False)
                    break
            self.canva.drawList[self.canva.tempIndex][2]=s1.GetObject()
            self.canva.drawList[self.canva.tempIndex][-1]=True
        elif force:
            plgn = BRepBuilderAPI_MakePolygon()
            for pnt1 in self.CutPlines[0]:
                plgn.Add(gp_Pnt(pnt1[0], pnt1[1], pnt1[2]))
            w = plgn.Wire()
            for i in range(min(len(self.CutPlines[1]),len(self.CutPlines[2]))):
                d=min(distance2d(self.CutPlines[0][0],self.CutPlines[1][i]),distance2d(self.CutPlines[0][0],self.CutPlines[2][i]))
                wt=make_offset(w,d,round=True,close=False)
                pnts=getPoints(wt)[2:-2]
                pnts[0]=self.CutPlines[1][i]
                pnts[-1]=self.CutPlines[2][i]
                self.OnPLine(event)
                self.canva.lstPnt=pnts
                Coord_yes(self,drawP=True)
                self.OnCancel(event)
        else:
            self.CutPlines[self.cutPlineId]=getPoints(self.canva.tmpEdge.GetObject().Shape())
        self.NavigateMenu(event)
        self.OnCancel(event)
        pass

    def OnCutPLineEnd(self,event):
        """ Конец рисования полилинии прирезки """
        self.canva.SetTogglesToFalse(event)
        self.canva.snap.SetSelection(2)
        if (self.canva.snap.GetCurrentSelection() == 2):
            self.NavigateMenu(event)
            self.canva.MakePLine=False
            self.canva.EdCmd = CMD_EdBrCutE
            self.canva.EdStep = 1
            self.SetStatusText("Куда?", 0)
        else:
            self.SetStatusText("*** Нет Near ***", 0)
        pass

    def CreateRightToolbar(self):
        # Начало формирования палитры
        tb = wx.ToolBar(self.panel1, - 1, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT | wx.TB_NODIVIDER)  #| wx.TB_VERTICAL )

        tb.SetToolBitmapSize((24, 24))
        zoom_all = CreateMaskedBitmap(os.path.join(THISPATH, 'icons', 'zoom_all.bmp'), 24, 24)
        zoom_win = CreatePng(os.path.join(THISPATH, 'icons', 'zoom-fit-best.png'), 24, 24)
        pointer = CreateMaskedBitmap(os.path.join(THISPATH, 'icons', 'pointer.bmp'), 24, 24)
        zoom = CreateMaskedBitmap(os.path.join(THISPATH, 'icons', 'zoom.bmp'), 24, 24)
        pan = CreateMaskedBitmap(os.path.join(THISPATH, 'icons', 'pan.bmp'), 24, 24)
        rotate = CreateMaskedBitmap(os.path.join(THISPATH, 'icons', 'rotate.bmp'), 24, 24)

        self.PointerID = wx.NewId()
        tb.AddCheckTool(id=self.PointerID, bitmap=pointer,
                       shortHelp="Pointer",
                       longHelp="Select.")
        self.Bind(wx.EVT_TOOL, self._pointer, id=self.PointerID)

        zoom_allID = wx.NewId()
        tb.AddTool(id=zoom_allID, bitmap=zoom_all,
                       shortHelpString="Zoom All",
                       longHelpString="Zoom out to show all of the visible geometry.")
        self.Bind(wx.EVT_TOOL, self._zoomall, id=zoom_allID)

        self.zoom_winID = wx.NewId()
        tb.AddTool(id=self.zoom_winID, bitmap=zoom_win,
                       shortHelpString="Zoom Window",
                       longHelpString="Zoom window.")
        self.Bind(wx.EVT_TOOL, self._zoomwin, id=self.zoom_winID)

        self.zoomID = wx.NewId()
        tb.AddCheckTool(id=self.zoomID, bitmap=zoom ,
                       shortHelp="Dynamic Zoom",
                       longHelp="Dynamically zoom in and out when the mouse moves.")
        self.Bind(wx.EVT_TOOL, self._dynamiczoom, id=self.zoomID)

        self.panID = wx.NewId()
        tb.AddCheckTool(id=self.panID, bitmap=pan,
                       shortHelp="Pan",
                       longHelp="Pan the view as when the mouse moves.")
        self.Bind(wx.EVT_TOOL, self._pan, id=self.panID)

        self.rotateID = wx.NewId()
        tb.AddCheckTool(id=self.rotateID, bitmap=rotate,
                       shortHelp="Rotate",
                       longHelp="Dynamically rotate the view when the mouse moves.")
        self.Bind(wx.EVT_TOOL, self._rotate, id=self.rotateID)
        # Конец формирования палитры
        tb.Realize()
        return tb

    def CreateGgisToolbar(self):
        # Начало формирования палитры кнопочного меню
        tb = wx.ToolBar(self.panel1, - 1, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT | wx.TB_NODIVIDER)
        tb.SetToolBitmapSize((24, 24))
        '''
        # Отмена
        img_cancel = CreatePng(os.path.join(THISPATH, 'icons', 'process-stop.png'), 16, 16)
        self.cancelID = wx.NewId()
        tb.AddLabelTool(self.cancelID, 'Stop', img_cancel, shortHelp='Отмена')
        self.Bind(wx.EVT_TOOL, self.OnCancel, id=self.cancelID)

        # Линия
        img_line = CreatePng(os.path.join(THISPATH, 'icons', 'segment.png'), 16, 16)
        self.lineID = wx.NewId()
        tb.AddLabelTool(self.lineID, 'Line', img_line, shortHelp='Отрезок')
        self.Bind(wx.EVT_TOOL, self.OnCLine, id=self.lineID)

        # Полилиния
        self.plineID = wx.NewId()
        img_pline = CreatePng(os.path.join(THISPATH, 'icons', 'linear.png'), 16, 16)
        tb.AddLabelTool(self.plineID, 'PLine', img_pline, shortHelp='Полилиния')
        self.Bind(wx.EVT_TOOL, self.OnPLine, id=self.plineID)

        # Coord input cyx
        tb.AddSeparator()'''
        # Ввод текста /broly
        tb.AddControl(wx.StaticText(tb, wx.NewId(), u'Текст: ', wx.DefaultPosition, wx.DefaultSize, 0))
        self.textxyz = wx.NewId()
        self.canva.text = wx.TextCtrl(tb, self.textxyz, "<координаты>", wx.DefaultPosition, (190, 40), 0)
        tb.AddControl(self.canva.text)

        # Ввод координат
        tb.AddControl(wx.StaticText(tb, wx.NewId(), u'Точка: ', wx.DefaultPosition, wx.DefaultSize, 0))
        self.coordXYZ = wx.NewId()
        self.canva.coord = wx.TextCtrl(tb, self.coordXYZ, "x,y[,z]", wx.DefaultPosition, (190, 30), 0)
        tb.AddControl(self.canva.coord)
        # Ввод уровня
        tb.AddControl(wx.StaticText(tb, wx.NewId(), 'Z', wx.DefaultPosition, wx.DefaultSize, 0))
        self.coordZ = wx.NewId()
        self.canva.coordZ = wx.TextCtrl(tb, self.coordZ, "0.00", wx.DefaultPosition, (90, 30), 0)
        tb.AddControl(self.canva.coordZ)
        # Принять координаты
        self.put_coordOk = wx.NewId()
        coord_bmp = CreateGif(os.path.join(THISPATH, 'icons', 'but_login.gif'), 16, 16)
        tb.AddLabelTool(self.put_coordOk, 'Coords', coord_bmp, shortHelp='Принять')
        self.Bind(wx.EVT_TOOL, self.onCoord_yes, id=self.put_coordOk)
        # Объектные привязки
        tb.AddSeparator()
        tb.AddControl(wx.StaticText(tb, wx.NewId(), u'Привязки: ', wx.DefaultPosition, wx.DefaultSize, 0))
        self.snapId = wx.NewId()
        self.canva.snap = wx.ComboBox(tb, self.snapId, u'Без привязки',
                                      wx.DefaultPosition, wx.DefaultSize,
                                      [u'Без привязки', u'Конец', u'Близкая', u'Центр', u'Тангенциальная'],
                                      wx.CB_SIMPLE)
        self.canva.snap.SetSelection(0)
        tb.AddControl(self.canva.snap)
        # Конец формирования палитры
        tb.Realize()
        return tb

    def createOptionsPane(self): #!_!
        # Создание окна параметров рисования
        # Оставляет атрибуты главного окна self
        #
        # self.horList  - список имен горизонтов            [гор, ...]
        # self.horIds   - список ключей в таблице horizons  [key, ...]
        # self.gorLst   - компонент с выбранными горизонтами
        # IsChecked(i)  - проверка выбора i-го горизонта в списке self.horList
        # self.gorCur   - комполнет выбора текущего горизонта
        # self.gorCur.GetCurrentSelection() - номер выбранного в self.horList
        #
        # self.objList = ["Бровки", "Тела", "Скважины", "Изолинии", "Отметки","Надписи", "БВР"]
        # self.chkObjs  - компонент с выбранными объектами, аналог self.gorLst
        # IsChecked(i)  - проверка выбора i-го объекта в списке self.objList
        #
        # self.stepXY   - компонент с выбранным шагом сетки
        # self.stepXY.GetValue() - выбранный размер сетки как целое от 0 до 100
        #
        # self.egde_typeList - список типов бровок в БД
        # [[id_edge_type,  name, line_type, color, thickness] , ... ]
        # self.edge_typeCur  - компонент с выбранным именем типа бровки
        # self.edge_typeCur.GetCurrentSelection() - номер выбранного в self.edge_typeList
        #
        # self.sortList - список сортов РТ  в формате
        #[[id_sort,  name, norm_weight, color, line_type, thickness, color_fill, description] , ... ]
        # self.sortCur  - компонент с выбранным именем сорта
        # self.sortCur.GetCurrentSelection() - номер выбранного в self.sortList
        #
        # self.coordList - список используемых систем координат из БД в формате
        # [[id_coord_system, id_srid, description] , ... ]
        # self.coordCur - компонент с выбранным именем системы координат
        # self.coordCur.GetCurrentSelection() - номер выбранного в self.coordList
        #
        # self.line_typeList - список используемых типов линий из БД в формате
        #[[id_type_line, name, description] , ... ]
        # self.line_typeCur - компонент с выбранным именем линии
        # self.line_typeCur.GetCurrentSelection() - номер выбранного в self.line_typeList
        #
        # self.colorList - список используемых цветов из БД в формате
        # # [[id_color, name_color, red, green, blue] , ... ]
        # self.colorCur  - компонент с выбранным именем цвета
        # self.colorCur.GetCurrentSelection() - номер выбранного в self.colorList
        #
        # self.lineWidth - компонент с выбранной толщиной линии
        # self.lineWidth.GetValue() - выбранная толщина линии от 0 до 10
        #
        # self.bodyH - Высота тела
        #
        # self.drillH - Глубина скважины
        #
        # self.drillName - Имя скважины
        #
        # self.ploshWidth - Ширина площадок
        #
        # self.wayWidth - Ширина съездов
        #
        # self.wayAngle - Угол съездов
        #
        # self.wayLen - Длинна съездов
        #

        panel = self.panel2     #.win
        dataBox = wx.BoxSizer(wx.HORIZONTAL)    # Общий sizer
        # Горизонты
        horBox = wx.BoxSizer(wx.VERTICAL)       # Колонка для горизонтов
        self.gorList = []
        hors = GetRowsTbl("horizons", "")
        self.horList = []
        self.horIds = []
        # [[id_hor, point, h_ledge, description], ...]
        for hor in hors:
            self.horIds = self.horIds + [hor]
            self.horList = self.horList + [str(hor[1])]
        horBox.Add(wx.StaticText(panel,-1,"Горизонты",
                                 size = (130,20)),
                    flag=wx.EXPAND)

        self.gorLst = wx.CheckListBox(panel, -1,
                                 #(10,30),
                                 size=(120, 300),
                                 choices=self.horList,
                                 style=wx.LB_MULTIPLE)
        horBox.Add(self.gorLst, flag=wx.EXPAND)

        horBox.Add((10, 40))
        horBox.Add(wx.StaticText(panel, -1, "Текущий горизонт",size=(180,20)),
                   flag=wx.EXPAND)

        self.gorCur = wx.ComboBox(panel, -1,
                                 self.horList[0],
                                 #(10,350),
                                 size=(150, 30),
                                 choices=self.horList,
                                 style=wx.CB_READONLY)
        self.gorCur.SetSelection(0)
        horBox.Add(self.gorCur,flag=wx.EXPAND)
        dataBox.Add(horBox, flag=wx.EXPAND)     # Включить в сайзер
        dataBox.Add((40,10))

        objBox = wx.BoxSizer(wx.VERTICAL)       # Колонка для объектов
        objBox.Add(wx.StaticText(panel,-1,"Объекты",size=(130,20)),
                   flag=wx.EXPAND)
        self.objList = ["Бровки", "Тела", "Скважины", "Изолинии", "Отметки","Надписи", "БВР"]
        self.chkObjs = wx.CheckListBox(panel, -1,
                                 #(10,10),
                                 size=(120, 300),
                                 choices=self.objList,
                                 style=wx.LB_MULTIPLE)
        objBox.Add(self.chkObjs, flag=wx.EXPAND)

        objBox.Add((10, 40))
        objBox.Add(wx.StaticText(panel,-1,"Шаг сетки",size=(130,20)),
                   flag=wx.EXPAND)
        self.stepXY = wx.SpinCtrl(panel, -1,
                                  value = "0",
                                  #poz=(10,10),
                                  size=(120, 30),
                                  style = wx.SP_ARROW_KEYS,
                                  min = 0, max = 100, initial = 0)

        objBox.Add(self.stepXY, flag=wx.EXPAND)
        objBox.Add((10, 40))

        btnRefresh = wx.Button(panel, -1,       # Кнопка Обновить
                               label = "Обновить",
                               #pos=(1,10),
                               size = (100,30))
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, btnRefresh)
        objBox.Add(btnRefresh, flag=wx.EXPAND)

        dataBox.Add(objBox, flag=wx.EXPAND)     # Включить в сайзер
        dataBox.Add((40,10))

        par1Box = wx.BoxSizer(wx.VERTICAL)       # Колонка для параметров 1
        par1Box.Add(wx.StaticText(panel, -1, "Тип бровки",size = (130, 20)),
                    flag=wx.EXPAND)
        #[[id_edge_type,  name, line_type, color, thickness] , ... ]
        edges_type = GetRowsTbl("edge_type", "")

        self.egde_typeList = []     # Глобальный список типов бровок
        typeLst = []                # Локальный для списка выбора
        for edge in edges_type:
            self.egde_typeList = self.egde_typeList + [list(edge)]
            typeLst = typeLst + [edge[1]]
        if (typeLst):
            value = typeLst[0]
        else:
            value = "Нет бровок в БД"
        self.edge_typeCur =  wx.ComboBox(panel, -1,
                                         value,
                                         size=(150, 30),
                                         choices=typeLst,
                                         style=wx.CB_READONLY)
        self.edge_typeCur.SetSelection(0)
        par1Box.Add(self.edge_typeCur, flag=wx.EXPAND, border = 1)
        par1Box.Add((10,40))
        par1Box.Add(wx.StaticText(panel,-1,"Сорт РТ",size = (130,20)),
                    flag=wx.EXPAND)
        #[[id_sort,  name, norm_weight, color, line_type, thickness, color_fill, description] , ... ]
        sorts_type = GetRowsTbl("sorts", "")

        self.sortList = []      # Глобальный список типов бровок
        sortLst = []            # Локальный для списка выбора
        for sort in sorts_type:
            self.sortList = self.sortList + [list(sort)]
            sortLst = sortLst + [sort[1]]
        if sortLst:
            value = sortLst[0]
        else:
            value = "Нет сортов в БД"
        self.sortCur = wx.ComboBox(panel, -1,
                                         value,
                                         size=(150, 30),
                                         choices=sortLst,
                                         style=wx.CB_READONLY)
        self.sortCur.SetSelection(0)
        par1Box.Add(self.sortCur, flag=wx.EXPAND, border = 1)

        par1Box.Add((10,40))
        par1Box.Add(wx.StaticText(panel,-1,"Высота тела",size = (180,20)),
                    flag=wx.EXPAND)
        self.bodyH = wx.TextCtrl(panel, -1, "5",size=(150,30))
        par1Box.Add(self.bodyH, flag=wx.EXPAND, border = 1)

        par1Box.Add((10, 40))
        par1Box.Add(wx.StaticText(panel,-1,"Система координат",size = (180,20)),
                    flag=wx.EXPAND)
        #[[id_coord_system, id_srid, description] , ... ]
        coord_systems = GetRowsTbl("coord_systems", "")

        self.coordList = []      # Глобальный список типов бровок
        coordLst = []            # Локальный для списка выбора
        for coord in coord_systems:
            self.coordList = self.coordList + [list(coord)]
            coordLst = coordLst + [coord[2]]
        if coordLst:
            value = coordLst[0]
        else:
            value = "Нет координатных систем"
        self.coordCur = wx.ComboBox(panel, -1,
                                         value,
                                         size=(150, 30),
                                         choices=coordLst,
                                         style=wx.CB_READONLY)
        self.coordCur.SetSelection(0)
        par1Box.Add(self.coordCur, flag=wx.EXPAND, border=1)

        par1Box.Add((10, 40))
        par1Box.Add(wx.StaticText(panel, -1, "Глубина сважины", size = (180, 20)),
                    flag=wx.EXPAND)
        self.drillH = wx.TextCtrl(panel, -1, "16",size=(150,30))
        par1Box.Add(self.drillH, flag=wx.EXPAND, border = 1)

        par1Box.Add((10,40))
        par1Box.Add(wx.StaticText(panel,-1,"Имя сважины",size = (180, 20)),
            flag=wx.EXPAND)
        self.drillName = wx.TextCtrl(panel, -1, "Скважина",size=(150, 30))
        par1Box.Add(self.drillName, flag=wx.EXPAND, border = 1)

        par1Box.Add((10,40))
        par1Box.Add(wx.StaticText(panel,-1,"Ширина площадок",size = (180, 20)),
        flag=wx.EXPAND)
        self.ploshWidth = wx.TextCtrl(panel, -1, "16",size=(150,30))
        par1Box.Add(self.ploshWidth, flag=wx.EXPAND, border = 1)

        dataBox.Add(par1Box,flag=wx.EXPAND)     # Включить в сайзер
        dataBox.Add((40,10))

        par2Box = wx.BoxSizer(wx.VERTICAL)       # Колонка для параметров 2
        par2Box.Add(wx.StaticText(panel,-1,"Тип линии",size=(130,20)),
                    flag=wx.EXPAND)
        lines_type = GetRowsTbl("line_type", "")
        #[[id_type_line, name, description] , ... ]
        self.line_typeList = []     # Глобальный список типов линий
        lineLst = []                # Локальный для списка выбора
        for line in lines_type:
            self.line_typeList = self.line_typeList + [list(line)]
            lineLst = lineLst + [line[1]]
        if lineLst:
            value = lineLst[0]
        else:
            value = "Нет типов линий в БД"
        self.line_typeCur = wx.ComboBox(panel, -1,
                                         value,
                                         size=(150, 30),
                                         choices=lineLst,
                                         style=wx.CB_READONLY)
        self.line_typeCur.SetSelection(0)
        par2Box.Add(self.line_typeCur, flag=wx.EXPAND, border=1)
        par2Box.Add((10, 40))
        par2Box.Add(wx.StaticText(panel,-1,"Цвет линии",size = (130, 20)),
                    flag=wx.EXPAND)

        colorS = GetRowsTbl("color", "")
        # [[id_color, name_color, red, green, blue] , ... ]
        self.colorList = []         # Глобальный список цветов
        colorLst = []               # Локальный для списка выбора
        for color in colorS:
            self.colorList = self.colorList + [list(color)]
            colorLst = colorLst + [color[1]]
        if colorLst:
            value = colorLst[0]
        else:
            value = "Нет цветов в БД"
        self.colorCur =  wx.ComboBox(panel, -1,
                                         value,
                                         size=(150, 30),
                                         choices=colorLst,
                                         style=wx.CB_READONLY)
        self.colorCur.SetSelection(0)
        par2Box.Add(self.colorCur, flag=wx.EXPAND, border = 1)
        par2Box.Add((10,40))
        par2Box.Add(wx.StaticText(panel,-1,"Толщина линии",size = (130,20)),
                    flag=wx.EXPAND)
        self.lineWidth = wx.SpinCtrl(panel, -1,
                                  value = "1",
                                  #poz=(10,10),
                                  size=(120, 30),
                                  style = wx.SP_ARROW_KEYS,
                                  min = 0, max = 10, initial = 1)

        par2Box.Add(self.lineWidth, flag=wx.EXPAND)

        par2Box.Add((10,40))
        par2Box.Add(wx.StaticText(panel,-1,"Ширина съезда",size = (180,20)),flag=wx.EXPAND)
        self.wayWidth = wx.TextCtrl(panel, -1, "16",size=(150,30))
        par2Box.Add(self.wayWidth, flag=wx.EXPAND, border = 1)

        '''par2Box.Add((10,40))
        par2Box.Add(wx.StaticText(panel,-1,"Длинна съезда",size = (180,20)),flag=wx.EXPAND)
        self.wayLen = wx.TextCtrl(panel, -1, "300",size=(150,30))
        par2Box.Add(self.wayLen, flag=wx.EXPAND, border = 1)'''

        par2Box.Add((10,40))
        par2Box.Add(wx.StaticText(panel,-1,"Уклон съезда",size = (180,20)),flag=wx.EXPAND)
        self.wayAngle = wx.TextCtrl(panel, -1, "20",size=(150,30))
        par2Box.Add(self.wayAngle, flag=wx.EXPAND, border = 1)

        dataBox.Add(par2Box,flag=wx.EXPAND)     # Включить в сайзер
        #dataBox.Add((40,10))

        panel.SetSizer(dataBox)
        panel.SetAutoLayout(True)
        dataBox.Fit(panel)

        pass
    #=====================================================

    def ExecPyFile(self, event):
        if not hasattr(self, "workingdir"):
            self.workingdir = "."
        dlg = wx.FileDialog(self, "Execute Script", self.workingdir, "",
                         "Python Files (*.py)|*.py|All Files (*.*)|*.*",
                         wx.OPEN)
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return False

        fullpathname = dlg.GetPath()
        self.workingdir = os.path.dirname(fullpathname)

        wx.BeginBusyCursor()
        try:
            if self.pyshell:
                locals = self.pyshell.interp.locals
            else:
                locals = None
            execfile(fullpathname, locals)
        except Exception, errno:
            msg = "Error in script [%s]\n%s" % (fullpathname, errno)
            dlg = wx.MessageDialog(self, msg, "Method Error", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            msg = "Unable to execute script [%s]" % fullpathname
        wx.EndBusyCursor()

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "pythonOCC Interactive Console"
        info.Version = VERSION
        info.Copyright = "(C) 2008-2009 Andy Haywood"
        info.Description = "PythonOCC Interactive Console is part of pythonOCC, an free set of Python bindings to OpenCascade library."
        info.WebSite = ("http://www.pythonocc.org", "pythonOCC home page")
        info.Developers = [ "Andy Haywood", "Thomas Paviot"]
        info.License = """This software is governed by the CeCILL license under French law and
        abiding by the rules of distribution of free software.  You can  use, modify and/ or
        redistribute the software under the terms of the CeCILL license as circulated by CEA, CNRS
        and INRIA at the following URL "http://www.cecill.info"."""
        wx.AboutBox(info)

    def OnRestoreDefaultPerspective(self, event):
        """Restore the UI to the default layout."""
        self._mgr.LoadPerspective(self.DefaultPerspective)
        has_help_pane = False
        has_py_pane = False
        for i in range(self.notebook.PageCount):
            pagetext = self.notebook.GetPageText(i)
            if pagetext == "Help":
                has_help_pane = True
            if pagetext == "Python":
                has_py_pane = True
        if not has_help_pane:
            self._createbrowser()
        if not has_py_pane:
            self._createpythonshell()

    def _clearall(self, event):
        self.canva.EraseAll()

    def _refreshui(self):
        setpointer = True
        if self.canva.DynaZoom or self.canva.WinZoom or self.canva.DynaPan or self.canva.DynaRotate:
            setpointer = False
        self.tb1.ToggleTool(self.PointerID, setpointer)
        self.tb1.ToggleTool(self.zoomID, self.canva.DynaZoom)
        self.tb1.ToggleTool(self.zoom_winID, self.canva.WinZoom)
        self.tb1.ToggleTool(self.panID, self.canva.DynaPan)
        self.tb1.ToggleTool(self.rotateID, self.canva.DynaRotate)
        self.canva.SetDynaCursor()

    def SaveAsImage(self, event):
        if not hasattr(self, "workingdir"):
            self.workingdir = "."
        dlg = wx.FileDialog(self, "Save", self.workingdir, "Image.bmp",
                            "Bitmap file (*.bmp)|*.bmp|All Files (*.*)|*.*",
                            wx.SAVE | wx.HIDE_READONLY)
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return False
        else:
            self.canva._3dDisplay.Repaint()
            imagefilename = dlg.GetPath()
            dlg.Destroy()
            if imagefilename:
                self.canva._3dDisplay.Repaint()
                self.canva.SaveAsImage(str(imagefilename))

    def OnRestoreDefaultPerspective(self, event):
        """Restore the UI to the default layout."""
        self._mgr.LoadPerspective(self.DefaultPerspective)
        has_help_pane = False
        has_py_pane = False
        #for i in range(self.notebook.PageCount):
        #    pagetext = self.notebook.GetPageText(i)
        #    if pagetext == "Help":
        #        has_help_pane = True
        #    if pagetext == "Python":
        #        has_py_pane = True
        #if not has_help_pane:
        #    self._createbrowser()
        #if not has_py_pane:
        #    self._createpythonshell()

    def _createbrowser(self):
        url = os.path.join(THISPATH, "doc", "index.html")
        b = browser.Browser(self.notebook, url)
        self.browser = b
        help_icon = CreateMaskedBitmap(os.path.join(THISPATH, 'icons', 'help.png'), 16, 16)
        self.notebook.AddPage(b, "Help", True, help_icon)

    def _createpythonshell(self):
        intronote = "Interactive Python Shell for pythonOCC."
        py = wx.py.shell.Shell(self.panel4, - 1, introText=intronote)
        py.interp.locals["self"] = self
        py.interp.locals["canvas"] = self.canva
        if sys.platform == 'win32':
            py.interp.locals["display"] = self.canva._3dDisplay
        #py_icon = CreateMaskedBitmap(os.path.join(THISPATH, 'icons', 'py.png'), 16, 16)
        #self.notebook.AddPage(py, "Python shell", True, py_icon)
        self.pyshell = py

    def OnSelectionVertex(self, event):
        self.canva._3dDisplay.SetSelectionModeVertex()

    def OnSelectionEdge(self, event):
        self.canva._3dDisplay.SetSelectionModeEdge()

    def OnSelectionFace(self, event):
        self.canva._3dDisplay.SetSelectionModeFace()

    def OnSelectionNeutral(self, event):
        self.canva._3dDisplay.SetSelectionModeNeutral()

    def OnDisplayModeWireframe(self, event):
        self.canva._3dDisplay.SetModeWireFrame()

    def OnDisplayModeShaded(self, event):
        self.canva._3dDisplay.SetModeShaded()

    def OnDisplayModeQHLR(self, event):
        #print "Display QHLR"
        self.canva._3dDisplay.SetModeQuickHLR()

    def OnDisplayModeEHLR(self, event):
        #print "Display EHLR"
        self.canva._3dDisplay.SetModeExactHLR()

    def OnAntialiasingOn(self, event):
        self.canva._3dDisplay.EnableAntiAliasing()
        self.canva_top._3dDisplay.EnableAntiAliasing()
        self.canva_front._3dDisplay.EnableAntiAliasing()

    def OnAntialiasingOff(self, event):
        self.canva._3dDisplay.DisableAntiAliasing()
        self.canva_top._3dDisplay.DisableAntiAliasing()
        self.canva_front._3dDisplay.DisableAntiAliasing()

    def _zoomall(self, event):
        self.canva.SetTogglesToFalse(event)
        self.canva.ZoomAll()
        self._refreshui()

    def _zoomwin(self, event):
        self.canva.SetTogglesToFalse(event)
        self.canva.WinZoom = True
        self.canva._drawbox = None
        self.canva_top.WinZoom = True
        self.canva_top._drawbox = None
        self.canva_front.WinZoom = True
        self.canva_front._drawbox = None
        self._refreshui()

    def _pointer(self, event):
        self.canva.SetTogglesToFalse(event)
        self._refreshui()

    def _dynamiczoom(self, event):
        self.canva.SetTogglesToFalse(event)
        self.canva.DynaZoom = True
        self.canva_top.DynaZoom = True
        self.canva_front.DynaZoom = True
        self._refreshui()

    def _pan(self, event):
        self.canva.SetTogglesToFalse(event)
        self.canva.DynaPan = True
        self.canva_top.DynaPan = True
        self.canva_front.DynaPan = True
        self._refreshui()

    def _rotate(self, event):
        self.canva.SetTogglesToFalse(event)
        self.canva.DynaRotate = True
        self._refreshui()

    def OnOpen(self, event):
        # Choose file dialog
        if not hasattr(self, "_workingdir"):
            self._workingdir = "."
        wild = "STEP (*.step)|*.step|"     \
           "IGES (*.iges)|*.iges|" \
           "STL (*.stl)|*.stl|"    \
           "BRep (*.brep)|*.brep|"   \
           "All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self._workingdir,
            defaultFile="",
            wildcard=wild,
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() <> wx.ID_OK:
            dlg.Destroy()
            return
        path = dlg.GetPath()
        self._workingdir = os.path.dirname(path)
        self._addRecentFileToList(path)
        dlg.Destroy()
        self.LoadFile(path)

    def OnClickRecentFile(self, event):
        # get the file based on the menu ID
        fileNum = event.GetId() - wx.ID_FILE1
        fname = self.filehistory.GetHistoryFile(fileNum)
        self.LoadFile(fname)

    def LoadFile(self, filename):
        extension = os.path.basename(filename).split(".").pop().lower()
        start_time = time.time()
        if extension == "step" or extension == "stp":
            stepReader = STEPControl.STEPControl_Reader()
            stepReader.ReadFile(str(filename))
            numTranslated = stepReader.TransferRoots()
            shape = stepReader.OneShape()
        elif extension == "stl":
            shape = TopoDS.TopoDS_Shape()
            stl_reader = StlAPI.StlAPI_Reader()
            stl_reader.Read(shape, str(filename))
        elif extension == "iges" or extension == "igs":
            i = IGESControl.IGESControl_Controller()
            i.Init()
            iges_reader = IGESControl.IGESControl_Reader()
            iges_reader.ReadFile(str(filename))
            iges_reader.TransferRoots()
            shape = iges_reader.OneShape()
        elif extension == "brep":
            shape = TopoDS.TopoDS_Shape()
            builder = BRep.BRep_Builder()
            BRepTools.BRepTools().Read(shape, str(filename), builder)
        else:
            return True
        self.canva.EraseAll()
        self.canva.DisplayShape(shape)
        wx.SafeYield()
        self.canva._3dDisplay.View_Iso()
        self.canva._3dDisplay.FitAll()
        end_time = time.time()
        self.SetTitle("pythonOCC Interactive Console %s:%s" % (VERSION, filename))
        duration = end_time - start_time
        print "%s STEP file loaded and displayed in %f seconds." % (filename, duration)
        self.msgWin.AppendText("%s STEP file loaded and displayed in %f seconds." %
                               (filename, duration) + "\n")

    def OnExit(self, event):
        self.OnClose(event)

    def OnClose(self, event):
        SaveRecentFiles(self._recentfiles, os.path.join ( THISPATH, "recentfiles" ))
        SaveProt(self)
        needSave = False
        for element in self.canva.drawList:
            needSave = needSave or element[-1]
        #print "Need closing window : " + str(needSave)
        if needSave:
            #SaveProt(self)
            if YesNo(self, u"Выйти без сохранения?", caption=u'Были изменены элементы карьера'):
                self._mgr.UnInit()
                self.Destroy()
            else:
                SaveDB(self)
        else:
            self._mgr.UnInit()
            self.Destroy()

    def _addRecentFileToList(self, fname):
        while fname in self._recentfiles:
            self._recentfiles.remove(fname)
        self._recentfiles.insert(0, fname)
        self.filehistory.AddFileToHistory(fname)

    #===================================================================
    # Обработка меню ГГИС добавил Суханов В.И.
    # Тексты функций расположены в модуле ggisFun.py

    def OnCLine(self, event):
        """Рисование отрезка"""
        CLine(self)

    def OnPLine(self, event):
        """ Рисование ломаной """
        PLine(self)

    def OnCAxis(self, event):
        """ Рисование длинных осей """
        CAxis(self)

    def OnCreateDB(self, event):
        """ Создание элементов в базе данных PostGIS """
        CreateDB(self)

    def OnCExplore(self, event):
        """ Заказ на просмотр элемента """
        CExplore(self)

    def OnCEdit(self,event):
        """ Изменение координат объекта"""
        CEdit(self)

    def onCoord_yes(self, event):
        """ Ввод координат из окна Point от кнопки или мыши """
        Coord_yes(self)

    def OnCancel(self, event):
        """ Отмена рисования элементов """
        self.canva.SetTogglesToFalse(event)
        CancelOp(self)

    def OnDemoPit(self, event):
        """ Прямое рисование элементов карьера без сохранения в СУБД
        для нагрузочного тестирования"""
        self.canva.SetTogglesToFalse(event)
        DemoPit(self)

    def OnLoadDB(self, event):
        """ Загрузка элементов из базы данных PostGIS """
        LoadDB(self)

    def OnSaveDB(self, event):
        """ Сохранить изменения в БД """
        SaveDB(self)

    def OnLidar(self, event):
        """ Рисовать файл .las  """
        Lidar(self)

    def OnEtalon(self, event):
        """ Рисовать файл эталон  """
        Etalon(self)

    def OnRefresh(self, event):
        """ Обновить окно  """
        Refresh(self)

#=== Edit menu =========================================================

    def OnEdBrMerge(self, event):
        """ Разбить линию в точке  """
        self.canva.SetTogglesToFalse(event)
        # сохранить старые привязки
        self.canva.snap.SetSelection(2)
        if self.canva.snap.GetCurrentSelection() == 2:
            self.NavigateMenu(event)
            self.canva.EdCmd = CMD_EdBrMerge
            self.canva.EdStep = 1
            self.SetStatusText("Куда?", 0)
        else:
            self.SetStatusText("*** Нет Near ***", 0)
        pass

    def OnEdBrSelB(self,event):
        """ выбрать бровку """
        self.canva.SetTogglesToFalse(event)
        # сохранить старые привязки
        self.canva.snap.SetSelection(2)
        if self.canva.snap.GetCurrentSelection() == 2:
            self.NavigateMenu(event)
            self.canva.EdCmd = CMD_EdBrSelB
            self.canva.EdStep = 1
            self.SetStatusText("Куда?", 0)
        else:
            self.SetStatusText("*** Нет Near***", 0)
        pass

    def OnEdBrMoveP(self,event):
        self.canva.SetTogglesToFalse(event)
        # сохранить старые привязки
        self.canva.snap.SetSelection(1)
        if self.canva.snap.GetCurrentSelection() == 1:
            self.NavigateMenu(event)
            self.canva.EdCmd = CMD_EdBrMoveP
            self.canva.EdStep = 1
            self.SetStatusText("Куда?", 0)
        else:
            self.SetStatusText("*** Нет End***", 0)
        pass

    def OnEdBrMoveV(self, event):
        """ Перенести вершину бровки """
        self.canva.SetTogglesToFalse(event)
        # сохранить старые привязки
        self.canva.snap.SetSelection(1)
        if self.canva.snap.GetCurrentSelection() == 1:
            self.NavigateMenu(event)
            self.canva.EdCmd = CMD_EdBrMoveV
            self.canva.EdStep = 1
            self.SetStatusText("Куда?", 0)
        else:
            self.SetStatusText("*** Нет End***", 0)
        pass

    def OnEdBrInsV(self, event):
        """ Вставить вершину  """
        self.canva.SetTogglesToFalse(event)
        # сохранить старые привязки
        self.canva.snap.SetSelection(2)
        if self.canva.snap.GetCurrentSelection() == 2:
            self.NavigateMenu(event)
            self.canva.EdCmd = CMD_EdBrInsV
            self.canva.EdStep = 1
            self.SetStatusText("Куда?", 0)
        else:
            self.SetStatusText("*** Нет Near ***", 0)
            #self.SetStatusText("Включите Near", 3)
        pass

    def OnEdBrDelV(self, event):
        """ Удалить вершину  """
        self.canva.SetTogglesToFalse(event)

        self.canva.snap.SetSelection(1)
        if self.canva.snap.GetCurrentSelection() == 1:
            self.NavigateMenu(event)
            self.canva.EdCmd = CMD_EdBrDelV
            self.canva.EdStep = 1
            self.SetStatusText("Куда?", 0)
        else:
            self.SetStatusText("*** Нет End***", 0)
        pass

    def OnEdBrBrkV(self, event):
        """ Разбить линию в точке  """
        self.canva.SetTogglesToFalse(event)
        # сохранить старые привязки
        self.canva.snap.SetSelection(2)
        if self.canva.snap.GetCurrentSelection() == 2:
            self.NavigateMenu(event)
            self.canva.EdCmd = CMD_EdBrBrkV
            self.canva.EdStep = 1
            self.SetStatusText("Куда?", 0)
        else:
            self.SetStatusText("*** Нет Near ***", 0)
        pass

    def OnEdBrDelB(self, event):
        """ Удалить линию  """
        self.canva.SetTogglesToFalse(event)
        self.NavigateMenu(event)
        self.canva.EdCmd   = CMD_EdBrDelB
        self.canva.EdStep = 1
        self.SetStatusText("Укажите объект", 0)
        pass

    def OnInvert(self,event):
        sel_shape = self.canva._3dDisplay.selected_shape
        if not sel_shape:
            self.SetStatusText("Выберите объект и повторите команду", 0)
            return
        if not sel_shape:
            self.SetStatusText("Выберите объект и повторите команду", 0)
            return
        indexInfo = None
        for i in xrange(len(self.canva.drawList)):
            s1 = self.canva.drawList[i][2]
            if s1:
                if s1.Shape().IsEqual(sel_shape):     # Только в классе Shape есть метод IsEqual()
                    indexInfo = i
                    break
        if indexInfo is not None and not self.canva.drawList[indexInfo][0] in (0,1,3):
            return
        w = invert(sel_shape)
        '''
        edge_type=self.egde_typeList[self.canva.drawList[indexInfo][]]
        for i in range(len(self.colorList)):
            if self.colorList[i][0]==edge_type[3]:
                r=int(str(self.colorList[i][2]))/255.0
                g=int(str(self.colorList[i][3]))/255.0
                b=int(str(self.colorList[i][4]))/255.0
                s1=self.canva._3dDisplay.DisplayColoredShape(w, OCC.Quantity.Quantity_Color(r,g,b,0), False)
                break
        '''
        self.canva.drawList[indexInfo][2]=OCC.AIS.AIS_Shape(w)
        self.canva.drawList[indexInfo][-1]=True

    def OnLenth(self, event):
        sel_shape = self.canva._3dDisplay.selected_shape
        if not sel_shape:
            self.SetStatusText("Выберите объект и повторите команду", 0)
            return
        indexInfo = None
        for i in xrange(len(self.canva.drawList)):
            s1 = self.canva.drawList[i][2]
            if s1:
                if s1.Shape().IsEqual(sel_shape):     # Только в классе Shape есть метод IsEqual()
                    indexInfo = i
                    break
        if indexInfo is not None and not self.canva.drawList[indexInfo][0] in (0, 1, 3):
            return
        pnts = getPoints(sel_shape)

        self.msgWin.AppendText("Длинна каркаса: "+str(length(pnts))+"\n")

    def OnDebug(self, event):
        """
        Prints debug information into console
        """
        pass

    def OnAddText(self, event):
        self.canva.EdCmd = CMD_AddText

    def OnShowGrid(self, event):
        if not self.canva.usedHorizons:
            self.SetStatusText("Загрузите объекты для отображения сетки", 0)
            return
        if self.canva.Grid_DoOnce == 0:
            self.canva.Grid_DoOnce = 1
            self.SetView(None, self.canva._3dDisplay.View_Iso)
            self.canva.GridCoords = self.canva.GetWindowCenterPosition(False)
            DrawGrid(self)
            self.GridSlider(None)
            self.canva.ZoomAll()
        else:
            RemoveGrid(self, True)

#====================================================================

if __name__ == "__main__":
    app = wx.PySimpleApp()
    wx.InitAllImageHandlers()
    frame = AppFrame(None)
    if sys.platform == 'win32':
        frame.Show(True)
    else:
        frame.Show(True)
        wx.SafeYield()
        frame.canva.Init3dViewer()
        frame.canva._3dDisplay.View_Iso()
        frame.canva_top.Init3dViewer()
        frame.canva_top._3dDisplay.View_Top()
        frame.canva_front.Init3dViewer()
        frame.canva_front._3dDisplay.View_Front()
        #frame.pyshell.interp.locals["display"] = frame.canva._3dDisplay
    app.SetTopWindow(frame)
    app.MainLoop()
