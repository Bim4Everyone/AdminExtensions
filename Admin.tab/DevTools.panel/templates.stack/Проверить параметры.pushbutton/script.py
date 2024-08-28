# -*- coding: utf-8 -*-

import clr

clr.AddReference("dosymep.Revit.dll")
clr.AddReference("dosymep.Bim4Everyone.dll")

import dosymep

clr.ImportExtensions(dosymep.Revit)
clr.ImportExtensions(dosymep.Bim4Everyone)

from pyrevit import forms
from pyrevit import EXEC_PARAMS, HOST_APP

from dosymep.Revit import *
from dosymep.Bim4Everyone import *
from dosymep.Bim4Everyone.SharedParams import *
from dosymep.Bim4Everyone.ProjectParams import *

from dosymep_libs.bim4everyone import *

from Autodesk.Revit.DB import *


@notification()
@log_plugin(EXEC_PARAMS.command_name)
def script_execute(plugin_logger):
    users = ["biseuv_o", "tikhomirov_amgvxad", "tikhomirov_am"]
    if __revit__.Application.Username.lower() not in users:
        script.exit()

    __revit__.OpenAndActivateDocument(ModuleEnvironment.ParametersTemplatePath)

    doc = __revit__.ActiveUIDocument.Document  # type: Document

    shared_params = SharedParamsConfig.Instance.GetRevitParams()
    project_params = ProjectParamsConfig.Instance.GetRevitParams()

    params = []
    params.extend(shared_params)
    params.extend(project_params)

    for param in params:
        param_element = param.GetRevitParamElement(doc)

        if param_element is None:
            print "Param element non found {}".format(param.Id)
            continue

        if param_element.Name != param.Name:
            print "Name non equal {}".format(param.Id)

        if isinstance(param_element, SharedParameterElement):
            if param_element.GuidValue != param.Guid:
                print "Guid non equal {}".format(param.Id)

        if param_element.GetStorageType() != param.StorageType:
            print "StorageType non equal {}".format(param.Id)

        definition = param_element.GetDefinition()

        if HOST_APP.is_exactly(2020):
            if definition.UnitType != param.UnitType:
                print "UnitType non equal {}".format(param.Id)
        elif HOST_APP.is_exactly(2021):
            if definition.GetSpecTypeId() != param.UnitType:
                print "UnitType non equal {}".format(param.Id)
        else:
            if definition.GetDataType() != param.UnitType:
                print "UnitType non equal {}".format(param.Id)


script_execute()
