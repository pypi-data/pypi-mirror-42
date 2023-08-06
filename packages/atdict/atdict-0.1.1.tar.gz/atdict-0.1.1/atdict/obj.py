# Tai Sakuma <tai.sakuma@gmail.com>
import collections
import logging

##__________________________________________________________________||
class atdict(object):
    """a simple class to represent an object in an event, e.g., a jet, muon.

    implemented as an attribute-access ordered dictionary

    """

    def __init__(self, *args, **kwargs):

        try:
            # First, assume args[0] is another instance of this class,
            # and try to copy the contents of the instance.
            attrdict = collections.OrderedDict(args[0]._attrdict)
        except (AttributeError, IndexError):
            # Otherwise, all arguments are simply given to OrderedDict
            # so that this class can be instantiated with any
            # arguments that can instantiate OrderedDict.
            attrdict = collections.OrderedDict(*args, **kwargs)
        else:
            if len(args) > 1 or kwargs:
                logger = logging.getLogger(__name__)
                logger.warning('extra arguments are given: args={}, kwargs={}'.format(args[1:], kwargs))

        object.__setattr__(self, '_attrdict', attrdict)
        # self._attrdict = attrdict # this would cause infinite
                                    # recursion as __setattr__() is
                                    # implemented

    def __copy__(self):
        return self.__class__(self)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(k, v) for k, v in self._attrdict.items()])
        )

    def __getattr__(self, attr):
        try:
            return self._attrdict[attr]
        except KeyError:
            raise AttributeError('{} has no attribute "{}"'.format(self, attr))

    def __setattr__(self, name, value):
        self._attrdict[name] = value

    def __eq__(self, other):
        return self._attrdict == other._attrdict

##__________________________________________________________________||
