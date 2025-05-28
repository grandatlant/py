#!/usr/bin/env -S python3 -O
# -*- coding = utf-8 -*-
"""Decorators and other tools to enhance function usage.
"""

__version__ = '1.0.0'
__copyright__ = 'Copyright (C) 2025 grandatlant'

__all__ = [
    'wrap_with_calls',
    'wrap_with',
    'call_before',
    'call_after',
]

import functools

def wrap_with_calls(
    func: callable = None,
    *func_args,
    first_call: callable = None,
    after_call: callable = None,
    args: tuple = None,
    kwds: dict = None,
    return_filter_func: callable = None,
    reduce_result_func: callable = None,
    ) -> callable:
    """Decorator to execute specified functions
    before and after the decorated function.

    Parameters:
        func (Callable):
            a single function to call before AND after
            the decorated function called.
            if wrap_with_calls used without (), transforms func
            into decorator, can be applied to other functions
        first_call (Callable or Iterable[Callable]):
            Function(s) to call before the decorated function.
        after_call (Callable or Iterable[Callable]):
            Function(s) to call after the decorated function.
        args (Tuple):
            Positional arguments to pass to all callables.
        kwds (Dict):
            Keyword arguments to pass to all callables.
        return_filter_func (Callable):
            Filter function to apply to return values of callables.
        reduce_result_func (Callable):
            Function to reduce results of all calls into one value.

    Returns:
        Callable: The decorated function.
    """

    def list_of_callables(callables):
        """Ensure the input is an iterable of callables."""
        if callables is None:
            return list()
        elif callable(callables):
            return list((callables,))
        elif hasattr(callables, '__iter__'):
            return list(callables)
        else:
            # I dont want exceptions here for dynamic use
            return list()
            #raise ValueError(f'Parameter "{callables}" '
            #                 'must be a callable '
            #                 'or an iterable of callables.')
    
    _args = args or tuple()
    _kwds = kwds or dict()
    
    @functools.wraps(func)
    def decorator(decorated_func):
        @functools.wraps(decorated_func)
        def decorated_func_wrapper(
            *decorated_func_args,
            **decorated_func_kwds
        ):
            results = list()

            # first calls
            for item in list_of_callables(first_call):
                if callable(item):
                    cur_result = item(*_args, **_kwds)
                    if (callable(return_filter_func)
                        and return_filter_func(cur_result)):
                        return cur_result
                    results.append(cur_result)

            # func before decorated_func
            if callable(func):
                func_result = func(*func_args, *_args, **_kwds)
                if (callable(return_filter_func)
                    and return_filter_func(func_result)):
                    return func_result
                results.append(func_result)

            # !!! decorated_func call !!!
            decorated_func_result = decorated_func(
                *decorated_func_args,
                **decorated_func_kwds
            )
            ##TODO: Think about next 2 commented lines...
            #if return_filter_func(decorated_func_result):
            #    return decorated_func_result
            results.append(decorated_func_result)

            # func after decorated_func
            if callable(func):
                func_result = func(*func_args, *_args, **_kwds)
                if (callable(return_filter_func)
                    and return_filter_func(func_result)):
                    return func_result
                results.append(func_result)

            # after calls
            for item in list_of_callables(after_call):
                if callable(item):
                    cur_result = item(*_args, **_kwds)
                    if (callable(return_filter_func)
                        and return_filter_func(cur_result)):
                        return cur_result
                    results.append(cur_result)
            
            # reduce results if specified
            if callable(reduce_result_func):
                return functools.reduce(reduce_result_func, results)
            
            # general result
            return decorated_func_result
        return decorated_func_wrapper
    return decorator

def wrap_with(
    func_before = None,
    func_after = None,
    *func_args,
    args: tuple = None,
    kwds: dict = None,
    return_filter_func: callable = None,
    reduce_result_func: callable = None,
) -> callable:
    return wrap_with_calls(
        first_call=func_before,
        after_call=func_after,
        args=(*func_args, *(args or tuple())),
        kwds=kwds,
        return_filter_func=return_filter_func,
        reduce_result_func=reduce_result_func,
        )

def call_before(
    func,
    *func_args,
    args: tuple = None,
    kwds: dict = None,
    return_filter_func: callable = None,
    reduce_result_func: callable = None,
) -> callable:
    return wrap_with_calls(
        first_call=func,
        args=(*func_args, *(args or tuple())),
        kwds=kwds,
        return_filter_func=return_filter_func,
        reduce_result_func=reduce_result_func,
        )

def call_after(
    func,
    *func_args,
    args: tuple = None,
    kwds: dict = None,
    return_filter_func: callable = None,
    reduce_result_func: callable = None,
) -> callable:
    return wrap_with_calls(
        after_call=func,
        args=(*func_args, *(args or tuple())),
        kwds=kwds,
        return_filter_func=return_filter_func,
        reduce_result_func=reduce_result_func,
        )

##  MAIN ENTRY POINT
def main(args=None):
    return 0

if __name__ == '__main__':
    main()
