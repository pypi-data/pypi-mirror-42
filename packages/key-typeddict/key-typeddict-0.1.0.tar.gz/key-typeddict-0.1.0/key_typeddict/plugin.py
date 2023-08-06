from collections import OrderedDict
from typing import Callable, List, Optional, Set, Tuple, cast

from mypy import message_registry
from mypy.checkexpr import ExpressionChecker
from mypy.exprtotype import expr_to_unanalyzed_type
from mypy.nodes import CallExpr, Context, DictExpr, Expression, GDEF, NameExpr, StrExpr, SymbolTableNode
from mypy.plugin import DynamicClassDefContext, Plugin
from mypy.semanal import SemanticAnalyzerPass2
from mypy.semanal_typeddict import TypedDictAnalyzer
from mypy.types import AnyType, Instance, Type, TypeOfAny, TypedDictType


class UnsupportedKeyTypeError(ValueError):
    pass


def parse_key_typeddict_fields(attrs_expr: DictExpr) -> Tuple[List[str], List[Type], Set[str]]:
    fields = []
    types = []
    required_fields = set()
    for field_name_expr, field_type_expr in attrs_expr.items:
        if isinstance(field_name_expr, StrExpr):
            fields.append(field_name_expr.value)
            required_fields.add(field_name_expr.value)

        elif isinstance(field_name_expr, CallExpr):
            fields.append(field_name_expr.args[0].value)
            required_expr = field_name_expr.args[1] if len(field_name_expr.args) == 2 else NameExpr('builtins.True')
            if required_expr.fullname == 'builtins.True':
                required_fields.add(field_name_expr.args[0].value)

        else:
            raise UnsupportedKeyTypeError(str(type(field_name_expr)))
        types.append(expr_to_unanalyzed_type(field_type_expr))

    return fields, types, required_fields


def check_typeddict_call_with_kwargs(self,
                                     callee: TypedDictType,
                                     kwargs: 'OrderedDict[str, Expression]',
                                     context: Context) -> Type:
    if not getattr(callee, 'allow_extra', False):
        if not (callee.required_keys <= set(kwargs.keys()) <= set(callee.items.keys())):
            expected_keys = [key for key in callee.items.keys()
                             if key in callee.required_keys or key in kwargs.keys()]
            actual_keys = kwargs.keys()
            self.msg.unexpected_typeddict_keys(
                callee,
                expected_keys=expected_keys,
                actual_keys=list(actual_keys),
                context=context)
            return AnyType(TypeOfAny.from_error)

    for (item_name, item_expected_type) in callee.items.items():
        if item_name in kwargs:
            item_value = kwargs[item_name]
            self.chk.check_simple_assignment(
                lvalue_type=item_expected_type, rvalue=item_value, context=item_value,
                msg=message_registry.INCOMPATIBLE_TYPES,
                lvalue_name='TypedDict item "{}"'.format(item_name),
                rvalue_name='expression')

    return callee


def copy_modified(self, *, fallback: Optional[Instance] = None,
                  item_types: Optional[List[Type]] = None,
                  required_keys: Optional[Set[str]] = None) -> 'TypedDictType':
    if fallback is None:
        fallback = self.fallback
    if item_types is None:
        items = self.items
    else:
        items = OrderedDict(zip(self.items, item_types))
    if required_keys is None:
        required_keys = self.required_keys

    new_type = TypedDictType(items, required_keys, fallback, self.line, self.column)
    new_type.allow_extra = getattr(self, 'allow_extra', False)
    return new_type


ExpressionChecker.check_typeddict_call_with_kwargs = check_typeddict_call_with_kwargs
TypedDictType.copy_modified = copy_modified


def add_key_typeddict_to_global_symboltable(ctx: DynamicClassDefContext) -> None:
    api = cast(SemanticAnalyzerPass2, ctx.api)
    typeddict_analyzer = TypedDictAnalyzer(options=api.options,
                                           api=api,
                                           msg=api.msg)
    try:
        fields, types, required_fields = parse_key_typeddict_fields(ctx.call.args[1])
    except UnsupportedKeyTypeError as error:
        api.fail(f'Unsupported key type {error.args[0]}', ctx=ctx.call)

    info = typeddict_analyzer.build_typeddict_typeinfo(ctx.name,
                                                       items=fields,
                                                       types=types,
                                                       required_keys=required_fields)
    allow_extra = api.parse_bool(ctx.call.args[2]) if len(ctx.call.args) > 2 else False
    info.typeddict_type.allow_extra = allow_extra
    api.add_symbol_table_node(ctx.name,
                              SymbolTableNode(GDEF, info))


class KeyTypedDictPlugin(Plugin):
    def get_dynamic_class_hook(self, fullname: str
                               ) -> Optional[Callable[[DynamicClassDefContext], None]]:
        if fullname == 'key_typeddict.core.KeyTypedDict':
            return add_key_typeddict_to_global_symboltable
        return None


def plugin(version):
    return KeyTypedDictPlugin
