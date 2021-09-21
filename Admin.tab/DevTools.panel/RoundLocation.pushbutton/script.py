# -*- coding: utf-8 -*-

import clr
clr.AddReference("dosymep.Revit.dll")
clr.AddReference("dosymep.Bim4Everyone.dll")

import dosymep
clr.ImportExtensions(dosymep.Revit)
clr.ImportExtensions(dosymep.Bim4Everyone)

from Autodesk.Revit.DB import *

document = __revit__.ActiveUIDocument.Document
elements = __revit__.ActiveUIDocument.GetSelectedElements()
elements = [e for e in elements if e.Category.Id == ElementId(BuiltInCategory.OST_Columns) or e.Category.Id == ElementId(BuiltInCategory.OST_StructuralColumns)]

def base_round(x, base=0.5):
    return base * round(float(x) / base, 2)

with Transaction(document, "Округление") as transaction:
    transaction.Start()

    for element in elements:
        point = element.Location.Point
        print "Before: " + str(point)

        point = XYZ(base_round(point.X), base_round(point.Y), base_round(point.Z))
        element.Location.Point = point

        print "After: " + str(element.Location.Point)

    transaction.Commit()



