# -*- coding: utf-8 -*-

import clr

from System import InvalidOperationException

from dosymep_libs.bim4everyone import *
from dosymep_libs.simple_services import *

clr.AddReference("dosymep.Revit.dll")
clr.AddReference("dosymep.Bim4everyone.dll")

from pyrevit import HOST_APP
from pyrevit import EXEC_PARAMS


def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    pass
    # чтобы нормально работала панель,
    # она должна быть инициализированная заранее
    # RevitFamilyExplorer.RegisterFamilyExplorerCommand().RegisterPanel(__rvt__)


@notification()
@log_plugin(EXEC_PARAMS.command_name)
def script_execute(plugin_logger):
    raise InvalidOperationException("Команда отключена на доработку.")
    # RevitFamilyExplorer.FamilyExplorerCommand().ChangeVisiblePanel(__revit__)


if __name__ == '__main__':
    script_execute()
