#!/usr/bin/env python
# -*- coding: utf-8 -*-
##Copyright  2010, 2011 Владимир Суханов 
##
#/****************************************************************
# * This java applet shows an incremental algorithm for Delaunay *
# * Triangulations. It can also find Voronoi Diagrams and Convex *
# * Hulls.                                                       *
# *                                                              *
# * Author : Conglin Lu.                                         *
# * Date: 6/25/96                                                *
# *                                                              *
# ***************************************************************/


#/******************************************************************
#*    Edge class. Defines a quadedge structure, which contains the *    
#*        information of endpoints, various adjacent edges, *    
#*        and dual edges.                      *
#*    - isValidEdge():    whether it's visible          *
#******************************************************************/
from math import *
global mCol, Pnts

TOLERANCE = 0.0001
mCol = []
Pnts = []

class Edge:
    def __init__(self):
        self.org = None # Origin -- Начало
        self.Onext = None # next counterclockwise edge -- следующее
        self.Rot = None # dual edge -- дуальное ребро
    # setting edge properties 
    def SetOrg(self, pt):
        # from point x,y связать ребро с точкой где ребро начинается
        self.org = pt
    def SetDest(self, pt):
        # to Cpoint  связать ребро с точкой где заканчивается сторона треугольника
        self.Sym().org = pt
    def SetRot(self, e):
        # rot edge установить ссылку на другое ребро по часовой стрелке
        self.Rot = e
    def SetSym(self, e):
        # sym edge усановить ссылку на симметричное ребро по часовой стрелке
        self.Rot.Rot = e
    def SetRot3(self, e):
        # rot for 4 vert Обычно это ссылка для замыкания структуры из 4-х вершин
        self.Rot.Rot.Rot = e
    def SetOnext(self, e):
        # установить ссылку на другое ребро против часовой стрелки
        self.Onext = e
    def SetLnext(self, e):
        # next for 4 vert установить ссылку для 3-го ребра по часовой, которое слева
        self.Rot3().Onext.Rot = e
    def SetOprev(self, e):
        # pred vert предыдущая вершина
        self.Rot.Onext.Rot = e
    def SetRnext(self, e):
        # следующая справа
        self.rn = self.Rot.Onext.Rot3()
        rn = e
 
    #getting information
    def GetOrg(self):
        return self.org
    def GetDest(self):
        return self.Sym().org
    def GetRot(self):
        return self.Rot
    def Sym(self):
        return self.Rot.Rot
    def Rot3(self):
        return self.Rot.Rot.Rot
    def GetOnext(self):
        return self.Onext
    def GetLnext(self):
        return self.Rot3().Onext.Rot
    def GetOprev(self):
        return self.Rot.Onext.Rot
    def GetRnext(self):
        return self.Rot.Onext.Rot3()
    def GetDprev(self):
        return self.Rot3().Onext.Rot3()
    def GetLprev(self):
        return self.Onext.Sym()
    def isValidEdge(self):
        og = self.GetOrg()
        dt = self.GetDest()
        if ((og == None) or og.isInf or (dt == None) or (dt.isInf)):
            return False
        else:
            return True
# end class Edge

def MakeQEdge():
        e = []
        for i in range(4):
            e.append(Edge())     
        #set initial relationships
        e[0].SetRot(e[1]);
        e[1].SetRot(e[2]);
        e[2].SetRot(e[3]);
        e[3].SetRot(e[0]);
        e[0].SetOnext(e[0]);
        e[1].SetOnext(e[3]);
        e[2].SetOnext(e[2]);
        e[3].SetOnext(e[1]);

        for i in range(4): 
            mCol.append(e[i]);

        return e[0];

def Splice(a, b):
        aa = a.GetOnext().GetRot();
        bb = b.GetOnext().GetRot();

        tmp = a.GetOnext();
        a.SetOnext(b.GetOnext());
        b.SetOnext(tmp);

        tmp = aa.GetOnext();
        aa.SetOnext(bb.GetOnext());
        bb.SetOnext(tmp);

def Connect(a, b):
        e = MakeQEdge();
        e.SetOrg(a.GetDest());
        e.SetDest(b.GetOrg());
        Splice(e, a.GetLnext());
        Splice(e.Sym(), b);
        return e;
        #Connect

def DeleteEdge(e):
        Splice(e, e.GetOprev());
        Splice(e.Sym(), e.Sym().GetOprev());
    
        #eRot = Edge();
        for i in range(3):  #(int i=0; i<3; i++) {
            eRot = e.GetRot();
            #removeElement(e);
            mCol.remove(e);
            e = eRot;        
        #removeElement(e);
        mCol.remove(e);
        # DeleteEdge
        
def Swap(e):
        a = e.GetOprev();
        b = e.Sym().GetOprev();
        Splice(e, a);
        Splice(e.Sym(), b);
        Splice(e, a.GetLnext());
        Splice(e.Sym(), b.GetLnext());
        e.SetOrg(a.GetDest());
        e.SetDest(b.GetDest());
        # Swap
        
    #prepare for animation
    #public void setAnimation() {
    #if (testEdges == null)
    #    testEdges = new Vector();
    #else
    #    testEdges.removeAllElements();
#
    #if (newEdges == null)
    #    newEdges = new Vector();
    #else
    #    newEdges.removeAllElements();    
#
    #if (testGroup == null)
    #    testGroup = new Vector();
    #else
    #    testGroup.removeAllElements();
    #}

def PeqP(p1, p2):     # p1 == p2
        return ((abs(p1.x - p2.x) < TOLERANCE) and (abs(p1.y - p2.y) < TOLERANCE))

def _e(edge):
    return ("edge=", [edge.org, edge.Rot, edge.Onext])

def _p(p):
    return ("p=", [p.x, p.y, p.z])

def LocateE(P): # проверить Врет!
        #print "LocateE: ", _p(P)
        edge = mCol[0]
        n = 0
        while(n < len(mCol)):    # защита от зацикливания
            #print _e(edge)
            if PeqP(P, edge.GetOrg()) or PeqP(P, edge.GetDest()):
                return edge
                break   # точка на конце стороны тр-ка  
            if (P.isRightOf(edge)):     # справа от ребра
                edge = edge.Sym();      # перейти по ребру к концу
            else:                       # слева
                if (not(P.isRightOf(edge.Onext))):  # слева от следующего ребра
                    edge = edge.Onext;  # перейти на ребро против часовой
                else:                   # справа от следующего ребра
                    if (not(P.isRightOf(edge.GetDprev()))): # справа от dual ребра
                        edge = edge.GetDprev();
                    else:
                        return edge
                        break
            n = n + 1
        if (n >= len(mCol)):    # не нашли ребро
            return None
        else:
            return edge

def GetZ(X, Y):    
    Z = - 10000#
    pnt = CPoint(X, Y, 0)
    E1 = LocateE(pnt)   # //where is Pnt?
    if (E1 == None):
        E1 = mCol[0]    # точка из бесконечности со средней отметкой
        P1 = E1.GetOrg()
        Z = P1.z
        #print 'Z1=',Z
    else:
        P1 = E1.GetOrg()
        P2 = E1.GetDest()
        if pnt.isRightOf(E1):
            #P3 = E1.GetLprev().GetOrg()
            P3 = E1.GetRnext().GetOrg()
        else:
            #P3 = E1.GetRnext().GetOrg()
            P3 = E1.GetLprev().GetOrg()
        #print 'P1,P2,P3=',[P1.x,P1.y,P1.z],[P2.x,P2.y,P2.z],[P3.x,P3.y,P3.z]
        dx  = X-P1.x; dy = Y-P1.y;
        #print '(dx,dy)=',(dx,dy)
        dx2 = P2.x-P1.x; dy2 = P2.y-P1.y; dz2 = P2.z-P1.z;
        #print '(dx2,dy2,dz2)=',(dx2,dy2,dz2)
        dx3 = P3.x-P1.x; dy3 = P3.y-P1.y; dz3 = P3.z-P1.z;
        #print '(dx3,dy3,dz3)=',(dx3,dy3,dz3)
        Tz = dy2*dx3 - dx2*dy3 
        #print 'Tz=',Tz
        if (abs(Tz) < 0.00001):
            Z = P1.z
            #print 'Z2=',Z
        else:
            dz = (dx*(dy2*dz3 - dz2*dy3) + dy*(dz2*dx3 - dx2*dz3))/Tz;
            Z = P1.z + dz
            #print 'Z3=',Z
    return Z

def printDiagram():
        i = 12
        while (i < len(mCol)):
            E1 = mCol[i];
            P1 = E1.GetOrg()
            P2 = E1.GetDest()
            P3 = E1.GetRnext().GetOrg() #Right
            P4 = E1.GetLprev().GetOrg() # Left
            print 'P1,P2,Right,Left=',[P1.x,P1.y,P1.z],[P2.x,P2.y,P2.z],[P3.x,P3.y,P3.z],[P4.x,P4.y,P4.z]
            i = i + 4


#def GetVoronoiDiagram():
#        i = 12
#        while (i < len(mCount)):
#            e = mCol[i];
#            if (e.isValidEdge()):
#                pl = getVoronoiVertex(e, e.GetOnext());
#                pr = getVoronoiVertex(e, e.GetOprev());
#                e.Rot.SetOrg (pr);
#                e.Rot.SetDest(pl);
#            i = i + 4
#
    #Computes the Voronoi vertices, which are the intersecting points of
    #the dual edges of Delaunay Triangulation.
#def getVoronoiVertex(e1, e2):
#        pnt = CPoint(0, 0);
#        x2 = e1.GetOrg().x;
#        y2 = e1.GetOrg().y;
#        x1 = e1.GetDest().x;
#        y1 = e1.GetDest().y;
#        x3 = e2.GetDest().x;
#        y3 = e2.GetDest().y;
#
#        det = (y2-y3)*(x2-x1) - (y2-y1)*(x2-x3);
#        c1 = (x1+x2)*(x2-x1)/2 + (y2-y1)*(y1+y2)/2;
#        c2 = (x2+x3)*(x2-x3)/2 + (y2-y3)*(y2+y3)/2;
#        pnt.x = (int) ((c1*(y2-y3) - c2*(y2-y1)) / det);
#        pnt.y = (int) ((c2*(x2-x1) - c1*(x2-x3)) / det);
#        pnt.isInf = False;
#
#        return pnt;

#Computes the sign of the orientable area. Used to determine whether
#a point is to the left, right, or on an give edge.
def Area(p1, p2, p3):
        return((p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y));
   

#/************************************************************************
#*    Graph class. Base class for general graphs using quadedge         *
#*            representation.                    *
#*    - MakeQEdge():     Generates a new edge;                *
#*    - Splice():    Changes the topological relationships between    *
#*            two edges;                    *
#************************************************************************/
 
#class Graph:
#    pass

#/***************************************************************************
#*    DelaunayGraph class. Computes Delaunay Triangulation, Voronoi Diagram *
#*                and Convex Hull.               *
#*    - init():    adds 3 points at "infinity";               *
#*    - Connect():    connects two points and update edge structures;       *
#*    - DeleteEdge(): deletes an existing edge, inverse of Connect();       *
#*    - Swap():    makes changes in a certain quadrilateral;       *
#*    - setAnimation(): prepare for animation                   *
#*    - InsertSite():    inserts a new point in the graph;           *
#*    - Locate():    locates a new point;                   *
#*    - GetVoronoiDiagram():    computes the dual graph -- Voronoi Diagram *
#*    - draw():    draws the graph;                   *
#***************************************************************************/

class DelaunayGraph:
    #Vector testEdges, newEdges, testGroup;

    def __init__(self, Pnts):
        e1 = MakeQEdge();
        e2 = MakeQEdge();
        e3 = MakeQEdge();

        ##Three points at infinity
        e1.SetOrg(Pnts[0]);
        e2.SetOrg(Pnts[1]);
        e3.SetOrg(Pnts[2]);

        e1.SetDest(e2.GetOrg());
        e1.GetOrg().isInf = True;
        e2.SetDest(e3.GetOrg());
        e2.GetOrg().isInf = True;
        e3.SetDest(e1.GetOrg());
        e3.GetOrg().isInf = True;

        e1.SetOnext(e3.Sym());
        e1.GetRot().SetOnext(e2.GetRot());
        e1.Sym().SetOnext(e2);
        e1.Rot3().SetOnext(e2.Rot3());

        e2.SetOnext(e1.Sym());
        e2.GetRot().SetOnext(e3.GetRot());
        e2.Sym().SetOnext(e3);
        e2.Rot3().SetOnext(e3.Rot3());

        e3.SetOnext(e2.Sym());
        e3.GetRot().SetOnext(e1.GetRot());
        e3.Sym().SetOnext(e1);
        e3.Rot3().SetOnext(e1.Rot3());
        #init
        
    def InsertPoint(self, P):   # Вставить точку CPoint P в граф
        e = LocateE(P);    #where is X?
        if (e == None):
            return
        if (P.isOn(e)):    #on a edge
            t = e.GetOprev();
            DeleteEdge(e);
            e = t;

        # connects X to existing points
        newEdge = MakeQEdge();    
        StartPnt = e.GetOrg();
        newEdge.SetOrg(StartPnt);
        newEdge.SetDest(P);
        Splice(newEdge, e);
        while True: 
            newEdge = Connect(e, newEdge.Sym());
            e = newEdge.GetOprev();
            if (e.GetDest() == StartPnt): 
                break
        # makes necessary changes in the graph
        while True:
            t = e.GetOprev();
            passTest = P.isInCircle(e.GetOrg(), t.GetDest(), e.GetDest());
            if (t.GetDest().isRightOf(e) and passTest):
                #P is in the circle. Should delete an old edge and add a new one.
                Swap(e);
                e = e.GetOprev();
            else:
                if (e.GetOrg() == StartPnt):
                    return
                else:
                    e = e.GetOnext().GetLprev();
                    

#/****************************************************************
#*   CPoint class.                         *
#*     - isOn():    Whether it's on an edge;        *
#*    - isRightOf():    Whether it's to the right of an edge;    *
#*    - isLeftOf():    Whether it's to the left of an edge;    *
#*    - isInCircle(): Whether it's in a circle        *
#*    - draw():    draws the point;            *
#****************************************************************/

class CPoint:  
    def __init__(self, x, y, z):
        self.x = x;
        self.y = y;
        self.z = z;
        self.isInf = False; 

    def isOn(self, e):
        pts = e.GetOrg();
        pte = e.GetDest();
        return (Area(pts, self, pte) == 0);

    def isRightOf(self, e):
        pts = e.GetOrg();
        pte = e.GetDest();
        return (Area(self, pts, pte) > 0);

    def isLeftOf(self, e):
        pts = e.GetOrg();
        pte = e.GetDest();
        return (Area(self, pts, pte) < 0);

    def isInCircle(self, p1, p2, p3):
        x4 = self.x;
        y4 = self.y;
        x1 = p1.x;
        y1 = p1.y;
        x2 = p2.x;
        y2 = p2.y;
        x3 = p3.x;
        y3 = p3.y;

        a = (x2 - x1) * (y3 - y1) * (x4 * x4 + y4 * y4 - x1 * x1 - y1 * y1) + \
        (x3 - x1) * (y4 - y1) * (x2 * x2 + y2 * y2 - x1 * x1 - y1 * y1) + \
        (x4 - x1) * (y2 - y1) * (x3 * x3 + y3 * y3 - x1 * x1 - y1 * y1) - \
        (x2 - x1) * (y4 - y1) * (x3 * x3 + y3 * y3 - x1 * x1 - y1 * y1) - \
        (x3 - x1) * (y2 - y1) * (x4 * x4 + y4 * y4 - x1 * x1 - y1 * y1) - \
        (x4 - x1) * (y3 - y1) * (x2 * x2 + y2 * y2 - x1 * x1 - y1 * y1);

        return (a > 0);
    