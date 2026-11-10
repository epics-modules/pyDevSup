import devsup.ptable as PT
from devsup.ptable import _ONPROC
from devsup.hooks import addHook
from devsup import NO_ALARM, MINOR_ALARM, MAJOR_ALARM, INVALID_ALARM, READ_ALARM, WRITE_ALARM
from devsup.db import getRecord
import signal
import sys
import numpy as np
from threading import Thread, Event, Lock


class AlarmTest(PT.TableBase):
    # Output paramaters
    calcout = PT.Parameter()
    aao = PT.Parameter()
    ao = PT.Parameter()
    bo = PT.Parameter()
    int64out = PT.Parameter()
    longout = PT.Parameter()
    lso = PT.Parameter()
    mbbo = PT.Parameter()
    mbboDirect = PT.Parameter()
    stringout = PT.Parameter()
    
    # Input parameters
    aai = PT.Parameter(iointr=True)
    ai = PT.Parameter(iointr=True)
    bi = PT.Parameter(iointr=True)
    int64in = PT.Parameter(iointr=True)
    longin = PT.Parameter(iointr=True)
    lsi = PT.Parameter(iointr=True)
    mbbiDirect = PT.Parameter(iointr=True)
    mbbi = PT.Parameter(iointr=True)
    stringin = PT.Parameter(iointr=True)
    waveform = PT.Parameter(iointr=True)

    def __init__(self, name):
        super().__init__(name=name)
        self.stop = False
        self.odd_alarm = False
        self.count = None
        self.onproc_event = Event()
        self.calcout.addAction(self.proc_out_calcout, _ONPROC)
        self.aao.addAction(self.proc_out_aao, _ONPROC)
        self.ao.addAction(self.proc_out_ao, _ONPROC)
        self.bo.addAction(self.proc_out_bo, _ONPROC)
        self.int64out.addAction(self.proc_out_int64out, _ONPROC)
        self.longout.addAction(self.proc_out_longout, _ONPROC)
        self.lso.addAction(self.proc_out_lso, _ONPROC)
        self.mbboDirect.addAction(self.proc_out_mbboDirect, _ONPROC)
        self.mbbo.addAction(self.proc_out_mbbo, _ONPROC)
        self.stringout.addAction(self.proc_out_stringout, _ONPROC)
        self.inp_list = [self.aai, self.ai, self.bi, self.int64in, self.longin, self.lsi, self.mbbiDirect, self.mbbi, self.stringin, self.waveform]
        self.run_thread = Thread(target=self._run)

    def start(self):
        self.run_thread.start()

    def stop_threads(self):
        print("stopping threads")
        self.stop = True
        self.onproc_event.set()
        self.run_thread.join()

    def set_alarm(self, PV):
        """
        This method sets the alarm status on two PVs in alternation.
        These two PVs would be either the inputs and driven from the _run thread,
        or output PVs and driven from the onproc method(s).
        """
        if self.count is None:
            return
        odd_number = bool(self.count % 2)
        if PV is not None:
            if odd_number == self.odd_alarm:
                PV.alarm = MAJOR_ALARM
                if self.odd_alarm:
                    PV.amsg = "odd number"
                else:
                    PV.amsg = "even number"
                if self.calcout.value is not None and self.calcout.value > 10:
                    # Just to show that other alarm status values than COMM are possible.
                    PV.stat = READ_ALARM
            else:
                PV.alarm = NO_ALARM
                PV.amsg = None
        self.odd_alarm = not self.odd_alarm
        
    def _run(self):
        while True:
            if self.onproc_event.wait():
                self.onproc_event.clear()
            if self.stop:
                break
            if self.calcout.value is None:
                continue
            
            self.aai.value = [self.count]
            # Note that the RVAL field for the AI type does not accept float values
            # as it is aimed at use by A to D converters.
            self.ai.value = self.count
            self.bi.value = self.count % 2
            self.int64in.value = self.count
            self.longin.value = self.count
            self.lsi.value = str(self.count)
            self.mbbiDirect.value = self.count
            self.mbbi.value = self.count % 16      # 0..15 values available
            self.stringin.value = str(self.count)
            self.waveform.value = [self.count]
            self.odd_alarm = False
            for PV in self.inp_list:
                self.set_alarm(PV)
                #print(PV.name, PV.value, type(PV.value), PV.alarm)
                PV.notify()
            
    def proc_out_calcout(self):
        """
        This method is called in response to timer scanning within the database scan.
        This drives the application timing.
        """
        if self.calcout.value is not None:
            self.count = round(self.calcout.value)
        if self.count is not None:
            self.odd_alarm = False
            self.set_alarm(self.calcout)
            #self.onproc_event.set()
            aao = getRecord("AAO")
            if aao.scan is not None:
                aao.VAL = [self.count]
                # The record needs to be scanned to update the scan status.
                aao.scan(sync=False, force=0)

    def proc_out_aao(self):
        self.set_alarm(self.aao)
        ao = getRecord("AO")
        if ao.scan is not None and self.count is not None:
                # Note that the RVAL field for the AO type does not accept float values
                # as it is aimed at use by A to D converters
            ao.VAL = float(self.count)
            ao.scan(sync=False, force=0)

    def proc_out_ao(self):
        self.set_alarm(self.ao)
        bo = getRecord("BO")
        if bo.VAL is not None and self.count is not None:
            bo.VAL = self.count % 2
            bo.scan(sync=False, force=0)

    def proc_out_bo(self):
        self.set_alarm(self.bo)
        int64out = getRecord("INT64OUT")
        if int64out.VAL is not None and self.count is not None:
            int64out.VAL = self.count
            int64out.scan(sync=False, force=0)

    def proc_out_int64out(self):
        self.set_alarm(self.int64out)
        longout = getRecord("LONGOUT")
        if longout.VAL is not None and self.count is not None:
            longout.VAL = self.count
            longout.scan(sync=False, force=0)

    def proc_out_longout(self):
        self.set_alarm(self.longout)
        lso = getRecord("LSO")
        if lso.VAL is not None and self.count is not None:
            lso.VAL = str(self.count)
            lso.scan(sync=False, force=0)

    def proc_out_lso(self):
        self.set_alarm(self.lso)
        mbboDirect = getRecord("MBBODIRECT")
        if mbboDirect.VAL is not None and self.count is not None:
            mbboDirect.VAL = self.count
            mbboDirect.scan(sync=False, force=0)
        
    def proc_out_mbboDirect(self):
        self.set_alarm(self.mbboDirect)
        mbbo = getRecord("MBBO")
        if mbbo.VAL is not None and self.count is not None:
            mbbo.VAL = self.count % 16      # 0..15 values available
            mbbo.scan(sync=False, force=0)
        
    def proc_out_mbbo(self):
        self.set_alarm(self.mbbo)
        stringout = getRecord("STRINGOUT")
        if stringout.VAL is not None and self.count is not None:
            stringout.VAL = str(self.count)
            stringout.scan(sync=False, force=0)
        
    def proc_out_stringout(self):
        self.set_alarm(self.stringout)
        self.onproc_event.set()
        
def build():
    sup = AlarmTest(name="alarm")

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    addHook('AfterIocRunning', sup.start)
    addHook('AtIocExit', sup.stop_threads)

    return sup
