# -*- coding: utf-8 -*-

from System.Collections.Generic import List

from Autodesk.Revit.DB import *

document = __revit__.ActiveUIDocument.Document

elements = FilteredElementCollector(document).OfClass(SharedParameterElement).WhereElementIsNotElementType().ToElements()
if elements:
    elements = [ element for element in elements if element.GetDependentElements(None).Count == 1  ]
    with Transaction(document) as transaction:
        transaction.Start("Удаление параметров")
        for element in elements:
            try:
                print str(element.GuidValue) +" - " + str(element.Id.IntegerValue) + " - " + element.Name
                document.Delete(element.Id)
            except Exception as ex:
                print str(ex)

        transaction.Commit()