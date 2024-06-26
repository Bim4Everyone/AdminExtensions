# -*- coding: utf-8 -*-

import clr

clr.AddReference("EPPlus")
clr.AddReference("dosymep.Revit.dll")
clr.AddReference("dosymep.Bim4Everyone.dll")

from System.IO import *
from System.Diagnostics import *

from OfficeOpenXml import *
from Autodesk.Revit.DB import *

from pyrevit import forms
from pyrevit import script

import dosymep
clr.ImportExtensions(dosymep.Revit)
clr.ImportExtensions(dosymep.Bim4Everyone)

active_document = __revit__.ActiveUIDocument.Document


def get_families_documents(document):
    families = FilteredElementCollector(document) \
        .OfClass(Family) \
        .ToElements()

    return [document.EditFamily(family) for family in families if family.IsEditable]


def get_shared_parameters(document):
    result = []

    for family_document in get_families_documents(document):
        shared_params = FilteredElementCollector(family_document) \
            .OfClass(SharedParameterElement) \
            .WhereElementIsNotElementType() \
            .ToElements()

        result.append((family_document, shared_params))

    return result


def export_to_excel():
    file_name, shared_params = get_script_data()

    with ExcelPackage() as excelPackage:
        for (document, params) in shared_params:
            if not params:
                continue

            sorted(params, key=lambda x: x.Name)
            worksheet = excelPackage.Workbook.Worksheets.Add(document.Title)

            worksheet.Cells[1, 1].Value = "GUID"
            worksheet.Cells[1, 2].Value = "Id"
            worksheet.Cells[1, 3].Value = "Name"

            worksheet.Cells[1, 3].AutoFilter = True
            worksheet.Cells[1, 3].Style.Font.Bold = True
            worksheet.Cells[1, 2].Style.Font.Bold = True
            worksheet.Cells[1, 1].Style.Font.Bold = True

            for (param, index) in zip(params, range(2, len(params) + 2)):
                worksheet.Cells[index, 1].Value = param.GuidValue
                worksheet.Cells[index, 2].Value = param.Id.GetIdValue()
                worksheet.Cells[index, 3].Value = param.Name

            worksheet.Cells.AutoFitColumns(0)

        excelPackage.SaveAs(FileInfo(file_name))

    Process.Start(file_name)


def get_script_data():
    shared_params = get_shared_parameters(active_document)
    if not shared_params:
        script.exit()

    file_name = forms.save_file(files_filter="Excel файлы (*.xlsx)|*.xlsx", default_name=active_document.Title)
    if not file_name:
        script.exit()

    return file_name, shared_params


export_to_excel()
