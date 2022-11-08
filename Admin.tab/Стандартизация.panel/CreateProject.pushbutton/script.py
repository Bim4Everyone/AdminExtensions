# -*- coding: utf-8 -*-

import os

import clr
clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import *

from Autodesk.Revit.DB import *
from Autodesk.Revit.ApplicationServices import *

from pyrevit import EXEC_PARAMS

from dosymep_libs.bim4everyone import log_plugin
from dosymep_libs.simple_services import notification

application = __revit__.Application # type: Application

template_file_path = r"T:\Проектный институт\Отдел стандартизации BIM и RD\BIM-Ресурсы\5-Надстройки\Bim4Everyone\A101"
template_file_path = os.path.join(template_file_path, application.VersionNumber, "RevitCopyStandarts")

def get_file_path():
    with SaveFileDialog() as dialog:
        dialog.RestoreDirectory = True
        dialog.Filter = "Revit files (*.rvt)|*.rvt"
        
        if dialog.ShowDialog() == DialogResult.OK:
            return dialog.FileName

    return None

@notification()
@log_plugin(EXEC_PARAMS.command_name)
def script_execute(plugin_logger):
    file_name = get_file_path()
    if file_name:
        document = application.NewProjectDocument(template_file_path)
        document.SaveAs(file_name, SaveAsOptions())
        document.Close(False)

        __revit__.OpenAndActivateDocument(file_name)


script_execute()