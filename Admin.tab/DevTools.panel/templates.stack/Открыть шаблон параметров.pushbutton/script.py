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
    if not __revit__.Application.Username.lower() == "biseuv_o" \
            or __revit__.Application.Username.lower() == "budaeva_v" \
            or __revit__.Application.Username.lower() == "tikhomirov_amgvxad":
        script.exit()

    __revit__.OpenAndActivateDocument(ModuleEnvironment.ParametersTemplatePath)


script_execute()