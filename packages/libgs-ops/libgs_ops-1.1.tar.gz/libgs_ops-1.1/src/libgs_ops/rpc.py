# -*- coding: utf-8 -*-
"""
..
    Copyright © 2017-2018 The University of New South Wales

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
    Software, and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    Except as contained in this notice, the name or trademarks of a copyright holder

    shall not be used in advertising or otherwise to promote the sale, use or other
    dealings in this Software without prior written authorization of the copyright
    holder.

    UNSW is a trademark of The University of New South Wales.

libgs_ops.rpc
=============

:date:   Tue Jan  2 10:10:48 2018
:author: Kjetil Wormnes
"""

import sys

if sys.version_info >= (3,):
    from xmlrpc.client import ServerProxy, Transport
else:
    from xmlrpclib import ServerProxy, Transport


class RPCClient(ServerProxy):
    """
    An improvement on ye olde :class:`~xmlrpclib.ServerProxy`.
    
    It is fully compatible with :class:`~xmlrpclib.ServerProxy` (i.e. it implements all the same methods and functionality),
    and additionally it:

      * Times out if the connection has gone belly up
      * Allows kwargs to be passed along with arguments, by adding the kwargs as a single dictionary argument
        at the end of the list of parameters. If no kwargs are specified it will not be added, and therefore it
        is fully backwards compatible with normal :class:`~SimpleXMLRPCServer.SimpleXMLRPCServer`.
      * Properly implements ``__dir__`` and ``__getattr__`` to query for remote methods and interface with them as attributes

    """
    # This flag is added by the client to an argument dictionary to be treated as kwargs
    _KWARGS_FLAG = '__xmlrpc__kwargs__'

    class TimeoutTransport(Transport):

        def __init__(self, timeout, use_datetime=0):
            self.timeout = timeout
            # xmlrpclib uses old-style classes so we cannot use super()
            Transport.__init__(self, use_datetime)

        def make_connection(self, host):
            connection = Transport.make_connection(self, host)
            connection.timeout = self.timeout
            return connection

    def __init__(self, uri, timeout=60, transport=None, encoding=None, verbose=0,
                 allow_none=0, use_datetime=0):

        """
            .. note::
                The RPCClient constructor accepts the same arguments as :class:`~xmlrpclib.ServerProxy` except you cannot set
                the transport. The reason is that RPCClient uses its own custom transport to implement the timeout.

            Args:
                uri (str):          URI of XMLRPC Server (e.g. https:///my.server)
                timeout (int):      Timeout in seconds to apply to queries to server
                transport:          Not available (must be None)    
                encoding:           Encoding to use
                verbose:            Debugging flag
                allow_none:         If true, None will be transmitted.
                use_datetime:       If true, :class:`datetime.datetime` will be transmitted.

            For further description of encoding, verbose, allow_none and use_datetime, see :class:`~xmlrpclib.ServerProxy`.

            Available methods are those that have been registered on the remote XMLRPC server.

        """

        if transport is not None:
            raise Exception("transport parameter is not allowed. This implementation uses a timeout transport")

        t = self.TimeoutTransport(timeout)

        ServerProxy.__init__(self, uri, t, encoding, verbose, allow_none, use_datetime)

    def __dir__(self):
        methods = self.system.listMethods()
        return [] if methods is None else methods

    def __getattr__(self, name):

        if name == 'system':
            return ServerProxy.__getattr__(self, name)

        def _method(*args, **kwargs):
            method = ServerProxy.__getattr__(self, name)
            if len(kwargs) > 0:
                kwargs[self._KWARGS_FLAG] = True
                params = list(args) + [kwargs]
                return method(*params)
            else:
                return method(*args)

        return _method