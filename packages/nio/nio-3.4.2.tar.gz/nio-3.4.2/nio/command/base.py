from nio.command.params.base import Parameter
from nio.command.params.string import StringParameter


class InvalidCommandArg(Exception):
    pass


class MissingCommandArg(Exception):
    pass


class Command(object):

    """Command to be used in CommandHolders (Blocks and Services).

    Args:
        id (str): The id of the command. Should be the same as the name of
            the corresponding method.
        params (Properties): List of Property Params that are part of the
            command
        title (str): An optionally more detailed description of the
            command. If left blank, title defaults to id.
        method (str): The id of the real method exposed by this command if
            different than id

    """

    def __init__(self, id, *params, title=None, method=None):
        self._id = id
        self._parameters = []
        for p in params:
            self._add_parameter(p)
        self._title = title or id
        self._method = method or id

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def parameters(self):
        return self._parameters

    @property
    def method(self):
        return self._method

    def get_description(self):
        """Returns a description for a command instance.

        This method is used iteratively in CommandHolder.get_description.

        Returns:
            description (dict): the title of the command and descriptions
                of its parameters
        """
        description = {"title": self.title}
        params = {}
        for p in self._parameters:
            params[p.name] = p.get_description()
        description["params"] = params
        return description

    def _add_parameter(self, param):
        if isinstance(param, Parameter):
            self._parameters.append(param)
        else:
            raise RuntimeError("Invalid command parameter type: '{}'".format(
                getattr(param, 'name', param)))

    def collect_arguments(self, args):
        """Format passed arguments into parameter args and kwargs.

        Assign values to the command's parameters. This is done to
        provide safe conversion of command arguments from strings (they
        will likely arrive as strings in an HTTP request body) and to
        ensure that arguments are of the correct types.

        This method converts each argument to the appropriate type per
        each parameter. Collection fails if, for any parameter, allow_none
        is false and the type conversion returns None.

        Args:
            args (dict): The arguments.

        Returns:
            args (list): The list of arguments, converted and type
                checked.
        """
        result = []
        result_kwargs = {}
        if isinstance(args, dict):

            # Find and convert each param needed
            for p in self._parameters:
                raw_val = args.get(p.name) or p.default
                if raw_val is not None or p.allow_none:
                    val = p.deserialize(raw_val)
                    result.append(val)
                else:
                    raise MissingCommandArg(
                        "Command {}: missing argument {}".format(
                            self.id, p.name))
            # Now that we have all params that were not passed but have
            # default value covered, lets check for unrecognized param passed
            invalid_args = [arg for arg in args if arg not in
                            [p.name for p in self._parameters]]
            # Treat all extra args in the passed dict as kwargs
            for arg in invalid_args:
                result_kwargs[arg] = args.get(arg)
        else:
            # Try to use whole arg as the param if the method only
            # needs one
            if len(self._parameters) == 1 and \
                    self._parameters[0].__class__ == StringParameter:
                result.append(args)
            else:
                raise InvalidCommandArg(
                    "Invalid arguments (dict expected): {0}".format(args))
        return result, result_kwargs
