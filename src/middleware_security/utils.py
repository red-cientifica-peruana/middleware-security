from falcon_exceptions import HTTPException


def scope_verify(scope=None):
    """ Decorator for scope verify """

    def method_decorator(func):
        def method_wrapper(*args, **kwargs):
            scope_obj = args[0].scope if not scope else scope
            context = args[1].context
            
            if isinstance(scope_obj, dict):
                scope_obj = scope_obj.get(func.__name__, None)
            
            if not 'token_scopes' in context:
                func(*args, **kwargs)
            else:
                if scope_obj is None:
                    raise HTTPException(500, "The scope was not set correctly")

                token_scopes = context['token_scopes']
                parts_scope = scope_obj.split(':')

                if len(parts_scope) < 3 or len(parts_scope) > 3:
                    raise HTTPException(500, "The scope was not set correctly")

                if (parts_scope[0] not in token_scopes or
                    parts_scope[1] not in token_scopes[parts_scope[0]] or
                    parts_scope[2] not in token_scopes[parts_scope[0]][parts_scope[1]]):
                    raise HTTPException(403, "You are not authorized to perform this action")

                func(*args, **kwargs)
        return method_wrapper
    return method_decorator
