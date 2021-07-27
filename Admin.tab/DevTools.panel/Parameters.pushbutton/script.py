# -*- coding: utf-8 -*-

from System.IO import File
from System.Text import Encoding
from System.Diagnostics import Process

from Autodesk.Revit.DB import *

from pyrevit import forms

document = __revit__.ActiveUIDocument.Document

elements = FilteredElementCollector(document).OfClass(SharedParameterElement).WhereElementIsNotElementType().ToElements()
if elements:
    result = [ "Id;ParamName" ]
    for element in elements:
        result.append(str(element.Id.IntegerValue) + ";" + element.Name)

    fileName = forms.save_file(files_filter="csv files (*.csv)|*.csv", default_name="Параметры")
    if fileName:
        File.WriteAllText(fileName, "\r\n".join(result), Encoding.GetEncoding(1251))
        Process.Start(fileName)