
from nio.modules.proxy import ModuleProxy


class PublisherError(Exception):
    pass


class Publisher(ModuleProxy):

    """ An interface for a generic Publisher in the communication module """

    def __init__(self, topic=None, **kwargs):
        """ Create a new publisher instance.

        Args:
            context: Information that can optionally be provided specific to
                the communication implementation.

                It can be used to customize a publisher by overriding settings
                such as 'heartbeat_interval' and 'heartbeat_check_interval'.

            topic (str): Defines the kind of information to publish.

            kwargs: Key value argument pairs, used for backwards compatibility.
        """
        super().__init__(topic=topic, **kwargs)

    def open(self, on_connected=None, on_disconnected=None):
        """ Opens publishing channel

        Args:
            on_connected (callable): function receiving notification when
                connection is established
            on_disconnected (callable): function receiving notification when
                a disconnection occurs

        This method will setup the channel for sending, it is implementation
        specific, for example in a tcp like implementation it will open a port.

        """
        raise NotImplementedError()

    def is_connected(self):
        """ Determine if this publisher is connected and ready

        """
        raise NotImplementedError()

    def send(self, signals):
        """ Sends signals

        Args:
            signals: Signals to send
        """

        raise NotImplementedError()

    def close(self):
        """ Closes publisher.

        No further signals will be sent after a publisher is closed.

        """
        raise NotImplementedError()

    def is_closed(self):
        """ Finds out if publisher has been closed

        """
        raise NotImplementedError()
