#!/usr/bin/env python

# Copyright (c) 2019, IRIS-HEP
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy

import uproot.source.chunked

class XRootDSource(uproot.source.chunked.ChunkedSource):
    # makes __doc__ attribute mutable before Python 3.3
    __metaclass__ = type.__new__(type, "type", (uproot.source.chunked.ChunkedSource.__metaclass__,), {})

    def __init__(self, path, timeout=None, *args, **kwds):
        self._size = None
        self.timeout = timeout
        super(XRootDSource, self).__init__(path, *args, **kwds)

    defaults = {"timeout": None, "chunkbytes": 16*1024, "limitbytes": 16*1024**2}

    def _open(self):
        try:
            import pyxrootd.client
        except ImportError:
            raise ImportError("Install pyxrootd package with:\n    conda install -c conda-forge xrootd\n(or download from http://xrootd.org/dload.html and manually compile with cmake; setting PYTHONPATH and LD_LIBRARY_PATH appropriately).")

        if self._source is None or not self._source.is_open():
            self._source = pyxrootd.client.File()
            status, dummy = self._source.open(self.path, timeout=(0 if self.timeout is None else self.timeout))
            if status.get("error", None):
                raise OSError(status["message"])
            status, info = self._source.stat(timeout=(0 if self.timeout is None else self.timeout))
            if status.get("error", None):
                raise OSError(status["message"])
            self._size = info["size"]

    def size(self):
        if self._size is None:
            self._open()
        return self._size

    def threadlocal(self):
        out = XRootDSource.__new__(self.__class__)
        out.path = self.path
        out._chunkbytes = self._chunkbytes
        out.cache = self.cache
        out._source = None             # XRootD connections are *not shared* among threads
        out._size = self._size
        out.timeout = self.timeout
        return out

    def _read(self, chunkindex):
        self._open()
        status, data = self._source.read(chunkindex * self._chunkbytes, self._chunkbytes, timeout=(0 if self.timeout is None else self.timeout))
        if status.get("error", None):
            raise OSError(status["message"])
        return numpy.frombuffer(data, dtype=numpy.uint8)

    def __del__(self):
        if self._source is not None:
            self._source.close(timeout=(0 if self.timeout is None else self.timeout))

    def dismiss(self):
        pass
