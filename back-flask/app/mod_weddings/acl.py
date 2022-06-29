from functools import wraps # functools is a standard Python module for higher-order functions (functions that act on or return other functions). wraps() is a decorator that is applied to the wrapper function of a decorator.

def verify_wedding(f):
    @wraps(f)
    def _verify(user, *args, **kwargs):
      print(user)
      print(kwargs)
      return f(user, *args, **kwargs)
    return _verify

def verify_wedding_images(f):
    @wraps(f)
    def _verify(user, *args, **kwargs):
      print(user)
      print(kwargs)
      return f(user, *args, **kwargs)
    return _verify