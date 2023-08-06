#
# Copyright 2008-2018 Universidad Complutense de Madrid
#
# This file is part of Numina
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

import inspect

from numina.util.parser import parse_arg_line
from numina.exceptions import NoResultFound
from numina.datamodel import DataModel


class DataTypeBase(object):
    """Base class for input/output types of recipes.

    """
    def __init__(self, *args, **kwds):
        import numina.core.tagexpr as tagexpr

        datamodel = kwds.get('datamodel')

        if datamodel is not None:
            if inspect.isclass(datamodel):
                self.datamodel = datamodel()
            else:
                self.datamodel = datamodel
        else:
            self.datamodel = DataModel()

        my_tag_table = self.datamodel.query_attrs
        self.query_expr = tagexpr.ConstExprTrue

        if hasattr(self, '__tags__'):
            # FIXME:
            if isinstance(self.__tags__, list):
                objtags = [my_tag_table[t] for t in self.__tags__]
            elif isinstance(self.__tags__, dict):
                objtags = [t for t in self.__tags__.values()]
            else:
                raise TypeError('type not supported in tags')

            self.query_expr = tagexpr.query_expr_from_attr(objtags)
        if 'query_expr' in kwds:
            self.query_expr = kwds['query_expr']

        if 'tags' in kwds:
            # Create expresion from tags
            objtags = [my_tag_table[t] for t in kwds['tags']]
            self.query_expr = tagexpr.query_expr_from_attr(objtags)

        self.names_t = self.query_expr.tags()
        self.names_f = self.query_expr.fields()
        self.query_opts = []

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        pass

    def _datatype_dump(self, obj, where):
        return obj

    def _datatype_load(self, obj):
        return obj

    def query(self, name, dal, obsres, options=None):
        from numina.core.query import ResultOf
        try:
            return self.query_on_ob(name, obsres)
        except NoResultFound:
            pass

        if isinstance(options, ResultOf):
            value = dal.search_result_relative(name, self, obsres,
                                               result_desc=options)
            return value.content

        if self.isproduct():
            # if not, the normal query
            prod = dal.search_product(name, self, obsres)
            return prod.content
        else:
            param = dal.search_parameter(name, self, obsres)
            return param.content

    def query_on_ob(self, key, ob):
        # First check if the requirement is embedded
        # in the observation result
        # It can in ob.requirements
        # or directly in the structure (as in GTC)
        if key in ob.requirements:
            content = ob.requirements[key]
            value = self._datatype_load(content)
            return value
        try:
            return getattr(ob, key)
        except AttributeError:
            raise NoResultFound("DataType.query_on_ob")

    def on_query_not_found(self, notfound):
        pass

    def query_constraints(self):
        from numina.core.query import Constraint
        return Constraint()

    @classmethod
    def isproduct(cls):
        """Check if the DataType is the product of a Recipe"""
        return False

    def __repr__(self):
        sclass = type(self).__name__
        return "%s()" % (sclass, )

    def name(self):
        """Unique name of the datatype"""
        return self.__repr__()

    @classmethod
    def from_name(cls, name):
        # name is in the form Class(arg1=val1, arg2=val2)
        # find first (
        fp = name.find('(')
        sp = name.find(')')
        if (fp == -1) or (sp == -1) or (sp < fp):
            # paren not found
            klass = name
            kwargs = {}
        else:
            # parse things between parens
            klass = name[:fp]
            fargs = name[fp+1:sp]
            kwargs = parse_arg_line(fargs)

        if klass == cls.__name__:
            # create thing
            obj = cls.__new__(cls)
            obj.__init__(**kwargs)

            return obj
        else:
            raise TypeError(name)

    @staticmethod
    def create_db_info():
        """Create metadata structure"""
        result = {}
        result['instrument'] = ''
        result['uuid'] = ''
        result['tags'] = {}
        result['type'] = ''
        result['mode'] = ''
        result['observation_date'] = ""
        result['origin'] = {}
        return result

    def extract_db_info(self, obj, db_info_keys):
        """Extract metadata from serialized file"""
        result = self.create_db_info()
        return result

    def update_meta_info(self):
        """Extract my metadata"""
        result = self.create_db_info()
        return result

    def tag_names(self):
        return self.names_t
