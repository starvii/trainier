#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class Constant(object):
    class ConstError(PermissionError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError( "Can't rebind const({})".format(name))
        self.__dict__[name] = value


    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError("Can't unbind const({})".format(name))
        raise NameError(name)

sys.modules[__name__] = Constant()
