"""
:babelast:`` AST structures
"""

from jast.util import AST, DecorateMixin, \
    js_var, list_attr, ConvList, \
    AliasFactory, cls, attr, json, convert_as, \
    Factory, partial, is_list

def JS(val): #pylint: disable=invalid-name,too-many-return-statements
    """
    Automatically convert python object to Boolean, Numeric, String or Object representation.
    """
    if val is None:
        return None
    if isinstance(val, AST):
        return val
    if isinstance(val, bool):
        return Boolean(val)
    if isinstance(val, int):
        return Numeric(val)
    if isinstance(val, basestring):
        return String(val)
    if isinstance(val, dict):
        return Object(val.items())
    if is_list(val):
        return Array(val)
    raise ValueError("Cannot resolve %r to AST value" % val)


@cls
class Program(AST):
    """
    :babelast:`programs`
    """

    type = "Program"
    body = list_attr()
    sourceType = attr(default='module')
    interpreter = attr(default=None)
    directives = list_attr()

    ast_keys_order = ['sourceType', 'interpreter', 'body', 'directives']


@cls
class Identifier(AST):
    """
    :babelast:`identifier`
    """
    type = "Identifier"
    name = attr(converter=js_var, default=None)
    definition = attr(default=None)

    @staticmethod
    def auto(val, imp=None):
        """
        Automatically convert value as an AST :class:`.Identifier`
        """
        if hasattr(val, 'identifier'):
            return val.identifier()

        if isinstance(val, AST):
            return val

        if isinstance(val, basestring):
            if "." in val:
                prop = Identifier(val.split(".")[-1])
                obj = Identifier.auto(".".join(val.split(".")[:-1]))
                return Member(object=obj, prop=prop, definition=imp)
            return Identifier(val, definition=imp)

        return val

    def call(self, *args):
        """
        Convert to :class:`.Call` instance.
        """
        return Call(self, args)

    def member(self, arg):
        """
        Convert to :class:`.Member` instance.
        """
        return Member(object=self, prop=Id.auto(arg))


Id = Identifier


@cls
class Extra(AST):
    """
    :babelast:`extra`
    """
    rawValue = attr()
    raw = attr(converter=json.dumps, default=AliasFactory('rawValue'))


@cls
class String(AST):
    """
    :babelast:`string`
    """
    type = "StringLiteral"
    value = attr()
    extra = attr(default=AliasFactory('value'), converter=convert_as(Extra))


@cls
class Numeric(AST):
    """
    :babelast:`numeric`
    """
    type = "NumericLiteral"
    value = attr(converter=int)
    extra = attr(default=AliasFactory('value'), converter=convert_as(Extra))


@cls
class Boolean(AST):
    """
    :babelast:`boolean`
    """
    type = "BooleanLiteral"
    value = attr(converter=bool)


def _import_factory(imp):
    """
    :class:`.Import` specificers converter.
    """
    if is_list(imp):
        return map(ImportSpecifier, imp)
    return [ImportDefaultSpecifier(imp)]

@cls
class Import(AST):
    """
    :babelast:`importdeclaration`
    """
    type = "ImportDeclaration"

    fct = lambda x: x.source.value if hasattr(x, 'source') else None
    specifiers = attr(default=Factory(fct, takes_self=True),
                      converter=_import_factory)
    source = attr(default=None, converter=convert_as(String))

    def id(self, key=None): #pylint: disable=invalid-name
        """
        Shortcut to :py:meth:`.Import.identifier`
        """
        return self.identifier(key)

    def identifier(self, key=None):
        """
        Get import statement specifier as :class:`.Identifier`.
        """
        #pylint: disable=unsubscriptable-object,not-an-iterable
        _id = None
        if key is None:
            assert len(self.specifiers) == 1
            _id = self.specifiers[0].local
        for spec in self.specifiers:
            if spec.local.name == key:
                _id = spec.local
                break
        _id = Identifier.auto(_id.copy())
        _id.definition = self
        return _id


@cls
class ImportSpecifier(AST):
    """
    :babelast:`importspecifier`
    """
    type = "ImportSpecifier"

    imported = attr(converter=Identifier.auto)
    local = attr(default=Factory(lambda x: x.imported, takes_self=True))


def _import_fix(imp):
    auto = Identifier.auto(imp)
    if isinstance(auto, Member):
        return auto.object
    return auto

@cls
class ImportDefaultSpecifier(AST):
    """
    :babelast:`importdefaultspecifier`
    """
    type = "ImportDefaultSpecifier"

    local = attr(converter=_import_fix)


@cls
class ObjectProperty(AST):
    """
    :babelast:`objectproperty`
    """
    type = "ObjectProperty"

    key = attr(default=None, converter=Identifier.auto)
    value = attr(default=None, converter=JS)
    computed = attr(default=False)
    shorthand = attr(default=False)
    method = attr(default=False)

    ast_keys_order = ['type', 'method', 'key', 'computed', 'shorthand', 'value']


def _normalize_dict_to_list(value):
    val = value
    if isinstance(val, dict):
        val = [ObjectProperty(key, JS(v)) for key, v in val.items()]
    return ConvList(val, convert=convert_as(ObjectProperty,
                                            expand_args=True))

@cls
class Object(AST, dict):
    """
    :babelast:`object`
    """
    type = "ObjectExpression"

    properties = attr(converter=_normalize_dict_to_list, default=Factory(
        partial(ConvList,
                convert=convert_as(ObjectProperty, expand_args=True))))


    @property
    def properties_dict(self):
        """
        Convert a js Object to python dict
        """
        #pylint: disable=not-an-iterable
        return dict([(x.key.name, x) for x in self.properties])

    def _property_index(self, key):
        for index, prop in enumerate(self.properties):
            if prop.key == key:
                return index
        return None

    def __getitem__(self, key):
        val = self.properties_dict[key]
        while hasattr(val, 'value'):
            val = getattr(val, 'value')
        return val

    def __setitem__(self, key, value):
        #pylint: disable=unsupported-assignment-operation,no-member
        index = self._property_index(key)
        val = JS(value)
        if not isinstance(val, ObjectProperty):
            val = ObjectProperty(key, val)

        if index:
            self.properties[index] = val
        else:
            self.properties.append(val)

    def __delitem__(self, key):
        #pylint: disable=unsupported-delete-operation
        index = self._property_index(key)
        del self.properties[index]

    def __contains__(self, key):
        return bool(self._property_index(key))



@cls
class NullLiteral(AST):
    """
    :babelast:`nullliteral`
    """
    type = "NullLiteral"

Null = NullLiteral() #pylint: disable=invalid-name


def _normalize_array(val):
    if not is_list(val):
        return JS(val)
    return val

@cls
class Array(AST):
    """
    :babelast:`arrayexpression`
    """
    type = "ArrayExpression"

    elements = list_attr(converter=JS, normalize=_normalize_array)


@cls
class Member(AST):
    """
    :babelast:`memberexpression`
    """
    type = "MemberExpression"
    object = attr(converter=Identifier.auto)
    prop = attr(converter=Identifier.auto)
    computed = attr(default=False)
    definition = attr(default=None)

    ast_map = {
        'prop': 'property'
    }

    def call(self, *args):
        """
        Convert to member Call statement
        """
        return Call(self, args)

@cls
class Var(AST):
    """
    :babelast:`variabledeclaration`
    """
    type = "VariableDeclaration"
    declarations = list_attr()
    kind = attr(default="let")

    @staticmethod
    def simple(identifier, init):
        """
        Common VariableDeclarator AST factory
        """
        return Var(VariableDeclarator(identifier, JS(init)))


@cls
class VariableDeclarator(AST):
    """
    :babelast:`variabledeclarator`
    """
    type = "VariableDeclarator"
    id = attr(converter=Identifier.auto)
    init = attr()


@cls
class Expression(AST):
    """
    :babelast:`expressionstatement`
    """
    type = "ExpressionStatement"
    expression = attr()


@cls
class Block(AST):
    """
    :babelast:`blockstatement`
    """
    type = "BlockStatement"
    body = list_attr(converter=Expression.converter)
    directives = list_attr()


@cls
class Function(AST):
    """
    :babelast:`functionexpression`
    """
    type = "FunctionExpression"

    params = list_attr(converter=Identifier.auto)
    body = attr(default=Factory(Block), converter=Block.converter)
    id = attr(default=None)
    isAsync = attr(default=False)
    generator = attr(default=False)

    ast_map = {
        'isAsync': 'async'
    }


@cls
class NamedFunction(Function):
    """
    :babelast:`functiondeclaration`
    """
    type = "FunctionDeclaration"


@cls
class Call(AST):
    """
    :babelast:`callexpression`
    """
    type = "CallExpression"
    callee = attr(converter=Identifier.auto, default=None)
    arguments = list_attr(converter=JS, default=None)


@cls
class Decorator(AST):
    """
    :babelast:`decorator`
    """
    type = "Decorator"
    expression = attr(converter=JS)


@cls
class CallDecorator(AST):
    """
    :babelast:`decorator`
    """
    type = "Decorator"
    expression = attr(converter=Call.converter)


@cls
class ClassProperty(AST, DecorateMixin):
    """
    :babelast:`classproperty`
    """
    type = "ClassProperty"
    key = attr(converter=convert_as(Id), default=None)
    value = attr(converter=JS, default=None)
    computed = attr(default=False)
    static = attr(default=False)
    decorators = list_attr(converter=convert_as(Decorator))

    def as_method(self, **kwargs):
        """
        Convert class property to class method.
        """
        return ClassMethod(key=self.key, decorators=self.decorators, **kwargs)


@cls
class ClassMethod(AST, DecorateMixin):
    """
    :babelast:`classmethod`
    """
    type = "ClassMethod"
    key = attr(converter=Identifier.auto, default=None)
    params = list_attr(converter=Identifier.auto)
    body = attr(default=None, converter=Block.converter)
    decorators = list_attr(converter=Decorator.converter)
    kind = attr(default=None)
    static = attr(default=False)
    generator = attr(default=False)
    isAsync = attr(default=False)
    id = attr(default=None)
    directives = list_attr(default=[])

    def as_property(self, **kwargs):
        """
        Convert class method to value-less class property.
        """
        return ClassProperty(key=self.key, decorators=self.decorators, **kwargs)

    @classmethod
    def getter(_cls, key, body, **kwargs): #pylint: disable=bad-classmethod-argument
        """
        Getter factory
        """
        kwargs['kind'] = 'get'
        return _cls(key, [], body, **kwargs)

    @classmethod
    def setter(_cls, key, body, **kwargs): #pylint: disable=bad-classmethod-argument
        """
        Setter factory
        """
        return _cls(key, [Id('val')], body, **kwargs)



@cls
class ClassBody(AST):
    """
    :babelast:`classbody`
    """
    type = "ClassBody"
    body = list_attr()


@cls
class Return(AST):
    """
    :babelast:`returnstatement`
    """
    type = "ReturnStatement"
    argument = attr(default=None)


@cls
class This(AST):
    """
    :babelast:`thisexpression`
    """
    type = "ThisExpression"

    def member(self, arg):
        """
        Get a member identifier
        """
        return Member(object=self, prop=Id.auto(arg))

This = This() #pylint: disable=invalid-name


@cls
class Class(AST):
    """
    :babelast:`classdeclaration`
    """
    type = "ClassDeclaration"
    id = attr(converter=Identifier.auto, default=None)
    superClass = attr(converter=Identifier.auto, default=None)
    body = attr(converter=convert_as(ClassBody),
                default=Factory(ClassBody))

    def add_property(self, key, val, decorators=None):
        """
        Append a property to class object
        """
        #pylint: disable=no-member
        decorators = decorators or []
        self.body.body.append(ClassProperty(key, val, decorators=decorators))


@cls
class ExportDefault(AST):
    """
    :babelast:`exportdefaultdeclaration`
    """
    type = "ExportDefaultDeclaration"
    declaration = attr(converter=convert_as(Identifier))
