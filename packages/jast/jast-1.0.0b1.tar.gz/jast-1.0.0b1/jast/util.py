"""
`jast` utility methods
"""
import json
import copy

from types import GeneratorType
from functools import partial

from collections import OrderedDict
from cattr import Converter

from inflection import camelize as camelize, underscore
from attr import s as cls, ib as attr, Factory


class classproperty(object): #pylint: disable=invalid-name,too-few-public-methods
    """
    SO development ftw, https://stackoverflow.com/a/3203659
    """
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


def is_list(val):
    """
    Iterable type inspection
    """
    list_types = [list, set, tuple, GeneratorType]
    return any([isinstance(val, x) for x in list_types])


def list_or_list(value):
    """
    Enforce list result
    """
    if is_list(value):
        return value
    return [value]


def is_string(val):
    """
    String type inspection
    """
    return isinstance(val, basestring)


class AliasFactory(Factory): #pylint: disable=too-few-public-methods
    """
    Generate a takes_self=True factory which returns a
    local attribute as factory predicate
    """
    def __init__(self, key, **kwargs):
        _factory = lambda x: getattr(x, key)
        takes_self = kwargs.pop('takes_self', True)
        super(AliasFactory, self).__init__(_factory, takes_self)


class ASTList(list):
    """
    :class:`.AST` mixin that produces list ast results
    by iterating local object.
    """
    def ast(self):
        """
        Return js AST representation
        """
        return [x.ast() for x in self]


class ConvList(ASTList):
    """
    :class:`.ASTList` object which additionally aplies converter to
    list items.
    """
    def __init__(self, items=None, convert=None):
        identity = lambda x: x
        self.convert = convert or identity
        items = items or []
        if not is_list(items):
            items = [items]

        items = list(items)
        items = map(self.convert, items)
        super(ConvList, self).__init__(items)

    def extend(self, arr):
        """
        Convert and delegate to list object
        """
        return list.append(self, map(self.convert, arr))

    def append(self, value):
        """
        Convert and delegate to list object
        """
        return list.append(self, self.convert(value))

    def insert(self, index, value):
        """
        Convert and delegate to list object
        """
        return list.insert(self, index, self.convert(value))

    def __setitem__(self, index, value):
        """
        Convert and delegate to list object
        """
        return list.__setitem__(self, index, self.convert(value))

    @classmethod
    def converter(_cls, _type): #pylint: disable=bad-classmethod-argument
        """
        Expose as attribute converter
        """
        return partial(ConvList, convert=_type)


def convert_as(_type, expand_args=False):
    """
    Generate a converter the provided AST class.
    """
    def _converter(value):
        """
        Introspects attribute value type to prevent double conversion.
        """
        if isinstance(value, _type):
            return value
        if expand_args:
            return _type(*value)
        return _type(value)
    return _converter


def list_attr(*args, **kwargs):
    """
    Declares :class:`.AST` object attribute as :class:`.ConvList`
    """
    convert = kwargs.get('converter', lambda x: x)
    factory = partial(ConvList, *args, convert=convert)
    return attr(default=Factory(factory), converter=factory)


def js_var(name, camelize_first=False):
    """
    Common :class:`.Identifier` converter.
    """
    if isinstance(name, basestring):
        from jast.babel import Identifier #pylint: disable=cyclic-import
        if '.' in name:
            return Identifier.auto(name)
        elif '-' in name:
            return camelize(underscore(name),
                            uppercase_first_letter=camelize_first)
        elif camelize_first:
            return camelize(name)
    return name


class _ASTConverter(Converter):
    """
    :class:`cattr.Converter` which applies a bit of ast magic.
    """
    def unstructure_attrs_asdict(self, obj):
        attrs = super(_ASTConverter, self).unstructure_attrs_asdict(obj)

        if hasattr(obj, 'ast_map'):
            mapping = obj.ast_map
            for key, val in mapping.items():
                attrs[val] = attrs[key]
                del attrs[key]
        if hasattr(obj, 'type'):
            attrs['type'] = obj.type
        if hasattr(obj, 'extra_ast_attrs'):
            extra = obj.extra_ast_attrs
            dispatch = self._unstructure_func.dispatch
            for name in extra:
                var = getattr(obj, name)
                attrs[name] = dispatch(var)(var)
        ordering = {'type': -100}
        attrs_order_map = getattr(obj, 'ast_keys_order',
                                  [x.name for x in obj.__attrs_attrs__])
        ordering.update(dict([(x, attrs_order_map.index(x)) for x in attrs_order_map]))
        ordered_items = sorted(attrs.items(), key=lambda x: ordering.get(x[0], 1))
        return OrderedDict(ordered_items)


@cls
class AST(object):
    """
    Base of all AST structure classes.
    """

    @classproperty
    def converter(self):
        """
        Expose a converter for the underlying AST structure.
        """
        return convert_as(self)

    def copy(self):
        """
        Make a clone of current AST instance.
        """
        return copy.deepcopy(self)

    @staticmethod
    def collect_definitions(ast):
        """
        Walk through AST structure and collect identifier definition entries. Expose
        them as AST :class:`.Import` statements.
        """
        imports = []
        ast = copy.deepcopy(ast)
        if not ast:
            return ast, imports

        if isinstance(ast, list):
            for i, value in enumerate(ast):
                val, _imp = AST.collect_definitions(value)
                ast[i] = val
                imports += _imp

        if isinstance(ast, dict):
            for key, value in ast.items():
                val, _imp = AST.collect_definitions(value)
                ast[key] = val
                imports += _imp

            if 'type' in ast and ast.get('type') in ['Identifier', 'MemberExpression']:
                if ast.get('definition'):
                    imports.append(ast.get('definition'))
                if 'definition' in ast:
                    del ast['definition']
        return ast, imports

    def ast(self):
        """
        Expose current AST instance to AST representation (dict or list).
        """
        converter = _ASTConverter()
        data = converter.unstructure(self)
        return data

    def ast_defs(self):
        """
        Helper methods to parse current AST instance as ast/imports tuple.
        """
        return AST.collect_definitions(self.ast())

    def json(self):
        """
        JSON representation of underlying AST instance
        """
        ast, _ = AST.collect_definitions(self.ast())
        return json.dumps(ast, indent=4)

    def to_dict(self):
        return json.loads(self.json())

    def json_defs(self):
        """
        JSON representation of :class:`.Import` statements related to current AST instance.
        """
        ast, imports = AST.collect_definitions(self.ast())
        return json.dumps(imports, indent=4), json.dumps(ast, indent=4)

    @classmethod
    def partial(_cls, *args, **kwargs): #pylint: disable=bad-classmethod-argument
        """
        Helper util to expose current AST structure as a partial constructor.
        """
        return partial(cls, *args, **kwargs)


@cls #pylint: disable=too-few-public-methods
class DecorateMixin(object):
    """
    AST mixin for structrures which can decorate other AST instances.
    """

    def decorate(self, item):
        """
        Expose current AST instance as a decorator
        """
        from jast.babel import Decorator #pylint: disable=cyclic-import

        decorator = self
        if not isinstance(decorator, Decorator):
            decorator = Decorator(self)
        assert hasattr(item, 'decorators')
        item.decorators.append(decorator)
        return self


def parse_module(mod):
    """
    Collect AST objects from a python module
    """
    keys = dir(mod)
    assert 'AST' in keys
    asts = getattr(mod, 'AST')
    if type(asts) != dict:
        asts = {
            mod.__name__: asts
        }
    return asts

def batch(*files):
    """
    Expose a set of :class:`jast.custom.File` objects into a grouped json ast structure.
    """
    data = {}
    for astfile in files:
        data[astfile.name] = astfile.ast()
    return json.dumps(data, indent=4)
