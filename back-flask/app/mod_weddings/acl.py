from functools import wraps # functools is a standard Python module for higher-order functions (functions that act on or return other functions). wraps() is a decorator that is applied to the wrapper function of a decorator.
from app import models
from mongoengine.queryset.visitor import Q
from bson.objectid import ObjectId

# can access the wedding as guest (read)
def verify_wedding(f):
    @wraps(f)
    def _verify(user, *args, **kwargs):
      print(user)
      print(kwargs)
      has_access = False
      if kwargs.get('id_wedding') is None:
        has_access = True
      if kwargs.get('id_wedding') is not None:
        try:
          wedding = models.Wedding.objects().get(id=kwargs.get('id_wedding'))
        except models.Wedding.DoesNotExist:
          return 'Wedding does not exist', 404
        except models.Wedding.MultipleObjectsReturned:
          return 'Multiple weddings found', 404
        except Exception as e:
          print(str(e))
          return 'Error: ' + str(e), 500
        if str(wedding.user.pk) == str(user['_id']):
          has_access = True
        else:
          users = list(filter(lambda useracl: useracl['email'] == user['email'], wedding.users))
          if len(users) > 0:
            has_access = True
      if not has_access:
        return 'You are not authorized to access this wedding.', 401
      else:
        return f(user, *args, **kwargs)
    return _verify

# can access the wedding as admin (write)
def verify_wedding_admin(f):
    @wraps(f)
    def _verify(user, *args, **kwargs):
      print(user)
      print(kwargs)
      is_admin = False
      try:
        wedding = models.Wedding.objects().get(id=kwargs.get('id_wedding'))
      except models.Wedding.DoesNotExist:
        return 'Wedding does not exist', 404
      except models.Wedding.MultipleObjectsReturned:
        return 'Multiple weddings found', 404
      except Exception as e:
        print(str(e))
        return 'Error: ' + str(e), 500
      if str(wedding.user.pk) == str(user['_id']):
        is_admin = True
      else:
        users = list(filter(lambda useracl: useracl['email'] == user['email'] and useracl['is_admin'] == True, wedding.users))
        if len(users) > 0:
          is_admin = True
      if not is_admin:
        return 'You are not authorized to access this wedding as admin.', 401
      return f(user, *args, **kwargs)
    return _verify