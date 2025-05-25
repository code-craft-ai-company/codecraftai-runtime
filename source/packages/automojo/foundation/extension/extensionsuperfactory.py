"""
.. module:: extensionsuperfactory
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the `ExtensionSuperFactory` object which is used to
               create a singleton instance for dynamically loading type extensions.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from operator import attrgetter
from typing import Callable, Generator, List, Type, Union

from automojo.foundation.extension.extensionfactory import ExtensionFactory

from automojo.foundation.extension.utilities import (
    load_and_set_extension_factory_type,
    scan_amr_factories_namespace
)

class ExtensionSuperFactory:
    """
        A :class:`ExtensionSuperFactory` object is used to maintain a chain of factory types that
        can be traversed in order to locate a factory that implements a specific protocol
        in order to enable various types of overload or overinstance states.
    """

    def __init__(self, factory_modules: List[str]):

        self._factory_modules = scan_amr_factories_namespace()
        if len(factory_modules) > 0:
            self._factory_modules.extend(factory_modules)

        self._extension_factories: List[ExtensionFactory] = []

        for smod in self._factory_modules:
            factory_type = load_and_set_extension_factory_type(smod)
            if factory_type is not None:
                self._extension_factories.append(factory_type)

        self._extension_factories.sort(key=attrgetter('PRECEDENCE'))

        return

    @property
    def extension_factories(self):
        item_list = [item for item in self._extension_factories]
        return item_list

    @property
    def factory_modules(self):
        item_list = [item for item in self._factory_modules]
        return item_list

    def add_factory_module(self, factory_module: str):
        """
            Can be used by super factory consumers to app the path of a wellknown factory module.
        """
        if factory_module not in self._factory_modules:
            self._factory_modules.append(factory_module)

            factory_type = load_and_set_extension_factory_type(factory_module)
            if factory_type is not None:
                self._extension_factories.append(factory_type)
                self._extension_factories.sort(key=attrgetter('PRECEDENCE'))
        return

    def create_instance_by_order(self, factory_method: Callable, *args, **kwargs) -> Union[object, None]:

        instance = None

        proto_type_name = factory_method.__qualname__.split('.')[0]
        proto_type = factory_method.__globals__[proto_type_name]
        proto_name = proto_type.ext_protocol_name
        factory_method = factory_method.__name__

        create_instance: Callable = None

        for factory_type in self._extension_factories:
            if hasattr(factory_type, factory_method):
                factory_proto_name = factory_type.ext_protocol_name
                if factory_proto_name == proto_name:
                    create_instance = getattr(factory_type, factory_method)
        
        if create_instance is not None:
            instance = create_instance(*args, **kwargs)

        return instance

    def create_instance_for_each(self, factory_method: Callable, *args, **kwargs) -> List[object]:

        list_of_instances = []

        proto_type_name = factory_method.__qualname__.split('.')[0]
        proto_type = factory_method.__globals__[proto_type_name]
        proto_name = proto_type.ext_protocol_name
        factory_method = factory_method.__name__

        for factory_type in self._extension_factories:
            if hasattr(factory_type, factory_method):
                factory_proto_name = factory_type.ext_protocol_name
                if factory_proto_name == proto_name:
                    create_instance = getattr(factory_type, factory_method)
                    instance = create_instance(*args, **kwargs)
                    list_of_instances.append(instance)

        return list_of_instances

    def get_override_types_by_order(self, get_type_method: Callable) -> Union[Type, List[Type], None]:

        found_type = None

        get_type_with = None

        proto_type_name = get_type_method.__qualname__.split('.')[0]
        proto_type = get_type_method.__globals__[proto_type_name]
        proto_name = proto_type.ext_protocol_name
        get_type_method = get_type_method.__name__

        for factory_type in self._extension_factories:
            if hasattr(factory_type, get_type_method):
                factory_proto_name = factory_type.ext_protocol_name
                if factory_proto_name == proto_name:
                    get_type_with = getattr(factory_type, get_type_method)
        
        if get_type_with is not None:
            found_type = get_type_with()
        
        return found_type
    
    def iterate_override_types_for_each(self, get_type_method: Callable, interate_type_lists: bool = True) -> Generator[Union[Type, List[Type], None], None, None]:

        found_type = None

        get_type_with = None

        proto_type_name = get_type_method.__qualname__.split('.')[0]
        proto_type = get_type_method.__globals__[proto_type_name]
        proto_name = proto_type.ext_protocol_name
        get_type_method = get_type_method.__name__
        
        for factory_type in self._extension_factories:
            if hasattr(factory_type, get_type_method):
                factory_proto_name = factory_type.ext_protocol_name
                if factory_proto_name == proto_name:
                    get_type_with = getattr(factory_type, get_type_method)
            
                    found_type = get_type_with()

                    if interate_type_lists and type(found_type) is list:
                        for ftitem in found_type:
                            yield ftitem
                    else:
                        yield found_type

