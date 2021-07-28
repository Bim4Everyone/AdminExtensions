# -*- coding: utf-8 -*-

from System.Collections.Generic import List

from Autodesk.Revit.DB import *

document = __revit__.ActiveUIDocument.Document

elements = FilteredElementCollector(document).OfClass(SharedParameterElement).WhereElementIsNotElementType().ToElements()
if elements:
    elements = [ element for element in elements if element.GetDependentElements(None).Count == 1  ]
    print "\r\n".join([ str(element.GuidValue) +" - " + str(element.Id.IntegerValue) + " - " + element.Name for element in elements ])

    with Transaction(document) as transaction:
        transaction.Start("Удаление параметров")

        document.Delete(List[ElementId]([ element.Id for element in elements ]))

        transaction.Commit()