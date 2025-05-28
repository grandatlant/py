#!/usr/bin/env -S python3 -O
# -*- coding = utf-8 -*-
"""Decorators and other tools to enhance function usage.
"""

__version__ = '0.0.1'
__copyright__ = 'Copyright (C) 2025 grandatlant'

__all__ = [
    'wrap_with_calls',
]

import functools

def wrap_with_calls(
    func: callable = None,
    /,
    *,
    first_call = None,
    after_call = None,
    args: tuple = None,
    kwds: dict = None,
    return_filter_func: callable = None,
    reduce_result_func: callable = None,
    ) -> callable:
    """Used to call something before and after decorated function call.
    Params:
        func - a single function to call before AND after
            the decorated function called.
            
            If applyed as decorator with no (), if transforms this function
            into decorator, that does something like next:
    
                @wrap_with_calls
                def print_yum():
                    print('yum')

                @print_yum
                def spit():
                    print('spit')
                
                spit()

            will result in next console output:
                yum
                spit
                yum
                
        first_call - callable or collection yielding callables to be called
            before decorated function
            
        after_call - callable or collection yielding callables to be called
            after decorated function
            
        args, kwds - positional and keyword arguments
            that will be passed to ALL callables
            in (*first_call, func, func, *after_call)

        return_filter_func - if specified, application this to any of the
            returns wraping functions will result in wrapped function return

            
    """

    #list of callables need to be called before decorated_func called
    _first_call = list()
    if first_call is None:
        pass
    elif callable(first_call):
        _first_call.append(first_call)
    elif hasattr(first_call, '__iter__'):
        _first_call.extend(first_call)
    else:
        raise ValueError('"first_call" parameter must be callable or iterable')
    #'func' call AFTER all 'first_call' calls
    if func is not None and callable(func):
        _first_call.append(func)

    #list of callables need to be called after_call decorated_func called
    _after_call = list()
    #'func' call BEFORE all 'first_call' calls
    if func is not None and callable(func):
        _after_call.append(func)
    if after_call is None:
        pass
    elif callable(after_call):
        _after_call.append(after_call)
    elif hasattr(after_call, '__iter__'):
        _after_call.extend(after_call)
    else:
        raise ValueError('"after_call" parameter must be callable or iterable')

    _args = args or tuple()
    _kwds = kwds or dict()
    _return_filter_enabled = (
        return_filter_func is not None
        and callable(return_filter_func)
    )
    
    @functools.wraps(func)
    def decorator(decorated_func):
        @functools.wraps(decorated_func)
        def decorated_func_wrapper(
            *decorated_func_args,
            **decorated_func_kwds
        ):
            results = list()
            # first calls
            for item in _first_call:
                if callable(item):
                    cur_result = item(*_args, **_kwds)
                    if (_return_filter_enabled
                        and return_filter_func(cur_result)):
                        return cur_result
                    results.append(cur_result)
            
            # !!! decorated_func call !!!
            decorated_func_result = decorated_func(
                *decorated_func_args,
                **decorated_func_kwds
            )
            ##TODO: Think about next 2 commented lines...
            #if return_filter_func(decorated_func_result):
            #    return decorated_func_result
            results.append(decorated_func_result)
            
            # after calls
            for item in _after_call:
                if callable(item):
                    cur_result = item(*_args, **_kwds)
                    if (_return_filter_enabled
                        and return_filter_func(cur_result)):
                        return cur_result
                    results.append(cur_result)
            
            # reduce results if specified
            if (reduce_result_func is not None
                and callable(reduce_result_func)):
                return functools.reduce(reduce_result_func, results)
            
            # general result
            return decorated_func_result
        return decorated_func_wrapper
    return decorator

def call_before(
    func,
    args: tuple = None,
    kwds: dict = None,
    return_filter_func: callable = None,
    reduce_result_func: callable = None,
):
    return wrap_with_calls(
        first_call=func,
        args=args,
        kwds=kwds,
        return_filter_func=return_filter_func,
        reduce_result_func=reduce_result_func,
        )

def call_after(
    func,
    args: tuple = None,
    kwds: dict = None,
    return_filter_func: callable = None,
    reduce_result_func: callable = None,
):
    return wrap_with_calls(
        after_call=func,
        args=args,
        kwds=kwds,
        return_filter_func=return_filter_func,
        reduce_result_func=reduce_result_func,
        )

##  MAIN ENTRY POINT
def main(args=None):
    return 0

if __name__ == '__main__':
    main()
