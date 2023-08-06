import dataclasses
import sys
import typing

from mypy_extensions import _check_fails, _dict_new  # type: ignore


@dataclasses.dataclass(eq=True, frozen=True)
class Key(object):
    name: str
    required: bool = True


def _key_typeddict_new(cls, _typename, _fields=None, **kwargs):
    total = kwargs.pop('total', True)
    if _fields is None:
        _fields = kwargs
    elif kwargs:
        raise TypeError("TypedDict takes either a dict or keyword arguments,"
                        " but not both")
    return _KeyTypedDictMeta(_typename, (), {'__annotations__': dict(_fields),
                                                  '__total__': total})


class _KeyTypedDictMeta(type):
    def __new__(cls, name, bases, ns, total=True, allow_extra=False):
        # Create new typed dict class object.
        # This method is called directly when TypedDict is subclassed,
        # or via _typeddict_new when TypedDict is instantiated. This way
        # TypedDict supports all three syntaxes described in its docstring.
        # Subclasses and instances of TypedDict return actual dictionaries
        # via _dict_new.
        ns['__new__'] = _key_typeddict_new if name == 'KeyTypedDict' else _dict_new
        tp_dict = super(_KeyTypedDictMeta, cls).__new__(cls, name, (dict,), ns)
        try:
            # Setting correct module is necessary to make typed dict classes pickleable.
            tp_dict.__module__ = sys._getframe(2).f_globals.get('__name__', '__main__')
        except (AttributeError, ValueError):
            pass
        anns = ns.get('__annotations__', {})
        msg = "KeyTypedDict('Name', {f0: t0, f1: t1, ...}); each t must be a type"
        anns = {n: typing._type_check(tp, msg) for n, tp in anns.items()}
        for base in bases:
            anns.update(base.__dict__.get('__annotations__', {}))
        tp_dict.__annotations__ = anns
        if not hasattr(tp_dict, '__total__'):
            tp_dict.__total__ = total
        if not hasattr(tp_dict, '__allow_extra__'):
            tp_dict.__allow_extra__ = allow_extra
        return tp_dict

    __instancecheck__ = __subclasscheck__ = _check_fails


KeyTypedDict = _KeyTypedDictMeta('KeyTypedDict', (dict,), {})
KeyTypedDict.__module__ = __name__
