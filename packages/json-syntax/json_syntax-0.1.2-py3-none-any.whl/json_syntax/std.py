from .helpers import (
    has_origin,
    get_origin,
    issub_safe,
    NoneType,
    JP,
    J2P,
    P2J,
    IJ,
    IP,
    II,
    JPI,
)
from .action_v1 import (
    check_collection,
    check_float,
    check_isinst,
    check_has_type,
    check_mapping,
    check_optional,
    check_parse_error,
    check_str_enum,
    convert_collection,
    convert_date,
    convert_datetime,
    convert_enum_str,
    convert_float,
    convert_mapping,
    convert_none,
    convert_optional,
    convert_str_enum,
    convert_time,
)

from collections import OrderedDict
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from functools import partial
from typing import Union

"""
These are standard rules to handle various types.

All rules take a verb, a Python type and a context, which is generally a RuleSet. A rule
returns a conversion function for that verb.
"""


def atoms(verb, typ, ctx):
    "Rule to handle atoms on both sides."
    if issub_safe(typ, (str, int, NoneType)):
        if verb in JP:
            if typ is NoneType:
                return convert_none
            for base in (str, bool, int):
                if issubclass(typ, base):
                    return base
        elif verb == IP:
            for base in (NoneType, str, bool, int):
                if issubclass(typ, base):
                    return partial(check_isinst, typ=base)
        elif verb == IJ:
            for base in (NoneType, str, bool, int):
                if issubclass(typ, base):
                    return partial(check_isinst, typ=base)


def floats(verb, typ, ctx):
    """
    Rule to handle floats passing NaNs through unaltered.

    JSON technically recognizes integers and floats. Many JSON generators will represent floats with integral value as integers.
    Thus, this rule will convert both integers and floats in JSON to floats in Python.

    Python's standard JSON libraries treat `nan` and `inf` as special constants, but this is not standard JSON.

    This rule simply treats them as regular float values. If you want to catch them, you can set ``allow_nan=False``
    in ``json.dump()``.
    """
    if issub_safe(typ, float):
        if verb in JP:
            return float
        elif verb == IP:
            return partial(check_isinst, typ=float)
        elif verb == IJ:
            return partial(check_isinst, typ=(int, float))


def floats_nan_str(verb, typ, ctx):
    """
    Rule to handle floats passing NaNs through as strings.

    Python's standard JSON libraries treat `nan` and `inf` as special constants, but this is not standard JSON.

    This rule converts special constants to string names.
    """
    if issub_safe(typ, float):
        if verb == J2P:
            return float
        elif verb == P2J:
            return convert_float
        elif verb == IP:
            return partial(check_isinst, typ=float)
        elif verb == IJ:
            return check_float


def decimals(verb, typ, ctx):
    """
    Rule to handle decimals natively.

    This rule requires that your JSON library has decimal support, e.g. simplejson.

    Other JSON processors may convert values to and from floating-point; if that's a concern, consider `decimals_as_str`.

    This rule will fail if passed a special constant.
    """
    if issub_safe(typ, Decimal):
        if verb in JP:
            return Decimal
        elif verb in II:
            return partial(check_isinst, typ=Decimal)


def decimals_as_str(verb, typ, ctx):
    """
    Rule to handle decimals as strings.

    This rule bypasses JSON library decimal support, e.g. simplejson.

    This rule will fail if passed a special constant.
    """
    if issub_safe(typ, Decimal):
        if verb == J2P:
            return Decimal
        elif verb == P2J:
            return str
        elif verb == IP:
            return partial(check_isinst, typ=Decimal)
        elif verb == IJ:
            return partial(check_parse_error, parser=Decimal, error=ArithmeticError)


def iso_dates(verb, typ, ctx):
    """
    Rule to handle iso formatted datetimes and dates.

    This is the strict variant that simply uses the `fromisoformat` and `isoformat` methods of `date` and `datetime`.

    There is a loose variant in the examples that will accept a datetime in a date. A datetime always accepts both
    dates and datetimes.
    """
    if typ not in (date, datetime, time):
        return
    if verb == P2J:
        return typ.isoformat
    elif verb == IP:
        return partial(check_has_type, typ=typ)
    elif verb in (J2P, IJ):
        if typ == date:
            parse = convert_date
        elif typ == datetime:
            parse = convert_datetime
        elif typ == time:
            parse = convert_time
        else:
            return
        if verb == J2P:
            return parse
        else:
            return partial(
                check_parse_error, parser=parse, error=(TypeError, ValueError)
            )


def enums(verb, typ, ctx):
    "Rule to convert between enumerated types and strings."
    if issub_safe(typ, Enum):
        if verb == P2J:
            return convert_enum_str
        elif verb == J2P:
            return partial(convert_str_enum, mapping=dict(typ.__members__))
        elif verb == IP:
            return partial(check_isinst, typ=typ)
        elif verb == IJ:
            return partial(check_str_enum, mapping=frozenset(typ.__members__.keys()))


def faux_enums(verb, typ, ctx):
    "Rule to fake an Enum by actually using strings."
    if issub_safe(typ, Enum):
        if verb in JP:
            mapping = {name: name for name in typ.__members__}
            return partial(convert_str_enum, mapping=mapping)
        elif verb in II:
            return partial(check_str_enum, mapping=frozenset(typ.__members__.keys()))


def optional(verb, typ, ctx):
    """
    Handle an ``Optional[inner]`` by passing ``None`` through.
    """
    if verb not in JPI:
        return
    if has_origin(typ, Union, num_args=2):
        if NoneType not in typ.__args__:
            return
        inner = None
        for arg in typ.__args__:
            if arg is not NoneType:
                inner = arg
        if inner is None:
            raise TypeError("Could not find inner type for Optional: " + str(typ))
    else:
        return
    inner = ctx.lookup(verb=verb, typ=inner)
    if verb in JP:
        return partial(convert_optional, inner=inner)
    elif verb in II:
        return partial(check_optional, inner=inner)


def lists(verb, typ, ctx):
    """
    Handle a ``List[type]`` or ``Tuple[type, ...]``.

    Trivia: the ellipsis indicates a homogenous tuple; ``Tuple[A, B, C]`` is a product
    type that contains exactly those elements.
    """
    if verb not in JPI:
        return
    if has_origin(typ, list, num_args=1):
        (inner,) = typ.__args__
    elif has_origin(typ, tuple, num_args=2):
        (inner, ell) = typ.__args__
        if ell is not Ellipsis:
            return
    else:
        return
    inner = ctx.lookup(verb=verb, typ=inner)
    con = list if verb in (P2J, IJ) else get_origin(typ)
    if verb in JP:
        return partial(convert_collection, inner=inner, con=con)
    elif verb in II:
        return partial(check_collection, inner=inner, con=con)


def sets(verb, typ, ctx):
    """
    Handle a ``Set[type]`` or ``FrozenSet[type]``.
    """
    if verb not in JPI:
        return
    if not has_origin(typ, (set, frozenset), num_args=1):
        return
    (inner,) = typ.__args__
    con = list if verb in (P2J, IJ) else get_origin(typ)
    inner = ctx.lookup(verb=verb, typ=inner)
    if verb in JP:
        return partial(convert_collection, inner=inner, con=con)
    elif verb in II:
        return partial(check_collection, inner=inner, con=con)


def _stringly(verb, typ, ctx):
    """
    Rule to handle types that reliably convert directly to strings.

    This is used internally by dicts.
    """
    if verb not in JPI or not issub_safe(typ, (int, str, date, Enum)):
        return
    for base in str, int:
        if issubclass(typ, base):
            if verb in JP:
                return base
            elif verb in II:
                return partial(check_isinst, typ=base)
    for rule in enums, iso_dates:
        action = rule(verb=verb, typ=typ, ctx=ctx)
        if action is not None:
            return action


def dicts(verb, typ, ctx):
    """
    Handle a ``Dict[key, value]`` where key is a string, integer or enum type.
    """
    if verb not in JPI:
        return
    if not has_origin(typ, (dict, OrderedDict), num_args=2):
        return
    (key_type, val_type) = typ.__args__
    key_type = _stringly(verb=verb, typ=key_type, ctx=ctx)
    if key_type is None:
        return
    val_type = ctx.lookup(verb=verb, typ=val_type)
    if verb in JP:
        return partial(convert_mapping, key=key_type, val=val_type, con=get_origin(typ))
    elif verb in II:
        return partial(check_mapping, key=key_type, val=val_type, con=get_origin(typ))
