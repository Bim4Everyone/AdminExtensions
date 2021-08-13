# -*- coding: utf-8 -*-
import clr
clr.AddReference("dosymep.Bim4Everyone.dll")

import os
import sys
import traceback

from dosymep.Bim4Everyone import ModuleEnvironment

appdata = os.getenv('APPDATA')

def __print_message(result, test_name, ex=None, tb=None):
    str_ex = ""
    if ex:
        str_ex = "\r\n" + "\r\n".join(traceback.format_exception(type(ex), ex, tb))

    print (":heavy_check_mark:" if result else ":heavy_multiplication_x:") + " " + test_name + str_ex


def testing(test_name=None):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                result = function(*args, **kwargs)
                __print_message(result, test_name if test_name else function.__name__)
            except Exception:
                result = False
                ex_type, ex, tb = sys.exc_info()
                __print_message(result, test_name if test_name else function.__name__, ex, tb)

        return wrapper

    return decorator


@testing()
def test_CurrentLibraryPath():
    return ModuleEnvironment.CurrentLibraryPath == os.path.join(appdata, r"pyRevit\Extensions\BIM4Everyone.lib")


@testing()
def test_TemplatesPath():
    return ModuleEnvironment.TemplatesPath == os.path.join(appdata, r"pyRevit\Extensions\BIM4Everyone.lib\templates")


@testing()
def test_EmptyTemplatePath():
    return ModuleEnvironment.EmptyTemplatePath == os.path.join(appdata,
                                                               r"pyRevit\Extensions\BIM4Everyone.lib\templates\empty_project.rte")


@testing()
def test_ParametersTemplatePath():
    return ModuleEnvironment.ParametersTemplatePath == os.path.join(appdata,
                                                                    r"pyRevit\Extensions\BIM4Everyone.lib\templates\project_parameters.rvt")

@testing()
def test_Exception():
    raise ValueError("ssss")


test_Exception()
test_Exception()
test_CurrentLibraryPath()
test_TemplatesPath()
test_EmptyTemplatePath()
test_ParametersTemplatePath()
