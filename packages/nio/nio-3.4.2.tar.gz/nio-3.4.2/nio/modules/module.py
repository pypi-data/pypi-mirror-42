from sys import maxsize

from nio.modules.context import ModuleContext


class ModuleNotInitialized(Exception):
    """ Exception raised when module that has not been initialized

    Due to the asynchronous nature of some components in the system,
    a module might be accessed even when it has not been fully
    initialized, this exception should be raised for such cases.
    """
    pass


class Module(object):

    """ A base class for defining a module interface or implementation """

    default_version = "0.1.0"

    def initialize(self, context):
        """ Override this method to perform actions on initialization.

        Typically, during initialization, a module will want to proxy some
        class definitions and perform some additional setup items.

        Args:
            context (ModuleContext): Information pertaining to this module

        Returns:
            None - the return is ignored
        """
        pass

    def finalize(self):
        """ Override this method to perform actions on finalization.

        Typically, during finalization, a module will want to unproxy the
        classes it proxied when it initialized. There may also be some
        additional clean up items.

        Returns:
            None - the return is ignored
        """
        pass

    def get_module_order(self):
        """ Override this method to set the precedence for this module.

        This method should return an int specifying when this module should
        be initialized and finalized. Modules will be initialized in the
        order low-to-high and will be finalized in the reverse order. For
        example, a module with an order of 10 will be initialized before a
        module with an order of 20, but will be finalized after it.

        Defaults to a very large number, meaning it is initialized after the
        other modules.

        Returns:
            int: The order this module should be initialized
        """
        return maxsize

    def prepare_core_context(self):
        """ Prepare a ModuleContext in the core process

        Returns:
            ModuleContext: core module context
        """
        return ModuleContext()

    def prepare_service_context(self, service_context=None):
        """ Prepare a ModuleContext for the service process

        Takes a service context so it can know information about the service.
        This method will be called in the core process, but the context
        returned will be applied to the module in the service process.

        Args:
            service_context (ServiceContext): Service context (same context
                that is used when configuring a service)

        Returns:
            ModuleContext: service module context
        """
        return ModuleContext()

    def get_module_type(self):
        """ Provides module type

        Allows to provide a module type, note that this is not meant
        to be an actual implementation type.

        Returns:
            str: module type
        """
        raise NotImplementedError()

    def get_version(self):
        """ Provides module version

        Actual module implementations are encouraged to override this method.

        Returns:
            str: module version
        """
        return Module.default_version

    def get_details(self):
        """ Provides module details

        Actual module implementations may override this method and
        decide what details/properties they would like to expose.
        It is encouraged to call parent method and 'update' the result
        with own details

        """
        return {"version": self.get_version()}
