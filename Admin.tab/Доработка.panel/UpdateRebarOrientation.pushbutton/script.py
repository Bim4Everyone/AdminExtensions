# -*- coding: utf-8 -*-

import clr
clr.AddReference("dosymep.Revit.dll")
clr.AddReference("dosymep.Bim4Everyone.dll")

import dosymep
clr.ImportExtensions(dosymep.Revit)
clr.ImportExtensions(dosymep.Bim4Everyone)

from System import *
from System.Collections.Generic import *

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

from pyrevit import forms


application = __revit__.Application
document = __revit__.ActiveUIDocument.Document
activeView = document.ActiveView

options = Options()
options.View = activeView

if not isinstance(document.ActiveView, View3D):
    forms.alert("Активный вид должен быть 3D", exitscript=True)


class RebarElement:
    def __init__(self, element):
        self.Element = element
        self.Host = document.GetElement(element.GetHostId())

    @property
    def BoundingBox(self):
        solid = next((g for g in self.Element.get_Geometry(options) if isinstance(g, Solid)), None)
        if solid:
            return solid.GetBoundingBox().Max - solid.GetBoundingBox().Min

        return self.Element.get_BoundingBox(activeView).Max - self.Element.get_BoundingBox(activeView).Min

    @property
    def HostCategory(self):
        return self.Host.Category

    @property
    def ZIsLonger(self):
        return self.BoundingBox.Z > self.BoundingBox.X and self.BoundingBox.Z > self.BoundingBox.Y

    @property
    def XIsLonger(self):
        return self.BoundingBox.X > self.BoundingBox.Z and self.BoundingBox.X > self.BoundingBox.Y

    @property
    def YIsLonger(self):
        return self.BoundingBox.Y > self.BoundingBox.Z and self.BoundingBox.Y > self.BoundingBox.X

    @property
    def IsAllowProcess(self):
        if self.HostCategory.Id == ElementId(BuiltInCategory.OST_Walls):
            wall_bounding_box = self.Host.get_BoundingBox(activeView).Max - self.Host.get_BoundingBox(activeView).Min
            if wall_bounding_box.Z > wall_bounding_box.X and wall_bounding_box.Z > wall_bounding_box.Y:
                return (wall_bounding_box.Z / 2) < self.BoundingBox.Z
            elif wall_bounding_box.X > wall_bounding_box.Z and wall_bounding_box.X > wall_bounding_box.Y:
                return (wall_bounding_box.X / 2) < self.BoundingBox.X
            else:
                return (wall_bounding_box.Y / 2) < self.BoundingBox.Y

        return True


category_list = List[Type]()
category_list.Add(Rebar)
category_list.Add(RebarInSystem)

category_filter = ElementMulticlassFilter(category_list)
elements = FilteredElementCollector(document, document.ActiveView.Id)\
    .WherePasses(category_filter)\
    .WhereElementIsNotElementType()\
    .ToElements()

rebar_elements = [ RebarElement(element) for element in elements ]
rebar_elements = [ element for element in rebar_elements
                   if element.HostCategory.Id == ElementId(BuiltInCategory.OST_Walls)
                   or element.HostCategory.Id == ElementId(BuiltInCategory.OST_Columns)
                   or element.HostCategory.Id == ElementId(BuiltInCategory.OST_StructuralColumns)]

with Transaction(document) as transaction:
    transaction.Start("Обновление ориентации арматуры")

    for rebar in rebar_elements:
        if rebar.IsAllowProcess:
            host_mark = rebar.Element.GetParamValueOrDefault(BuiltInParameter.REBAR_ELEM_HOST_MARK)
            structure_mark = "{}{}".format(host_mark, "_Вертик" if rebar.ZIsLonger else "_Гориз")

            rebar.Element.SetParamValue("Мрк.МаркаКонструкции", structure_mark)

    transaction.Commit()