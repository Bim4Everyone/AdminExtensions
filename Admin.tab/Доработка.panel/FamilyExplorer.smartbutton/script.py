# -*- coding: utf-8 -*-

import dosymep_libs
dosymep_libs.load_assemblies()

import clr
clr.AddReference("dosymep.Revit.dll")
clr.AddReference("dosymep.Bim4everyone.dll")

from pyrevit import HOST_APP

if HOST_APP.version == "2020":
    clr.AddReference("RevitFamilyExplorer.dll")
else:
    clr.AddReference("RevitFamilyExplorer_{}.dll".format(HOST_APP.version))

import RevitFamilyExplorer


def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    # чтобы нормально работала панель,
    # она должна быть инициализированная заранее
    #RevitFamilyExplorer.RegisterFamilyExplorerCommand().Execute(__rvt__)
    pass


def open_family_explorer():
    #RevitFamilyExplorer.FamilyExplorerCommand().Execute(__revit__)
    pass


if __name__ == '__main__':
    open_family_explorer()