"""
`jast` custom AST structures
"""
from jast.util import list_attr, cls, convert_as, attr, json
from jast.babel import AST, ExportDefault, Program


@cls
class Code(AST):
    """
    Custom AST type to represent a string of raw javascript code.
    """
    type = "Code"
    code = attr()


@cls
class File(AST):
    """
    Custom jast AST helper structure.
    """
    name = attr()
    body = list_attr()
    export = attr(default=None, converter=convert_as(ExportDefault))
    imports = list_attr()
    header = list_attr()

    def ast(self):
        #pylint: disable=not-an-iterable,no-member
        prog = Program()
        for imp in self.imports:
            prog.body.append(imp)
        for header in self.header:
            prog.body.append(header)
        for stm in self.body:
            prog.body.append(stm)

        export_converter = convert_as(ExportDefault)
        self.export = export_converter(self.export)
        if self.export and self.export.declaration.name:
            prog.body.append(self.export)

        ast, defs = prog.ast_defs()
        imports = [x.get('type') == 'ImportDeclaration' for x in defs]
        other = [x.get('type') != 'ImportDeclaration' for x in  defs]

        for decl in other:
            ast['body'].insert(0, decl)

        imported = []
        imports.reverse()
        for decl in imports:
            key = json.dumps(decl)
            if key in imported:
                continue
            imported.append(key)
            ast['body'].insert(0, decl)

        # collect identifiers imports
        return {
            "type": "File",
            "program": ast
        }
