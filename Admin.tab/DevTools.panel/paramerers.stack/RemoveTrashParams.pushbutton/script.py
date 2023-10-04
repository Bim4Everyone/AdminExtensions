# -*- coding: utf-8 -*-

import clr

clr.AddReference("dosymep.Revit.dll")
clr.AddReference("dosymep.Bim4Everyone.dll")

from extensions import *
from Autodesk.Revit.DB import *

import dosymep
clr.ImportExtensions(dosymep.Revit)
clr.ImportExtensions(dosymep.Bim4Everyone)

document = __revit__.ActiveUIDocument.Document


def remove_parameters():
    shared_params = get_trash_parameters(document)

    with Transaction(document) as transaction:
        transaction.Start("Удаление параметров")

        for shared_param in shared_params:
            try:
                print str(shared_param.GuidValue) + " - " + str(
                    shared_param.Id.GetIdValue()) + " - " + shared_param.Name

                document.Delete(shared_param.Id)
            except Exception as ex:
                print str(ex)

        transaction.Commit()

remove_parameters()
