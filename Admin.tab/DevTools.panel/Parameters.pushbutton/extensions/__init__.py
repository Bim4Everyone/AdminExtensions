# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import *


def get_parameters(document):
    elements = FilteredElementCollector(document) \
        .WherePasses(LogicalOrFilter(ElementIsElementTypeFilter(False), ElementIsElementTypeFilter(True))) \
        .ToElements()

    params = [params for element in elements
              for params in element.GetOrderedParameters()]

    params = [param.GUID for param in params
              if param.IsShared]

    for family_document in get_families_documents(document):
        shared_params = FilteredElementCollector(family_document) \
            .OfClass(SharedParameterElement) \
            .WhereElementIsNotElementType() \
            .ToElements()

        params.extend([shared_param.GuidValue for shared_param in shared_params])

    return set(params)


def get_shared_parameters(document):
    shared_params = FilteredElementCollector(document) \
        .OfClass(SharedParameterElement) \
        .WhereElementIsNotElementType() \
        .ToElements()

    params = get_parameters(document)

    shared_params = [shared_param for shared_param in shared_params
                     if shared_param.GetDependentElements(None).Count == 1]

    return sorted([shared_param for shared_param in shared_params
                   if shared_param.GuidValue not in params],
                  key=lambda element: element.Name)


def get_families_documents(document):
    families = FilteredElementCollector(document) \
        .OfClass(Family) \
        .ToElements()

    return [document.EditFamily(family) for family in families if family.IsEditable]
