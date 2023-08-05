
import inspect
import six

from .namespace import Namespace
from .container_namespace import ContainerNamespace
from .python_object_namespace import PythonObjectNamespace

from rook.exceptions import RookAttributeNotFound


# Fixing a bug in PyPy
import platform
if 'PyPy' == platform.python_implementation():
    import sys
    import six
    FakeFrameType = type(next(six.itervalues(sys._current_frames())))
    from types import FrameType

    def isframe(object):
        return isinstance(object, (FrameType, FakeFrameType))

    inspect.isframe = isframe

class FrameNamespace(Namespace):

    def __init__(self, frame):
        super(FrameNamespace, self).__init__(self.METHODS)

        self.frame = frame
        self._filename, self._lineno, self._function, self._code_context, self._index = inspect.getframeinfo(frame, 0)

    def read_attribute(self, name):
        if name in self.frame.f_locals:
            return PythonObjectNamespace(self.frame.f_locals[name])
        elif name in self.frame.f_globals:
            return PythonObjectNamespace(self.frame.f_globals[name])
        else:
            raise RookAttributeNotFound(name)

    def filename(self, args=None):
        return PythonObjectNamespace(self._filename)

    def line(self, args=None):
        return PythonObjectNamespace(self._lineno)

    def function(self, args=None):
        return PythonObjectNamespace(self._function)

    def module(self, args=None):
        module = inspect.getmodule(self.frame)
        if module:
            return PythonObjectNamespace(module.__name__)
        else:
            return PythonObjectNamespace(None)

    def locals(self, args=None):
        if args:
            depth = int(args)
        else:
            depth = None

        result = {}
        for name, value in six.iteritems(self.frame.f_locals):
            ns = PythonObjectNamespace(value)

            if depth is not None:
                ns.dump_config.max_depth = depth
            elif name == 'self':
                ns.dump_config = PythonObjectNamespace.ObjectDumpConfig.conservative_limits(value)

            result[name] = ns

        return ContainerNamespace(result)

    def globals(self, args):
        return PythonObjectNamespace(self.frame.f_globals)

    def dump(self, args):
        return ContainerNamespace({
            'locals': self.locals(args),
            'module': self.module(),
            'filename': self.filename(),
            'line': self.line(),
            'function': self.function(),
        })

    def f_back(self):
        frame = self.frame.f_back

        if frame:
            return FrameNamespace(self.frame.f_back)
        else:
            return PythonObjectNamespace(None)

    def f_next(self):
        frame = self.frame.f_next

        if frame:
            return FrameNamespace(self.frame.f_next)
        else:
            return PythonObjectNamespace(None)

    METHODS = (filename, line, function, module, locals, globals, dump)
