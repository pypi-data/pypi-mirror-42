import inspect
import types
import sys


def _is_serializable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False


if sys.version_info[0] == 3:

    # TODO: annotations

    def _get_method_sign(func):
        '''
        Returns a signature for a given function
        '''
        sign = {}
        argspec = inspect.getfullargspec(func)
        sign['type'] = 'method'
        sign['name'] = func.__name__
        sign['args'] = argspec.args
        sign['vargs'] = True if argspec.varargs else False
        sign['kwargs'] = True if argspec.varkw else False
        defs = argspec.defaults
        if defs is not None:
            defs = list(defs)
        if not _is_serializable(defs):
            defs = None
        sign['defaults'] = defs
        return sign
else:
    def _get_method_sign(func):
        '''
        Returns a signature for a given function
        '''
        sign = {}
        argspec = inspect.getargspec(func)
        sign['type'] = 'method'
        sign['name'] = func.__name__
        sign['args'] = argspec.args
        sign['vargs'] = True if argspec.varargs else False
        sign['kwargs'] = True if argspec.keywords else False
        defs = argspec.defaults
        if defs is not None:
            defs = list(defs)
        if not _is_serializable(defs):
            defs = None
        sign['defaults'] = defs
        return sign


def _get_cls_sign(cls, module=None):
    '''
    Returns a signature for a given function
    '''
    sign = {}
    sign['type'] = 'class'
    sign['name'] = str(cls).split("'")[1].split("'")[0]
    methods = []
    properties = []
    classmethods = []
    staticmethods = []
    bases = []
    classes = []
    variables = {}
    cls_dict = getattr(cls, '__dict__')
    if cls_dict is not None:
        for k, v in cls_dict.items():
            if k[0] == '_' and not (k.startswith('__') and k.endswith('__')):
                continue
            if module is not None:
                v_module = getattr(v, '__module__')
                if v_module is not None and v_module != module:
                    continue
            if isinstance(v, types.FunctionType):
                f_sign = _get_method_sign(v)
                # We trust the user to use 'self' here.
                args = f_sign['args']
                if len(args) > 0 and args[0] == 'self':
                    methods.append(f_sign)
                else:
                    staticmethods.append(f_sign)
            elif isinstance(v, types.MethodType):
                classmethods.append(_get_method_sign(v.__func__))
            elif isinstance(v, property):
                # We don't look into the actual get/setter signs.
                properties.append(k)
            elif isinstance(v, type):
                classes.append(_get_cls_sign(v))
            else:
                variables[k] = str(type(v))
    base_classes = set(inspect.getmro(cls)[1:])
    if object in base_classes:
        base_classes.remove(object)
    for base in base_classes:
        bases.append(_get_cls_sign(base))
    sign['methods'] = methods
    sign['properties'] = properties
    sign['classmethods'] = classmethods
    sign['staticmethods'] = staticmethods
    sign['bases'] = bases
    sign['variables'] = variables
    return sign


def _get_module_sign(module):
    name = module.__name__
    root_module = name.split('.')[0]
    sign = {}
    sign['type'] = 'module'
    sign['name'] = name
    modules = []
    classes = []
    methods = []
    variables = {}
    for k, v in module.__dict__.items():
        if k[0] == '_':
            continue
        v_module = getattr(v, '__module__', None)
        if v_module is not None and v_module.split('.')[0] != root_module:
            continue
        if isinstance(v, types.ModuleType):
            if not v.__name__.startswith(name + '.'):
                continue
            modules.append(_get_module_sign(v))
        elif isinstance(v, type):
            classes.append(_get_cls_sign(v))
        elif isinstance(v, types.FunctionType):
            methods.append(_get_method_sign(v))
        else:
            variables[k] = str(type(v))
    sign['modules'] = modules
    sign['classes'] = classes
    sign['methods'] = methods
    sign['variables'] = variables
    return sign


def sign(obj):
    if isinstance(obj, types.ModuleType):
        return _get_module_sign(obj)
    elif isinstance(obj, type):
        return _get_cls_sign(obj)
    elif isinstance(obj, (types.FunctionType, types.MethodType)):
        return _get_method_sign(obj)
    else:
        raise NotImplementedError("Unsupported type: " + str(type(obj)) + ".")
