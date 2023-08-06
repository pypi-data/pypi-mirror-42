# -*- coding: utf-8 -*-
import os
import sys
import types

import six
from functools import partial

from .exts.cloud_debug_python.module_explorer import GetCodeObjectAtLine, _GetModuleCodeObjects, _GetLineNumbers

from rook.logger import logger

from ..exceptions import RookBdbCodeNotFound, RookBdbSetBreakpointFailed, RookInvalidPositionException

try:
    from . import cdbg_native
    cdbg_native.InitializeModule(None)
except ImportError:
    # Special handling for Google AppEngine (Python 2.7)
    from google.devtools.cdbg.debuglets.python import cdbg_native


class BPStatus(object):
    __slots__ = ["disabled", "pickle_detected"]

    def __init__(self):
        self.disabled = False
        self.pickle_detected = False

class Bdb(object):
    def __init__(self):
        self.fncache = {}
        self._cookies = {}
        self._bp_status = {}
        self.user_line = None

    def set_trace(self):
        # Not needed
        pass

    def canonic(self, filename):
        if filename[0] == "<" and filename[-1] == ">":
            return filename
        canonic = self.fncache.get(filename)
        if not canonic:
            canonic = os.path.abspath(filename)
            canonic = os.path.normpath(canonic)
            self.fncache[filename] = canonic
        return canonic

    def ignore_current_thread(self):
        # Not needed
        pass

    def set_break(self, item, filename, lineno, aug_id):
        filename = self.canonic(filename)

        if isinstance(item, types.ModuleType):
            self._set_break_module(item, filename, lineno, aug_id)
        elif isinstance(item, types.CodeType):
            # the caller doesn't know if the code object has this line, so verify here
            if lineno not in _GetLineNumbers(item):
                return
            self._set_break_code_object(item, filename, lineno, None, aug_id)
        else:
            raise KeyError(type(item))

    def _set_break_module(self, module, filename, lineno, aug_id):
        status, code_object = GetCodeObjectAtLine(module, lineno)
        if not status:
            if hasattr(module, '__file__'):
                logger.debug("CodeNotFound module filename %s", module.__file__)

            for cobj in _GetModuleCodeObjects(module):
                logger.debug("Name: %s", cobj.co_name)
                for cline in _GetLineNumbers(cobj):
                    logger.debug("Name: %s, Line %d", cobj.co_name, cline)

            if code_object == (None, None):
                raise RookBdbCodeNotFound(filename=filename)
            else:
                raise RookInvalidPositionException(filename=filename, line=lineno, alternatives=code_object)

        self._set_break_code_object(code_object, filename, lineno, module, aug_id)

    def _set_break_code_object(self, code_object, filename, lineno, module, aug_id):
        module_name = None
        if module is not None:
            module_name = module.__name__
        # Install the breakpoint
        bp_status = BPStatus()
        cookie = cdbg_native.SetConditionalBreakpoint(code_object, lineno, None, partial(_callback, lineno=lineno,
                                                                                         user_line=self.user_line,
                                                                                         callback_object_id=id(_callback),
                                                                                         bp_status=bp_status,
                                                                                         filename=filename,
                                                                                         module=module_name,
                                                                                         aug_id=aug_id))

        if cookie < 0:
            raise RookBdbSetBreakpointFailed()

        self._cookies[aug_id] = cookie
        self._bp_status[aug_id] = bp_status

    def clear_break(self, aug_id):
        try:
            cookie = self._cookies[aug_id]
            status = self._bp_status[aug_id]
        except KeyError:
            return

        cdbg_native.ClearConditionalBreakpoint(cookie)
        status.disabled = True
        del self._cookies[aug_id]
        del self._bp_status[aug_id]

    def clear_all_breaks(self):
        for cookie in six.itervalues(self._cookies):
            cdbg_native.ClearConditionalBreakpoint(cookie)

        for status in six.itervalues(self._bp_status):
            status.disabled = True

        self._cookies = {}
        self._bp_status = {}

    def close(self):
        pass


# This function has been moved outside of the class so that it can be pickled
# safely by cloudpickle (which will pickle any objects referred to by its closure)
# When changing it, take care to avoid using references to anything not imported within the function
def _callback(lineno, user_line, callback_object_id, bp_status, filename, module, aug_id):
    import inspect
    frame = None
    try:
        frame = inspect.currentframe().f_back
    except:
        pass
    try:
        if bp_status.disabled is True or frame is None:
            return
        # this swap is atomic (the interpreter won't interrupt thanks to the GIL),
        # which allows us to make sure the block below is only ever visited once
        # without using a lock (which can't be pickled)
        bp_status.pickle_detected, old_pickle_detected_value = callback_object_id != id(_callback), bp_status.pickle_detected

        if bp_status.pickle_detected and old_pickle_detected_value is False:
            from rook.interface import _rook as singleton
            if singleton is None:
                return
            from rook.services import ImportService
            import_service = singleton.get_trigger_services().get_service(ImportService.NAME)
            import_service._notify_of_pickled_code_object(module, filename, frame.f_code, aug_id)

    except:
        pass
    try:
        if frame and user_line:
            user_line(frame, filename, lineno=lineno, aug_id=aug_id)
    except:
        pass