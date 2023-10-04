# -*- coding: utf-8 -*-

import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("dosymep.Revit.dll")
clr.AddReference("dosymep.Bim4Everyone.dll")

from System.Windows.Forms import *

from Autodesk.Revit.DB import *
from Autodesk.Revit.ApplicationServices import *

from pyrevit import EXEC_PARAMS

from dosymep.Revit import *
from dosymep.Bim4Everyone import *
from dosymep_libs.bim4everyone import *
from dosymep_libs.simple_services import *

application = __revit__.Application  # type: Application


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
        document = application.NewProjectDocument(ModuleEnvironment.EmptyTemplatePath)
        document.SaveAs(file_name, SaveAsOptions())
        document.Close(False)

        __revit__.OpenAndActivateDocument(file_name)


script_execute()
