"""Much cheaper version of 'overloaded', based exclusively on number of args"""

# TODO
# add support for class-, -static methods and functions


class Grouped(dict):
    def __call__(self, key):
        def wrap(value):
            self[key] = value
            return self
        return wrap

def group(key):
    return lambda value: Grouped({key: value})

class ArityGrouped(dict):
    def __call__(self, f):
        self[f.__code__.co_argcount] = f
        return self

def with_arity(f):
    return ArityGrouped()(f)

class Arity(type):
    def __new__(cls, name, bases, attrs):
        for k, v in attrs.items():
            if isinstance(v, ArityGrouped):
                def wrap(*args):
                    try:
                        f = v[len(args)]
                    except KeyError:
                        raise TypeError(f'no function with arity {len(args)}')
                    else:
                        return f(*args)

                attrs[k] = wrap

        return super().__new__(cls, name, bases, attrs)
