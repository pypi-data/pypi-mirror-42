from typing import Callable, Optional, TypeVar

import django

Args = TypeVar('Args')
ReturnType = TypeVar('ReturnType')
Func = Callable[[Args], ReturnType]


def admin_display(
    admin_order_value: Optional[str] = None,
    allow_tags: Optional[bool] = None,  # deprecated in django >= 2.0
    boolean: Optional[bool] = None,
    empty_value_display: Optional[str] = None,
    short_description: Optional[str] = None,
) -> Callable[[Func], Func]:
    """

    """
    def wrapper(func: Func) -> Func:
        if admin_order_value is not None:
            setattr(func, 'admin_order_value', admin_order_value)
        if allow_tags is not None:
            if django.VERSION[:2] > (1, 11):
                raise AttributeError(
                    "`allow_tags` is not supported by django > 2.0",
                )
            setattr(func, 'allow_tags', allow_tags)
        if boolean is not None:
            setattr(func, 'boolean', boolean)
        if empty_value_display is not None:
            setattr(func, 'empty_value_display', empty_value_display)
        if short_description is not None:
            setattr(func, 'short_description', short_description)
        return func

    return wrapper
