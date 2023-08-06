# Tai Sakuma <tai.sakuma@gmail.com>
import collections
import copy

##__________________________________________________________________||
class atdict(object):
    """An attribute-access ordered dictionary

    An `atdict` can be initialized with 1) another `atdict` or 2) any
    arguments that can initialize `collections.OrderedDict`.

    """

    def __init__(self, *args, **kwargs):

        try:
            # First, if `args[0]` is the only argument, assume it is
            # another `atdict`, and try to copy the its contents.
            if kwargs or len(args) != 1:
                raise TypeError
            attrdict = collections.OrderedDict(args[0]._attrdict)
        except:
            # Otherwise, all arguments are simply given to
            # `OrderedDict` so that an `atdict` can be initialized
            # with any arguments that can initialize `OrderedDict`.
            attrdict = collections.OrderedDict(*args, **kwargs)

        super(atdict, self).__setattr__('_attrdict', attrdict)
        # self._attrdict = attrdict # this would cause infinite
                                    # recursion as __setattr__() is
                                    # implemented

    def __copy__(self):
        return self.__class__(self)

    def __deepcopy__(self, memo):
        ret = self.__class__()
        super(atdict, ret).__setattr__('_attrdict', copy.deepcopy(self._attrdict))
        return ret

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

    def __delattr__(self, attr):
        del self._attrdict[attr]

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        super(atdict, self).__setattr__('__dict__', dict)

    def __eq__(self, other):
        return self._attrdict == other._attrdict

##__________________________________________________________________||
