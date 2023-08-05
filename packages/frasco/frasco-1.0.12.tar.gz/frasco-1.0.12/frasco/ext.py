from flask import current_app, has_app_context
from frasco.utils import (AttrDict, import_string, find_classes_in_module, extract_unmatched_items,
                          import_string, deep_update_dict)
import functools
import inspect
import logging


__all__ = ('Extension', 'ExtensionState', 'ExtensionError', 'ext_stateful_method',
           'require_extension', 'has_extension', 'get_extension_state')


class ExtensionError(Exception):
    pass


class ExtensionState(object):
    def __init__(self, extension, options):
        self.extension = extension
        self.options = AttrDict(options)

    def get_option(self, name, default=None):
        return self.options.get(name, default)

    def require_option(self, name):
        if not self.options.get(name):
            raise ExtensionError('Option "%s" is missing for extension "%s"' % (name, self.extension.name))
        return self.options[name]

    def import_option(self, name, required=True):
        if required:
            import_name = self.require_option(name)
        else:
            import_name = self.get_option(name)
        if import_name:
            return import_string(import_name)


class Extension(object):
    name = None
    defaults = None
    prefix_extra_options = None
    state_class = ExtensionState

    def __init__(self, app=None, **options):
        if not self.name:
            raise ExtensionError("A name property must be defined on Extension classes")
        self._wait_for_state_methods = []
        self.app = app
        self.init_options = options
        if app:
            self.init_app(app)

    def init_app(self, app, **options):
        options = deep_update_dict(deep_update_dict(dict(self.init_options), options), get_extension_config(app, self.name))
        if self.prefix_extra_options:
            app.config.update(extract_unmatched_items(options, self.defaults or {},
                prefix=self.prefix_extra_options, uppercase=True))
        app.extensions[self.name] = self.state_class(self, dict(self.defaults or {}, **options))
        self._init_app(app, app.extensions[self.name])
        for func, args, kwargs in self._wait_for_state_methods:
            func(self, app.extensions[self.name], *args, **kwargs)

    def _init_app(self, app, state):
        raise NotImplementedError()

    def get_app(self, app=None):
        if app is not None:
            return app
        if current_app:
            return current_app._get_current_object()
        if self.app is not None:
            return self.app
        raise RuntimeError(
            'No application found. Either work inside a view function or push'
            ' an application context.'
        )

    def get_state(self, app=None):
        return get_extension_state(self.name, app=self.get_app(app))


def ext_stateful_method(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        app = kwargs.get('_app')
        if has_app_context() or self.app or app:
            return func(self, self.get_state(app), *args, **kwargs)
        self._wait_for_state_methods.append((func, args, kwargs))
    return wrapper


def get_extension_config(app, name):
    opts = {k.lower(): v for k, v in app.config.get(name.upper(), {}).items()}
    opts.update(app.config.get_namespace("%s_" % name.upper()))
    return opts


def get_extension_state(ext_name, state=None, app=None, must_exist=True):
    if state:
        return state
    if not app:
        app = current_app
    if must_exist:
        assert ext_name in app.extensions, ("The current app does not have the extension '%s'" % ext_name)
    return app.extensions.get(ext_name)


def require_extension(ext_name, app=None):
    get_extension_state(ext_name, app)


def has_extension(name, app=None):
    return get_extension_state(name, app=app, must_exist=False) is not None


def load_extensions_from_config(app, key='EXTENSIONS'):
    loaded = []
    for spec in app.config.get(key, []):
        if isinstance(spec, (str, unicode)):
            ext_module = spec
            options = {}
        elif isinstance(spec, (tuple, list)):
            ext_module, options = spec
        elif isinstance(spec, dict):
            ext_module, options = spec.items()[0]
        ext_class = import_string(ext_module)
        if inspect.ismodule(ext_class):
            ext_classes = find_classes_in_module(ext_class, (Extension,))
            if len(ext_classes) > 1:
                raise ExtensionError('Too many extension classes in module')
            ext_class = ext_classes[0]
        loaded.append(ext_class(app, **options))
        logging.getLogger('frasco').info("Extension '%s.%s' loaded" % (ext_class.__module__, ext_class.__name__))
    return loaded
