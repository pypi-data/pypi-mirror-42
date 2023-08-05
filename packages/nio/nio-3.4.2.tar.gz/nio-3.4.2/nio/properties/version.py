from nio.util.versioning.check import is_version_valid, InvalidVersionFormat
from nio.properties import StringProperty


class VersionProperty(StringProperty):

    """ Defines a Version property.

    Version property permits saving version information with
    (major.minor.build) format
    """

    def __init__(self, version=None, title="Version", advanced=True, **kwargs):
        """ Initializes a version property.

        Keyword Args:
            Property definitions

        """
        if "default" in kwargs:
            if version is not None:
                # hmm, both version and default specified,
                # version argument overrides
                kwargs["default"] = version
            super().__init__(title=title, advanced=advanced, **kwargs)
        else:
            super().__init__(title=title, advanced=advanced, default=version, **kwargs)

    def __set__(self, instance, value):
        """ Override default set to make sure it's a valid version """
        # make sure value follows "major,minor,build" convention
        if not is_version_valid(value):
            raise InvalidVersionFormat("Version: {0} is invalid".format(value))

        super().__set__(instance, value)
