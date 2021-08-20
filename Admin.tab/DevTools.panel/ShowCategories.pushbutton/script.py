# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import *

document = __revit__.ActiveUIDocument.Document
elements = FilteredElementCollector(document)\
                .WhereElementIsNotElementType()\
                .ToElements()

categories = set([e.Category.Name for e in elements if e.Category])
categories = sorted(categories)
print "\r\n".join([c for c in categories])