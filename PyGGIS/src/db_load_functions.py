#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from regim import *
from utils import pars_geometry
from OCC.BRepBuilderAPI import *
from OCC.BRepPrimAPI import *
from OCC.BRepPrim import *
from OCC.gp import *


def load_horizons(self, horizons):
    self.SetStatusText("Бровки", 2)
    conn = psycopg2.connect("dbname="+POSTGR_DBN+" user="+POSTGR_USR)
    curs = conn.cursor()
    query = "select id_edge,hor,edge_type,ST_AsEWKT(geom),point,color from edge,horizons,edge_type "
    query += "where (id_hor in " + horizons + \
             ") and (edge.hor=horizons.id_hor) and (edge.edge_type=edge_type.id_edge_type);;"
    self.msgWin.AppendText("Query = " + query + "\n")
    curs.execute(query)
    rows = curs.fetchall()
    for record in rows:
        id_edge = int(record[0])
        id_hor = int(record[1])
        edge_type = int(record[2])
        poly_coords = pars_geometry(str(record[3]))
        point = float(record[4])
        if point not in self.canva.usedHorizons:
                self.canva.usedHorizons.append(point)
        color = record[5]
        query = "select red,green,blue from colors where id_color=" + str(color) + ";"
        curs.execute(query)
        red, green, blue = curs.fetchone()
        plgn = BRepBuilderAPI_MakePolygon()
        for pnt in poly_coords:
            if len(pnt) < 3:
                pnt += [point]
            plgn.Add(gp_Pnt(pnt[0], pnt[1], pnt[2]))
        try:
            w = plgn.Wire()
            s = self.canva.DisplayShape(w, OCC.Quantity.Quantity_Color(red, green, blue, 0), False)
            s1 = s.GetObject()
            self.canva.drawList += [[0, id_edge, s1, id_hor, edge_type, False]]
        except:
            self.msgWin.AppendText("Не удалось преобразовать полилинию %i в бровку.\n" % id_hor)

        self.SetStatusText("Готово!", 2)


def load_bodies(self, horizons):
        self.SetStatusText("Тела", 2)
        conn = psycopg2.connect("dbname="+POSTGR_DBN+" user="+POSTGR_USR)
        curs = conn.cursor()
        query = "select id_body,body.id_hor,h_body,body.id_sort,ST_AsEWKT(geom),point,color,color_fill from body,horizons,sorts "
        query += "where (body.id_hor in " + horizons
        query += ") and (body.id_hor=horizons.id_hor) and (body.id_sort=sorts.id_sort);"
        self.msgWin.AppendText("Query = " + query + "\n")
        curs.execute(query)
        rows = curs.fetchall()
        for record in rows:
            id_body = int(record[0])
            id_hor = int(record[1])
            h_body = int(record[2])
            if h_body not in self.canva.usedHorizons:
                self.canva.usedHorizons.append(float(h_body))
            id_sort = int(record[3])
            poly_coords = pars_geometry(str(record[4]))
            point = float(record[5])
            color = int(record[6])
            color_fill = int(record[7])
            query = "select red,green,blue from colors where id_color=" + str(color) + ";"
            curs.execute(query)
            red, green, blue = curs.fetchone()

            plgn = BRepBuilderAPI_MakePolygon()
            for pnt in poly_coords:
                if len(pnt) < 3:
                    pnt += [point]
                plgn.Add(gp_Pnt(pnt[0], pnt[1], pnt[2]))
            try:
                w = plgn.Wire()
                my_face = BRepBuilderAPI_MakeFace(w).Shape()
                aPrismVec = gp_Vec(0, 0, h_body)
                my_body = BRepPrimAPI_MakePrism(my_face, aPrismVec).Shape()
                #self.canva._3dDisplay.Context.SetMaterial(myBody,4)
                s = self.canva.DisplayShape(my_body, OCC.Quantity.Quantity_Color(red, green, blue, 0), False)
                s1 = s.GetObject()
                self.canva.drawList += [[1, id_body, s1, id_hor, point, h_body, id_sort, color, color_fill, False]]
            except:
                self.msgWin.AppendText("Не удалось преобразовать полилинию %i в тело.\n" % id_body)

        self.SetStatusText("Готово!", 2)


def load_skv(self, horizons):
    self.SetStatusText("Скважины", 2)
    conn = psycopg2.connect("dbname="+POSTGR_DBN+" user="+POSTGR_USR)
    curs = conn.cursor()
    query = "select id_drill_fld,horiz,coord_system,type_drill,coord_x,coord_y,coord_z,name from drills"
    query = query + " where (horiz in " + horizons + ");"
    curs.execute(query)
    rows = curs.fetchall()
    for record in rows:
        id_drill_fld, horiz, coord_system, type_drill, coord_x, coord_y, coord_z, name = record
         #Прочитать глубину скважины из БД
        query = "SELECT val FROM dril_pars WHERE (id_par=6) and (id_drill=" + str(id_drill_fld) + ");"
        curs.execute(query)
        pars = curs.fetchone()
        if pars:
            dept = pars[0]
        else:
            dept = 16.0
        position = gp_Ax2(gp_Pnt(coord_x, coord_y, coord_z), gp_Dir(0, 0, - 1))
        skv = BRepPrim_Cylinder(position, 0.1, dept)
        skv = skv.Shell()
        s = self.canva.DisplayShape(skv, 'YELLOW', False)
        s1 = s.GetObject()
        self.canva.drawList += [[2, id_drill_fld, s1, horiz, coord_system, type_drill, coord_x, coord_y, coord_z, dept, name, False]]
    self.SetStatusText("Готово!", 2)


def load_isolines(self):
    izoLst = (-10000, +10000)
    self.SetStatusText("Изолинии", 2)
    conn = psycopg2.connect("dbname="+POSTGR_DBN+" user="+POSTGR_USR)
    curs = conn.cursor()
    query = "select id_topo,heigth,coord_sys,ST_AsEWKT(geom) from topograph "
    query = query + "where (heigth>='" + str(izoLst[0]) + "')and(heigth<='" + str(izoLst[1]) + "')"
    self.msgWin.AppendText("Query = " + query + "\n")
    curs.execute(query)
    rows = curs.fetchall()
    for record in rows:
        id_topo = int(record[0])
        heigth = int(record[1])
        coord_sys = int(record[2])
        poly_coords = pars_geometry(str(record[3]))
        plgn = BRepBuilderAPI_MakePolygon()
        for pnt in poly_coords:
            plgn.Add(gp_Pnt(pnt[0], pnt[1], heigth))
        w = plgn.Wire()
        s = self.canva.DisplayShape(w, 'GREEN', False)
        s1 = s.GetObject()
        self.canva.drawList += [[3, id_topo, s1, heigth, coord_sys, False]]
    self.SetStatusText("Готово!", 2)