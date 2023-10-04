# -*- coding: utf-8 -*-

from System import InvalidOperationException

from Autodesk.Revit.DB import *

from pyrevit import forms
from pyrevit import revit
from pyrevit import EXEC_PARAMS

from dosymep_libs.bim4everyone import log_plugin
from dosymep_libs.simple_services import notification

application = __revit__.Application
document = __revit__.ActiveUIDocument.Document

@notification()
@log_plugin(EXEC_PARAMS.command_name)
def script_execute(plugin_logger):
    schedule = document.ActiveView
    if schedule.ViewType != ViewType.Schedule:
        forms.alert("Данная операция доступна только для спецификаций.", exitscript=True)

    elements = FilteredElementCollector(schedule.Document, schedule.Id).ToElements()

    with revit.Transaction("Обновление спецификации"):
        for element in elements:
            typeParameter = element.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM)
            nameParameter = element.get_Parameter(BuiltInParameter.RVT_LINK_INSTANCE_NAME)

            if typeParameter is not None and nameParameter is not None:
                nameParameter.Set(typeParameter.AsValueString())


script_execute()
