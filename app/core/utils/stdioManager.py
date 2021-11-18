# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:47:29 2019

@author: URJC
"""

import sys
import builtins

from app.core.utils import SingletonDecorator
# from singleton import SingletonDecorator
from abc import ABC, abstractmethod

try:
    import tensorflow.compat.v1 as tf
except:
    import tensorflow as tf


class OutStreamBase(ABC):
    @abstractmethod
    def write(self, m):
        pass

    def flush(self):
        pass


# !todo: Añade un print con color para los editores
# !todo: Añade niveles de verbose
@SingletonDecorator
class StdoutManager():
    def __init__(self):
        self._consolestdout = sys.stdout
        self._consolestderr = sys.stderr
        self._defaultstdout = sys.stdout
        self._defaultstderr = sys.stderr
        self._queueStdout = list()
        self._queueStderr = list()

        self._defaultPrint = builtins.print
        builtins.print = self._printVerbose
        self._verbose = True
        self._allowForcePrint = False

        self._tfdefaultPrint = tf.print
        self._tfverbose = True

    def _printNonVerbose(self, *args, forcePrint=False, **kwargs):
        if forcePrint:
            self._defaultPrint(*args, **kwargs)

    def _printVerbose(self, *args, forcePrint=False, **kwargs):
        self._defaultPrint(*args, **kwargs)

    @property
    def tfverbose(self):
        return self._tfverbose

    @tfverbose.setter
    def tfverbose(self, value):
        if not isinstance(value, bool):
            raise TypeError('Boolean expected')

        self._tfverbose = value

        tf.print = self._tfdefaultPrint if value else lambda *a, **k: None

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        if not isinstance(value, bool):
            raise TypeError('Boolean expected')

        self._verbose = value

        builtins.print = self._printVerbose if value else lambda *a, **k: None

        if self._allowForcePrint and not value:
            builtins.print = self._printNonVerbose

    @property
    def allowForcePrint(self):
        return self._allowForcePrint

    @allowForcePrint.setter
    def allowForcePrint(self, value):
        if not isinstance(value, bool):
            raise TypeError('Boolean expected')

        self._allowForcePrint = value
        self.verbose = self.verbose

    @property
    def consolestdout(self):
        return self._consolestdout

    @property
    def consolestderr(self):
        return self._consolestderr

    @property
    def defaultstdout(self):
        return self._defaultstdout

    @defaultstdout.setter
    def defaultstdout(self, value):
        if not (isinstance(value, OutStreamBase) or \
                value == self._consolestdout):
            raise TypeError("OutStreamBase value expected")

        self._defaultstdout = value

    @property
    def defaultstderr(self):
        return self._defaultstderr

    @defaultstderr.setter
    def defaultstderr(self, value):
        if not (isinstance(value, OutStreamBase) or \
                value == self._consolestderr):
            raise TypeError("OutStreamBase value expected")

        self._defaultstderr = value

    def pushStdout(self, stream):
        if not isinstance(stream, OutStreamBase):
            raise TypeError("OutStreamBase value expected")

        self._queueStdout.append(sys.stdout)
        sys.stdout = stream

    def popStdout(self):
        if len(self._queueStdout) != 0:
            sys.stdout = self._queueStdout.pop()

    def pushStderr(self, stream):
        if not isinstance(stream, OutStreamBase):
            raise TypeError("OutStreamBase value expected")

        self._queueStderr.append(sys.stderr)
        sys.stderr = stream

    def popStderr(self):
        if len(self._queueStderr) != 0:
            sys.stderr = self._queueStderr.pop()

    def pushDefaultStdout(self):
        self._queueStderr.append(sys.stdout)
        sys.stdout = self._defaultstdout

    def pushDefaultStderr(self):
        self._queueStderr.append(sys.stderr)
        sys.stderr = self._defaultstderr


class OutNullStream(OutStreamBase):
    def write(self, m):
        pass


class OutStrStream(OutStreamBase):
    def __init__(self, initialString=None, out=None):
        """(string, out=None) -> can write stdout, stderr to a string
        
        string = str
        out = alternate stream ( can be the original sys.stdout )
        """
        self._string = initialString
        self._out = out

    def write(self, m):
        self._string += m
        if self._out:
            self._out.write(m)

    def flush(self):
        if self._out:
            self._out.flush()

    @property
    def string(self):
        return self._string

    def clear(self):
        self._string = ""


class OutFileStream(OutStreamBase):
    def __init__(self, file, out=None):
        self._f = file
        self._out = out

    def write(self, m):
        self._f.write(m)
        if self._out:
            self._out.write(m)

    def flush(self):
        if self._out:
            self._out.flush()


if __name__ == '__main__':
    str_ = "Initial:\n"

    stdout = OutStrStream(initialString=str_,
                          out=StdoutManager().getDefaultStdout())
    StdoutManager().pushStdout(stdout)

    print(102, "23")
    StdoutManager().popStdout()
    print(stdout.string)

    StdoutManager().verbose = False
    print("Ko")

    StdoutManager().verbose = True
    print("Ok")

    StdoutManager().verbose = False
    print("Force Verbose KO", forcePrint=True)
    StdoutManager().allowForcePrint = True
    print("Force Verbose OK", forcePrint=True)
    StdoutManager().allowForcePrint = False
    print("Force Verbose KO", forcePrint=True)
