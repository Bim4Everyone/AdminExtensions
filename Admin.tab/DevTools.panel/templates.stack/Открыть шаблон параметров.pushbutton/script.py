# -*- coding: utf-8 -*-

import clr
clr.AddReference("dosymep.Revit.dll")
clr.AddReference("dosymep.Bim4Everyone.dll")

import dosymep
clr.ImportExtensions(dosymep.Revit)
clr.ImportExtensions(dosymep.Bim4Everyone)

from pyrevit import forms
from pyrevit import EXEC_PARAMS

from dosymep.Revit import *
from dosymep.Bim4Everyone import *
from dosymep_libs.bim4everyone import *

from Autodesk.Revit.DB import *


@notification()
@log_plugin(EXEC_PARAMS.command_name)
def script_execute(plugin_logger):
    users = ["biseuv_o", "tikhomirov_amgvxad", "tikhomirov_am"]
    if __revit__.Application.Username.lower() not in users:
        script.exit()

    __revit__.OpenAndActivateDocument(ModuleEnvironment.ParametersTemplatePath)


script_execute()
