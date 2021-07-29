# -*- coding: utf-8 -*-

from extensions import *
from Autodesk.Revit.DB import *

document = __revit__.ActiveUIDocument.Document


def remove_parameters():
    shared_params = get_trash_parameters(document)

    with Transaction(document) as transaction:
        transaction.Start("Удаление параметров")

        for shared_param in shared_params:
            try:
                print str(shared_param.GuidValue) + " - " + str(
                    shared_param.Id.IntegerValue) + " - " + shared_param.Name

                document.Delete(shared_param.Id)
            except Exception as ex:
                print str(ex)

        transaction.Commit()


remove_parameters()
