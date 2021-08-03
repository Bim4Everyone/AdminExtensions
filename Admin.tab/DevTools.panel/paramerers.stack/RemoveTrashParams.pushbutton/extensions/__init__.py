# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import *

def get_families_documents(document):
    families = FilteredElementCollector(document) \
        .OfClass(Family) \
        .ToElements()

    return [document.EditFamily(family) for family in families if family.IsEditable]


def get_shared_parameters(document):
    result = []

    for family_document in get_families_documents(document):
        if family_document.IsValidObject:
            shared_params = FilteredElementCollector(family_document) \
                .OfClass(SharedParameterElement) \
                .WhereElementIsNotElementType() \
                .ToElements()

            result.extend(list([shared_param.GuidValue for shared_param in shared_params]))
            family_document.Close(False)

    return result

def get_guid_parameters(document):
    elements = FilteredElementCollector(document) \
        .WherePasses(LogicalOrFilter(ElementIsElementTypeFilter(False), ElementIsElementTypeFilter(True))) \
        .ToElements()

    params = [params for element in elements
              for params in element.GetOrderedParameters()]

    params = [param.GUID for param in params
              if param.IsShared]

    params.extend(get_shared_parameters(document))

    return set(params)


def get_trash_parameters(document):
    shared_params = FilteredElementCollector(document) \
        .OfClass(SharedParameterElement) \
        .WhereElementIsNotElementType() \
        .ToElements()

    params = get_guid_parameters(document)

    shared_params = [shared_param for shared_param in shared_params
                     if shared_param.GetDependentElements(None).Count == 1]

    return sorted([shared_param for shared_param in shared_params
                   if shared_param.GuidValue not in params],
                  key=lambda element: element.Name)
