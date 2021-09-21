# -*- coding: utf-8 -*-

import clr
clr.AddReference("dosymep.Revit.dll")
clr.AddReference("dosymep.Bim4Everyone.dll")

import dosymep
clr.ImportExtensions(dosymep.Revit)
clr.ImportExtensions(dosymep.Bim4Everyone)

from Autodesk.Revit.DB import *

document = __revit__.ActiveUIDocument.Document
category = document.Settings.Categories[BuiltInCategory.OST_ImportObjectStyles]

with Transaction(document, "1") as t:
    t.Start()

    for subCategory in category.SubCategories:
        subCategory.LineColor = Color(0, 0, 0)

    t.Commit()




