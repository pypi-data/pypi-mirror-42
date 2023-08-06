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


libgs_ops.scheduling
=====================

:date: Sun Aug  6 17:36:19 2017
:author: kjetil

Usage
-----

.. note::
    This example focues on the scheduler. Please see :mod:`.propagator` for instructions on how to compute
    pass data (az, el and range_rate) for your pass. For the remainder of these tutorials it is assumed
    that pdat exists.

First the pass data must be converted into a :class:`CommsPass`:

>>> cp = CommsPass(pdat, desc="Test pass")
>>> cp
Communication Pass:
  Norad ID:       25544
  Description:    Test pass
  Visib. horizon: 10
  Pass start:     2017/10/13 13:57:16
  Pass end:       2017/10/13 14:03:58
  Scheduled comms:
   (no comms added but NOT listen mode)

.. note::
    The :class:`CommsPass` allows you to set arbitrary metadata. Such metadata will be stored in the pass database together with the schedule. 
    It may also be used by a custom protocol that requires it. (See :class:`libgs.protocols.protocolbase.ProtocolBase`) 
    The metadata can be seen in the :attr:`CommsPass.metadata` attribute. It is also directly accessible by the . operator, but 
    the . operator can *not* be used to create new metadata. Either add it to the metadata dict, or on :class:`CommsPass` construction as 
    in the example below.   

>>> cp = CommsPass(pdat, hello=123, test=[1,2,3], another=dict(a=1,b=2))
>>> cp.metadata
{'another': {'a': 1, 'b': 2},
 'desc': None,
 'hello': 123,
 'horizon': 10.0,
 'listen': False,
 'nid': 25544,
 'test': [1, 2, 3]}
>>> cp.test
[1, 2, 3]

Then add communications to the pass. There are several ways to specify the byte sequence of the communications. You can also set
the ``retries`` parameter that specifies how many times to try again in case of failure.

>>> cp.add_communication('DC-00-34-BB-AA')
>>> cp.add_communication('AA-BB-CC-DD', retries=1)
>>> cp.add_communication(bytearray([0xaa,0xab, 234,43,23,45]))
>>> cp
Communication Pass:
  Norad ID:       25544
  Description:    None
  Visib. horizon: 10
  Pass start:     2017/10/13 13:57:16
  Pass end:       2017/10/13 14:03:58
  Scheduled comms:
     0 ( 3 retries) : DC-00-34-BB-AA
     1 ( 1 retries) : AA-BB-CC-DD
     2 ( 3 retries) : AA-AB-EA-2B-17-2D

The scheduler also supports actions. :class:`Action` s refer to any functionality you may have implemented in the protocol's 
:meth:`libgs.protocols.protocolbase.ProtocolBase.do_action` method,  and there is no standard format since the syntax depends on the function. 
Assuming you have made some actions for starting and stopping comms, you could add them with something like this:

>>> cp.add_communication(Action(("start_comms", 3), {'some_kwarg': 2}, desc="Start communication", retries=5))
>>> cp.add_communication(Action(("stop_comms",)))
>>> cp
Communication Pass:
  Norad ID:       25544
  Description:    None
  Visib. horizon: 10
  Pass start:     2017/10/13 13:57:16
  Pass end:       2017/10/13 14:03:58
  Scheduled comms:
     0 ( 3 retries) : DC-00-34-BB-AA
     1 ( 1 retries) : AA-BB-CC-DD
     2 ( 3 retries) : AA-AB-EA-2B-17-2D
     3 ( 5 retries) : 'Start communication' <('start_comms', 3), {'some_kwarg': 2}>
     4 ( 0 retries) : 'unnamed' <('stop_comms',), {}>

In general it is recommended to only use one positional argument, (first tuple in :meth:`CommsPass.add_communication`) and keep action-specific parameters in the dictionary (second tuple).
But this is not a requirement. See :meth:`libgs.protocols.protocolbase.ProtocolBase.do_action`.

You can access the pass data in the commspass directly. This is exatly the same pdat structure you passed in on creation:

>>> cp.pass_data.head()

=============== ======================= =========== =========== ============
.                tstamp_str              az          el          range_rate
=============== ======================= =========== =========== ============
43020.081435     2017/10/13 13:57:16     314.109     10.0034     -6800.68
43020.081447     2017/10/13 13:57:17     314.111     10.1116     -6798.35
43020.081458     2017/10/13 13:57:18     314.113     10.2206     -6795.98
43020.081470     2017/10/13 13:57:19     314.115     10.3303     -6793.57
43020.081481     2017/10/13 13:57:20     314.117     10.4407     -6791.12
=============== ======================= =========== =========== ============

To make a schedule, you need to add :class:`CommsPass`'es to a :class:`Schedule`:

>>> s = Schedule()
>>> s.add_pass(cp)
>>> s
---- -------- -------------------- -------------------- --------------
#    Norad id Pass start (utc)     Pass end (utc)       Communications
---- -------- -------------------- -------------------- --------------
0    25544    2017/10/13 13:57:16  2017/10/13 14:03:58  5

The schedule does not permit you to add overlapping passes:

>>> s.add_pass(cp)
Error: Can't add pass as it overlaps with another pass in the schedule

It is often useful to dump the schedule to a file that can be shared with other operators or loaded into adfa-gs. 
To dump a schedule to file in JSON format use the to_json() method:

>>> with open('test.schedule', 'w') as fp:
>>>    fp.write(s.to_json())

To load it again, use from_json classmethod:

>>> s2 = Schedule.from_json('test.schedule')

The :class:`Schedule` provides several convenience functions. Check the help for details.

The below complete example adds schedules for several upcoming passes, all with the same communication, and with an extra communication
to the final:

>>> passes = p.get_passes(25544, N=10, when='2017/10/14', horizon=10)
>>> cps = []
>>> for k,satpass in passes.iterrows():
>>>    pdat, psum = p.compute_pass(satpass.nid, when=satpass.rise_t)
>>>    cps += [CommsPass(pdat)]
>>>    cps[-1].add_communication(bytearray([1,2,3,4]))
>>> s = Schedule(cps)    
>>> s.passes[-1].add_communication('AA-BB-CC-DD')
>>> s
---- -------- -------------------- -------------------- --------------
#    Norad id Pass start (utc)     Pass end (utc)       Communications
---- -------- -------------------- -------------------- --------------
0 	25544 	2017/10/14 13:05:17 	2017/10/14 13:11:33 	1
1 	25544 	2017/10/14 14:42:23 	2017/10/14 14:47:36 	1
2 	25544 	2017/10/14 19:36:11 	2017/10/14 19:40:33 	1
3 	25544 	2017/10/14 21:11:50 	2017/10/14 21:18:22 	1
4 	25544 	2017/10/15 12:13:52 	2017/10/15 12:18:42 	1
5 	25544 	2017/10/15 13:49:28 	2017/10/15 13:55:42 	1
6 	25544 	2017/10/15 18:44:54 	2017/10/15 18:46:44 	1
7 	25544 	2017/10/15 20:19:33 	2017/10/15 20:26:08 	1
8 	25544 	2017/10/15 21:58:46 	2017/10/15 21:59:03 	1
9 	25544 	2017/10/16 12:56:54 	2017/10/16 13:03:35 	2


In some situations you may want to manually calculate the pointings of the antenna, or the schedule. 
If so, just ensure you create a pdat in the correct format (i.e. with tstamp_str, az, el, range_rate as 
appropriate - other headings do not matter):

>>> pdat = pd.read_excel('passes_test.xlsx')
>>> cp = CommsPass(pdat, nid=-1)

.. note::
   When specifying the pass data this way you will need  to specify which Norad ID the schedule is associated with since the 
   excel file did not specify it. It does not have to be a valid NID, so if this was a testing pass we could for example set it to -1


There are two main ways of executing the schedule on the groundstation depending on how you have implemented it.

    1. You can start your software (and scheduler) by loading and running the schedule file.
    2. You can start your software by starting the :class:`libgs.rpc.RPCSchedulerServer`. You will then be able to send
       the schedule to the groundstation with a simple XMLRPC call via :class:`RPCSchedulerClient`.

If :class:`libgs.rpc.RPCSchedulerServer` is running on the target ground station, you can upload a schedule as follows:

>>> sch = RPCSchedulerClient(schedule=s, rpcaddr='http://xmlrpc/address/goes/here')

.. note::
   The syntax for rpcaddr is http(s)://<uname>:<passwd>@<host>:<port>/...
   So if basic authentication has been enabled, or the rpc runs on an unsual port you can adjust as required

:class:`RPCSchedulerClient` implements all the methods of the :class:`libgs.scheduler.Scheduler` so you can use it the same way:

To start:

>>> sch.execute()

To stop (abort) a running schedule:

>>> sch.stop()

The scheduler implements two flags; track_full_pass and compute_ant_points. If the former has been set to true, 
the antenna will keep tracking even after finishing its communications. 
If the latter has been set to false, the antenna will stupidly execute every line in the schedule. 
This is a really bad idea for automatically computed passes but you will probably want to use it if you are 
pointing the antenna in a fixed direction for testing:

>>> sch = RPCSchedulerClient(schedule=s, rpcaddr='http://rpc.mygroundstation.com:8000', track_full_pass=True, compute_ant_points=False)

Module Reference
----------------
"""

import sys

if sys.version_info >= (3,):
    basestring = str

import pandas as pd
from pandas import DataFrame
import numpy as np
import json
import ephem
import os
from .rpc import RPCClient
import logging
log = logging.getLogger('libgs_ops-log')
log.addHandler(logging.NullHandler())



class Error(Exception):
    """ Generic Exception """
    pass

#: Default buffertime
SCHEDULE_BUFFERTIME = 180



class Action(dict):
    """
    Actions are just a list and/or dict
    of parameters that will be passed unmodified to the protocol.

    It can be useful if issuing non-standard commands (ie not bytearrays)
    to the protocol class for whatever reason.
    """

    def __init__(self, args, kwargs={}, desc = "unnamed",  retries=0):
        """

        Args:
            args (list or tuple):       A list of arguments to pass to the protocol's 
                :meth:`~libgs.protocols.protocolbase.ProtocolBase.do_action` method as positional arguments
            kwargs (dict):              A dictionary to pass to the protocol's 
                :meth:`~libgs.protocols.protocolbase.ProtocolBase.do_action` method as kwargs.
            desc (str(optional)):       The description of the action
            retries (int(optional)):    The number of times to retry the action in case of failure.

        .. note::

            It is discouraged to use any positional arguments in the do_action function besides one, which is the
            action selector. Then use kwargs for anything else. See  :class:`libgs.protocols.protocolbase.ProtocolBase` for additional
            information on this topic.
        """

        if isinstance(args, list):
            args = tuple(args)

        if not isinstance(args, tuple):
            raise Error('args must be a tuple, not %s'%(type(args)))
        if not isinstance(kwargs, dict):
            raise Error('kwargs must be a dict, not %s'%(type(args)))

        self['desc'] = desc
        self['args'] = args
        self['kwargs'] = kwargs

        # Make something persist through the pass by setting retries to be
        # realy large, and allow the user to say retries=-1 for convenience.
        if retries < 0:
            retries =  10000000

        self['retries'] = int(retries)


        try:
            json.dumps(self)
        except TypeError as e:
            raise Error("All arguments to Action have to be json-serializable objects. Refer to python documentation (%s)", e)

    def __str__(self):
        return("Action: %s <%s, %s> (%d retries)"%(self['desc'], self['args'], self['kwargs'], self['retries']))

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        """
        Convert the action to python dictionary format

        Returns:
            A dictionary

        """
        return dict(self)

class Communication(dict):
    """
    This class holds the message (fully encoded) that is sent to the
    satellite.

    It is just a convenience class that wraps and populates a dictionary
    properly for use by the other classes in this module.

    It can be constructed with either a HEX string or a bytearray and will automatically compute the other. After construction
    it will be a dictionary with the following fields:

      * hexstr: Hex representation of byte stream
      * barray: :class:`bytearray` represenation of bytestream
      * retries: Number of retries
      * wait:    Whether to wait for reply


    """

    def __init__(self,cmd, retries=3, wait = True):
        """

        Args:
            cmd (basestring or bytearray): Command string (fully encoded) to send to satellite.
            retries (int): Number of times the command should be retried in case of failure
            wait (bool): Whether the ground station should wait for a reply from the satellite or not.

        """

        if isinstance(cmd, basestring):
            self._check_cmdstr(cmd)
            hexstr = cmd
            barray = bytearray([int(x, 16) for x in cmd.split('-')])
        elif isinstance(cmd, bytearray):
            hexstr = '-'.join(["%02X"%(x) for x in cmd])
            barray = cmd
        elif isinstance(cmd, Communication):
            hexstr = cmd['hexstr']
            barray = cmd['barray']
        else:
            raise Error('Unsupported argument : %s -  %s'%(cmd, type(cmd)))


        if type(retries) != int or retries < 0:
            raise Error("Retries must be an integer > 0")

        self['barray'] = barray
        self['hexstr'] = hexstr
        self['retries'] = retries
        self['wait'] = wait


    def _check_cmdstr(self, cmd):
        """
        Verify that the command string is in the right format

        """
        valid = '0123456789ABCDEF-'

        # do some input checking
        # cmd must be in format XX-XX-XX-XX
        #
        if not (np.array([len(s) for s in cmd.split('-')])  == 2).all():
            raise Error("cmd srting must be in the format XX-XX-XX-XX")

        if not (np.array([a in valid for a in cmd]).all()):
            raise Error("cmd string invalid hex")


    def to_dict(self):
        """
        Convert the class to a serialisable python dictionary format (gets rid of the bytearray entry).

        Returns:
            A serialisable dictionary

        """
        # Turn to serialisable dict... we get rid of bytearray entry.
        c = dict(hexstr=self['hexstr'], retries=self['retries'], wait=self['wait'])
        return c




class CommsPass(object):
    """
    Class to hold a communications pass.

    A CommsPass is defined as a pass data (az, el, range_rate) schedule with associated set of :class:`communications <.Communication>` 
    and :class:`actions <.Action>`.

    Arbitrary metadata (must be picklable) can also be added to the object.

    """

    _metadata = None

    def __init__(self, pass_data, desc=None, nid=None, horizon=0, comms=[], listen=False, **kwargs):
        """
        Args:
            pass_data (:class:`~pandas.DataFrame`): Dataframe with at least az, el, range_rate columns
            nid (int)               : Norad ID to associate with pass. Can be left empty if pass_data has a .nid field.
            horizon (float)         : The lowest acceptable elevation for the pass. Pass_data will be cropped to the horizon
            comms (list, optional)  : List of communications (can be added with add_communications instead)
            listen (bool, optional) : Whether it is a listen pass or not
            tle (str, optional)     : The TLE used for computing pass_data
            protocol (str, optional): The protocol to use during the pass
            **kwargs                : Any other key=value pair to pass to scheduler to be logged (added to the metadata)

        """
        # NOTE: Internally, picklable arguments (i.e. everything except pass_data and comms) are
        #       stored in metadata dictionary so it can be easily converted
        #       to dict/json, regardless of what is being passed.

        #initialising _metadata attribute is a bit tricky since we have overloaded __setattr__
        object.__setattr__(self, '_metadata', {})

        if not ('az' in list(pass_data.keys()) and 'el'in list(pass_data.keys()) and 'range_rate' in list(pass_data.keys()) and 'tstamp_str'in list(pass_data.keys())):
            #print(pass_data.head())
            raise Error('Pass_data must be a dataframe with at least "az", "el", "range_rate" and "tstamp_str" columns')

        # Initiate named metadata fields) - afterwareds we can access with . operator
        self.metadata['nid'] = None #<--- initialise metadata - will then be set correctly with .nid access immediately below
        self.metadata['listen'] = listen
        self.metadata['horizon'] = horizon
        self.metadata['desc'] =  desc
        
        if hasattr(pass_data, 'TLE') and 'tle' not in list(kwargs.keys()):
            self.metadata['tle'] = pass_data.TLE


        #
        # Check NID
        #
        if nid is None:
            if hasattr(pass_data, 'nid'):

                if 'norad_id' in list(pass_data.keys()):
                    pd_nid = pass_data.norad_id.unique()
                    if (len(pd_nid) != 1) or (pd_nid[0] != pass_data.nid):
                        raise Error("nid is set as an attribute on pass_data and also as a norad_id column, but there is a mismatch")

                self.nid=pass_data.nid

            elif 'norad_id' in list(pass_data.keys()):
                pd_nid = pass_data.norad_id.unique()
                if len(pd_nid) != 1:
                    raise Error("norad_id column is available in pass_data, but not unique - it should be")

                self.nid = pd_nid[0]
            else:
                raise Error("Norad ID (nid) is needed, but is not available in pass data or passed as an argument")
        else:
            self.nid = nid


        self.nid = int(self.nid)  # <--- ensure we dont get any funny numpy integer types

        #
        # Check timestamp
        #
        try:
            tstamps = [ephem.Date(pd.to_datetime(s)) for s in pass_data.tstamp_str]
        except Exception as e:
            raise Error("Badly formatted date(s) in pass_data.tstamp_str: %s"%(e))

        pass_data.index = tstamps
        pass_data.tstamp_str = [str(s) for s in tstamps]

        # Crop data to only contain waht is above the horizon
        pass_data = pass_data[pass_data.el >= self.horizon]

        if pass_data.empty:
            raise Error('Pass never comes above visibility horizon')

        # While strictly not necessay, not curating what gets stored in the commspass
        # makes it difficult to do automated testing. So this will need to be edited
        # if in the future we need anything more
        pass_data = pass_data[['tstamp_str', 'az', 'el', 'range_rate']]

        self.pass_data = pass_data
        self.comms = []

        for comm in comms:
            self.add_communication(comm)

        # Add any additional metadata fields
        self.metadata.update(kwargs)


    # This private method is included for backwards compatability only.
    def _change_time(self, tstamp):
        self.change_time(tstamp)


    def change_time(self, tstamp):

        """
        Modify the pass data start time.

        If you run this the pass will not correspond to a real satellite pass anymore, but it is an extremely useful function when
        testing an upcoming pass in a dry-run.

        Example:

        >>> cp.change_time('2019-11-01 12:32:42')

        Will modify the commspass pass data so that it starts at ``2019-11-01 12:32:42``. Everything else stays the same.

        Args:
            tstamp: New timestamp (in any format supported by :class:`ephem.Date`, for example ISO string, or a python :class:`datetime.datetime`)
        """
        curt =  self.pass_data.index[0]
        newt = ephem.Date(tstamp)

        dt = (newt-curt)
        newindex = pd.Series(self.pass_data.index + dt)


        s = newindex.apply(lambda x: str(ephem.Date(x))).tolist()


        new_pass_data = DataFrame(\
            index=self.pass_data.index + dt,
            data = dict(
                tstamp_str = s,
                az = self.pass_data.az.tolist(),
                el = self.pass_data.el.tolist(),
                range_rate = self.pass_data.range_rate.tolist()))

        self.pass_data = new_pass_data






    def __str__(self):
        s = "Communication Pass:\n"
        s += "  Norad ID:       %s\n"%(self.nid)
        s += "  Description:    %s\n"%(self.desc)
        s += "  Visib. horizon: %d\n"%(self.horizon)
        s += "  Pass start:     %s\n"%(self.pass_data.tstamp_str.iloc[0])
        s += "  Pass end:       %s\n"%(self.pass_data.tstamp_str.iloc[-1])
#        for k,v in self._metadata.items():
#            s += "  {:16s}{:s}\n".format(str(k),str(v))

        s += "  Scheduled comms:\n"

        if self.listen:
            s += "   (listen mode)\n"
        elif len(self.comms) == 0:
            s += "   (no comms added but NOT listen mode)"

        for k,v in enumerate(self.comms):

            if v['retries'] > 99:
                retrstr = '(%10s)'%(v['retries'])
            else:
                retrstr = '(%2d retries)'%(v['retries'])


            if isinstance(v, Action):
                s += "   %3d %s : '%s' <%s, %s>\n"%(k, retrstr, v['desc'],  v['args'], v['kwargs'])
            else:
                if v['wait']:
                    s += ("   %3d %s : %s\n"%(k, retrstr,v['hexstr']))
                else:
                    s += ("   %3d (no wait)    : %s\n"%(k, v['hexstr']))

        return(s)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """

        x == y should be true if everything is identical

        """

        try:
            eq = [\
                self.nid == other.nid,
                self.desc == other.desc,
                (self.pass_data == other.pass_data).all().all(),
                self.horizon == other.horizon,
                self.comms == other.comms,
                self._metadata == other._metadata]
        except ValueError:
            return False

        return all(eq)

    def overlaps(self, other, buffertime=0.0):
        """
        Check if current pass overlaps with another pass.

        By overlap is meant that the other pass begins within a
        defined buffertime of the current pass finishing.

        Args:
            other (:class:`.CommsPass`): The pass to compare with
            buffertime (float):         The time in seconds to allow as a minimum between passes

        """
        rt0 = pd.to_datetime(self.pass_data.iloc[0].tstamp_str)
        st0 = pd.to_datetime(self.pass_data.iloc[-1].tstamp_str)
        rt1 = pd.to_datetime(other.pass_data.iloc[0].tstamp_str)
        st1 = pd.to_datetime(other.pass_data.iloc[-1].tstamp_str)

        btime = pd.Timedelta(seconds = buffertime)

        if (   ((rt0 < rt1) and ((st0 + btime) < rt1))
            or ((rt1 < rt0) and ((st1 + btime) < rt0))):
                return False
        else:
            return True

    def __cmp__(self,other):
        return cmp(self.pass_data.index[0],other.pass_data.index[0])


    @property
    def metadata(self):
        """
        Dictionary of metdata associated with the Communication Pass
        """
        return self._metadata


    def __getattr__(self, key):
        """
        Make it possible to access metadata directly through . operator
        """
        try:
            return self.metadata[key]
        except KeyError:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, key))

    def __setattr__(self, key, val):
        """
        Make it possible to access metadata directly through . operator
        """
        if key in list(self.metadata.keys()):
            self.metadata[key] = val
        else:
            object.__setattr__(self, key, val)


    #
    # Add some helper methods to make the class pickle-able
    # It doesnt work out of the box because of our fiddling with __getattr__ and __setattr__
    # So we will make it use by keeping the state as the dict version instead.
    #
    def __getstate__(self):
        return self.to_dict()

    def __setstate__(self, state):
        object.__setattr__(self, '_metadata', {})
        cp = CommsPass.from_dict(state)
        self._metadata = cp._metadata
        self.pass_data = cp.pass_data
        self.comms     = cp.comms
    ########################################################



    def add_communication(self, comm, **kwargs):
        """
            Add a communication to the pass. 
            
            The communication can be supplied either as a string of HEX-pairs, 
            as a bytearray, or as a Communications object.

            If a HEX string or a bytearray is supplied, it will be converted to a
            Communication object internally

        Args:
            comm:       The communication to add (either a hex string ``"AB-CD-01-..."``,  a :class:`.Communication` object or 
                        an :class:`Action` object
            **kwargs:   Extra arguments passed to :class:`.Communication` constructor in case comm is a hex string.

        Returns:
            None

        """

        if isinstance(comm, Communication):
            if len(kwargs) > 0:
                raise Error("No kwargs expected for Communication object, got %s"%(kwargs))

            self.comms.append(comm)

        elif isinstance(comm, Action):
            if len(kwargs) > 0:
                raise Error("No kwargs expected for Action object, got %s"%(kwargs))

            self.comms.append(comm)


        elif isinstance(comm, basestring) or isinstance(comm, bytearray):
            self.comms.append(Communication(comm, **kwargs))
        else:
            raise Error("Invalid type for comms object: %s"%(type(comm)))



        if self.listen:
            log.info("Cannot use listen mode when communicating. listen mode disabled")
            self.listen = False


    def plot(self):
        """
        Visualise the pass. 
        
        **Not currently implemented**
        """
        raise Error("Not implemented")


    def to_dict(self):
        """
        Convert class to a python dictionary.
        """

        d = dict(
            pass_data = self.pass_data.to_dict(),
            comms = [c.to_dict() for c in self.comms],
            _metadata = self._metadata)

        return (d)

    def copy(self):
        """
        Create a copy of the class instance.
        """
        return(CommsPass.from_dict(self.to_dict()))

    @classmethod
    def from_dict(self, d):
        """
        Classmethod to create CommsPass object from a python dict.

        Usage:

        >>> cp = CommsPass.from_dict(dict_repr)

        Args:
            d (dict): dictionary representation of CommsPass

        """

        pass_data = DataFrame(d['pass_data'], columns = ['tstamp_str', 'az', 'el', 'range_rate'])
        pass_data.index = pass_data.index.astype(float)
        comms = d['comms']

        #################################
        # Allow backwards compatability
        # TODO: Remote and replace with just:
        # _metadata = d['_metadata']
        #
        _metadata = d.copy()
        del _metadata['comms']
        del _metadata['pass_data']

        if '_metadata' in list(d.keys()):
            del _metadata['_metadata']
            _metadata.update(d['_metadata'])
        #################################


        cpass = CommsPass(pass_data, **_metadata)
        for k,c in enumerate(comms):
            if 'args' in list(c.keys()) and 'kwargs' in list(c.keys()) and 'desc' in list(c.keys()) and 'retries' in list(c.keys()):
                cpass.add_communication(Action(c['args'], c['kwargs'], retries=c['retries'], desc=c['desc']))
            elif 'hexstr' in list(c.keys()) and 'retries' in list(c.keys()) and 'wait'in list(c.keys()):
                cpass.add_communication(c['hexstr'], retries=c['retries'], wait=c['wait'])
            else:
                raise Error("Invalid dict input to from_dict. Expected either Action or Communication in dict form, got %s"%(c))

        return cpass

    def to_json(self):
        """
        Convert the class to JSON representation.
        """
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    @classmethod
    def from_json(self, data):
        """
        Classmethod to Create CommsPass from a json string or from a json file.

        Usage:

        >>> cp = CommsPass.from_dict(json_repr or json_file)

        Args:
            json (fname or string): json string or file to load
        """

        if os.path.isfile(data):
            fp = open(data, 'r')
            data = fp.read()
            fp.close()

        d = json.loads(data)

        return self.from_dict(d)



class Schedule(object):
    """
    Class to hold a schedule of passes

    """

    def __init__(self, passes=[], buffertime = SCHEDULE_BUFFERTIME):
        """
            Args:
                passes (list(CommsPass))    : List of :class:`.CommsPass` objects
                buffertime (int, optional)  : number of seconds to allow, as a minimum between two passes
        """

        #
        # sorting can be disabled, but there is no obvious reason
        # why you would do that. It may also not be safe
        #
        self.sort_passes = True
        self.buffertime = buffertime

        self.passes = []
        for p in passes:
            self.add_pass(p)


    def __str__(self):
        s =  'Schedule of communication passes:\n'
        s += '  ---- -------- -------------------- -------------------- --------------\n'
        s += '  #    Norad id Pass start (utc)     Pass end (utc)       Communications\n'
        s += '  ---- -------- -------------------- -------------------- --------------\n'
        i = 0
        for p in self.passes:
            s += '  %04d %-8s %-20s %-20s %d\n'%(
                i,
                str(p.nid),
                p.pass_data.tstamp_str.iloc[0],
                p.pass_data.tstamp_str.iloc[-1],
                len(p.comms))
            i += 1
        s += '  ---- -------- -------------------- -------------------- --------------\n'
        return(s)

    def __repr__(self):
        return self.__str__()

    def _repr_html_(self):
        rows = []
        for p in self.passes:
            rows += [(p.nid, p.pass_data.tstamp_str.iloc[0], p.pass_data.tstamp_str.iloc[-1], len(p.comms))]

        df = DataFrame(\
            rows,
            columns=['Norad id', 'Pass start (utc)', 'Pass end (utc)', 'Communications'])

        return df._repr_html_()


    def __eq__(self, other):
        """

        x == y should be true if everything is identical

        """
        return (self.__dict__ == other.__dict__)


    def copy(self):
        """
        Create a copy of the Schedule instance.
        """
        return(Schedule.from_dict(self.to_dict()))


    def add_pass(self, tpass):
        """
        Add a pass to the schedule

        Args:
            tpass: The :class:`.CommsPass` instance to add.

        """

        # check for overlap. Raises exception if overlap
        self._check_overlap(tpass)

        #if all good, add
        self.passes.append(tpass)

        if self.sort_passes == True:
            self.passes.sort(key=lambda p : p.pass_data.index[0])

    def remove_pass(self, tpass):
        """
        Remove a :class:`.CommsPass` instance from the schedule

        Args:
            tpass (:class:`.CommsPass`): The instance to remove

        """
        self.passes.remove(tpass)

    def pop_pass(self, index=[]):
        """
        Pop the n'th pass from the schedule

        Args:
            index (int): The index (or list of indexes) to pop

        """
        self.passes.pop(index)

    def _check_overlap(self, tpass):

        if any([tpass.overlaps(x, buffertime=self.buffertime) for x in self.passes]):
            raise Error("Can't add pass as it overlaps with another pass in the schedule")


    def to_dict(self):
        """
        Convert schedule to its python dictionary representation
        """
        d = dict(
            passes = [p.to_dict() for p in self.passes],
            sort_passes = self.sort_passes,
            buffertime = self.buffertime)

        return(d)

    def to_json(self):
        """
        Convert schedule to its json  representation
        """

        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


    @classmethod
    def from_dict(self, d):
        """
        Classmethod to Create Schedule object from a python dictionary representation of the schedule

        Args:
            d (dict): dictionary representation of schedule

        """
        passes = [CommsPass.from_dict(x) for x in d['passes']]
        s = Schedule(passes, d['buffertime'])
        s.sort_passes = d['sort_passes']
        return(s)

    @classmethod
    def from_json(self, data):
        """
        Classmethod to create Schedule from a json string or from a json file.

        Args:
            json (fname or string): json string or file to load
        """

        if os.path.isfile(data):
            fp = open(data, 'r')
            data = fp.read()
            fp.close()

        d = json.loads(data)

        return self.from_dict(d)



class RPCSchedulerClient(object):
    """
    The RPCSchedulerClient class connects to a remote scheduler and allows basic interaction with it to
    upload/start/stop schedules.

    For futher information see :class:`libgs.scheduler.Scheduler`

    """

    def __init__(self, schedule, track_full_pass=True, compute_ant_points = True, rpcaddr='http://localhost:8000'):
        """

        Args:
            schedule:           The schedule to execute
            track_full_pass:    If True (default), a pass will be tracked to its end even when the communications are finished.
            compute_ant_points: If True (default), libgs will intelligently decide when to move the antenna based on its beamwidth.
                                Otherwise the schedule will be followed slavishly.
            rpcaddr:            The XMLRPC address of the remote. For example: http://some.address.com:8000
        """
        self._rpcaddr =  rpcaddr
        self._track_full_pass = track_full_pass
        self._compute_ant_points = compute_ant_points
        self.server = RPCClient(self._rpcaddr, allow_none=True)
        self._schedule = schedule

    @property
    def state(self):
        """
        Get current scheduler state from remote
        """
        return self.server.scheduler_state()


    def execute(self, N=None):
        """
        Execute the schedule on the remote

        Args:
            N (optional) : Only execute at most N entries

        """

        self.server.execute_schedule(self._schedule.to_json(), self._track_full_pass, self._compute_ant_points, N)

    def stop(self):
        """
        Stop the scheduler on the remote
        """
        self.server.stop_schedule()

    def enable(self):
        """
        Re-enable a disabled scheduler on the remote
        """
        self.server.enable()

    def disable(self):
        """
        Disable a scheduler on the remote. It will not be possible to send it schedules or execute schedules before
        it is re-enabled.
        """
        self.server.disable()



if __name__ == '__main__':

    if 1:
        import sys
        log.setLevel(logging.INFO)

        ch = logging.StreamHandler(sys.stdout)
        #
        # Attributes can be found here: https://docs.python.org/2/library/logging.html#logrecord-attributes
        #
        formatter = logging.Formatter('%(asctime)s - %(levelname)5s - %(module)10s - "%(message)s"')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        log.addHandler(ch)


