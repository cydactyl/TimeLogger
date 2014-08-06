# Copyright (c) 2014 SwedFTP; All Rights Reserved; See LICENSING
# Copyright (c) 2002 Joergen Cederberg; All Rights Reserved; See LICENSING
from tkinter import *
from datetime import datetime, timedelta
import io
import logging
import time


def main():
    """ Create Tk root widget, and instantiate the TimeLogger widget. """
    logging.basicConfig(
      filename='timelog.log',
      level = logging.DEBUG,
      format='%(asctime)s %(message)s',
      datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    root = Tk()
    app = TimeLogger(master=root)
    app.master.title('TimeLogger')
    app.mainloop()
    app.destroy()


class TimeLogger(Frame):
    """ Implement a timelogging widget. """
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, kw)

        self._start = 0.0
        self._elapsed = 0.0
        self._running = 0

        self._var = {
          'Days': IntVar(),
          'Hours': IntVar(),
          'Minutes': IntVar(),
          'Seconds': IntVar()
        }

        self._label = {}
        self._time = {}

        self.pack()
        self.createWidgets()

    def createWidgets(self):
        """ Create the time labels and control buttons. """
        for key, value in sorted(self._var.items()):
            self._label[key] = Label(self, text=key+': ')
            self._time[key] = Label(self, textvariable=value)
            self._label[key].pack(side=LEFT)
            self._time[key].pack(side=LEFT)

        self._start = Button(
            self, text="Start", command=self.start,
            padx=2, pady=2)
        self._start.pack(side=LEFT, padx=4, pady=4)
        
        self._stop = Button(
            self, text="Stop",
            command=self.stop, padx=2, pady=2)
        self._stop.pack(side=LEFT, padx=4, pady=4)
        
        self._reset = Button(
            self, text="Reset",
            command=self.reset, padx=2, pady=2)
        self._reset.pack(side=LEFT, padx=4, pady=4)

    def _update(self):
        """ Update the labels with the elapsed time. """
        self._elapsed = time.time() - self._start
        self._setTime(self._elapsed)
        self.timer = self.after(50, self._update)

    def _setTime(self, elapsed):
        """ Set the various time values in the self._var Dictionary using timedelta
        Days, Hours, Minutes, Seconds.
        """
        elapsed = timedelta(seconds=elapsed)
        d = datetime(1, 1, 1) + elapsed

        self._var['Days'].set(d.day-1)
        self._var['Hours'].set(d.hour)
        self._var['Minutes'].set(d.minute)
        self._var['Seconds'].set(d.second)

    def start(self):
        """ Start the Timelogger, ignore if running"""
        if not self._running:
            self._start = time.time() - self._elapsed
            self._update()
            self._running = 1
            logging.info('Started.')

    def stop(self):
        """ Stop the TimeLogger, ignore if stopped. """
        if self._running:
            self.after_cancel(self.timer)
            self._elapsed = time.time() - self._start
            self._setTime(self._elapsed)
            self._running = 0
            logging.info('Stopped.')
            logging.info("{'days' : %d, 'hours' : %d, 'minutes' : %d, 'seconds' : %d}" % (self._var['Days'].get(), self._var['Hours'].get(), self._var['Minutes'].get(), self._var['Seconds'].get()))

    def reset(self):
        """ Reset the TimeLogger, Ignore if no time has elapsed."""
        if self._elapsed != 0.0 and not self._running:
            self._start = time.time()
            self._elapsed = 0.0
            self._setTime(self._elapsed)
            logging.info('Reset.')


if __name__ == '__main__':
    main()