#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
logger.py - Takes a command, executes it, and displays its live stderr and stdout in a Tkinter window.
Has options for writing output to txt, and can be told of any temproary directory that the command
uses for proper cleanup.
"""

from __future__ import absolute_import
from __future__ import print_function
from six.moves.tkinter import *
from six.moves.queue import Queue
import threading
import re
import os
import signal
import subprocess
import time
import platform
import shutil
import sys
import traceback
import argparse

# Takes a command and displays its stdout and stderr as its running.  Used by most of the Argus programs to display progress.
class Logger(Tk):
    def __init__(self, cmd, tmp = '', wLog = False, doneButton = True):
        print('Changing stuff...')
        Tk.__init__(self)
        self.cmd = cmd
        self.tmp = tmp
        self.wLog = wLog
        self.doneButton = doneButton
        # create a done button and connect the close window command to its command to ensure cleanup
        self.dButton = Button(self, text = 'Cancel', command = self.wereDoneHere)
        self.q = Queue()
        self.id = None

        scrollbar = Scrollbar(self, width = 20)
        scrollbar.pack(side=RIGHT, fill=Y, padx = 10, pady = 10)
        self.log = Text(self, yscrollcommand = scrollbar.set, bg = "black", fg = "green")
        scrollbar.config(command=self.log.yview)
        self.t = ThreadCommand(self.q, command=self.cmd)

        # start thread that will wait for data
        self.t.daemon = True
        self.t.start()

        # make text updater class which is called every 100 ms to make sure everything can be seen in the log
        self.T = TextUpdater(self.t, self.q, self, self.log, self.wLog)

    # Kill everything, if were done that is
    def wereDoneHere(self):
        self.t.kill()
        if self.tmp != '':
            if os.path.isdir(self.tmp):
                shutil.rmtree(self.tmp)
        if self.wLog:
            self.T.fo.close()
        self.cancel()
        self.destroy()

    def cancel(self):
        if self.id is not None:
            print('Canceling...')
            self.after_cancel(self.id)

    # if the subprocess is done, change the label of the exit button from 'cancel' to 'done'
    def checkButton(self):
        if self.t.getStatus() is not None:
            self.dButton.configure(text = 'Done')
            self.update_idletasks()
            self.t.timeToChill = True
        else:
            try:
                self.id = self.after(100, self.checkButton)
            except:
                pass

    # start the subprocess and begin monitoring its stdout
    def start(self):
        self.resizable(width=FALSE, height=FALSE)
        self.wm_title('Log')

        # pack the log and tell the user where we're writing the log file if it's being written
        self.log.pack()
        if self.wLog:
            self.log.insert(END, 'Writing log file to: ' + os.getcwd() + '\n')

        self.log.insert(END, 'Build info: \n' + platform.platform() + " " + platform.machine() + '\n')

        if self.doneButton:
            self.dButton.pack()
        self.protocol('WM_DELETE_WINDOW', self.wereDoneHere)
        self.update_idletasks()
        self.after(100, self.T.update_text)
        self.after(100, self.checkButton)
        self.mainloop()

class ThreadCommand(threading.Thread):
    """
    run a command in its own thread
    """
    def __init__(self, queue, fetchfn=None, command=None):
        threading.Thread.__init__(self)
        self.queue = queue
        self.command = command
        self.fetchfn = self.read_buffer
        self.running = False
        self.proc = None
        self.timeToChill = False

    # read the stdout one character at a time
    def read_buffer(self, master):
        last_part = b""
        nl = re.compile(b'(\n)')
        while self.running:
            s = last_part
            try:
                s += os.read(master,1)
                s = s.replace(b'\r',b'') # \r shows up as music notes in tk (at least on linux)
                lines = nl.split(s)
                last_part = lines[-1]
                if not last_part:
                    data = b''.join(lines)
                else:
                    data = b''.join(lines[:-1])
                yield (True, data)
            except Exception as e:
                yield (False, b'')
                traceback.print_exc()
            if self.timeToChill:
                time.sleep(0.01)

    def getStatus(self):
        if self.proc is not None:
            return self.proc.poll()

    def run(self):
        self.running = True
        startupinfo = None
        if sys.platform == "win32" or sys.platform == "win64": # Make it so subprocess brings up no console window
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # Start the process
        self.proc = subprocess.Popen(self.command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = False, startupinfo = startupinfo)
        # Start getting data from the pipe and putting each line in a queue
        more_data = True
        for more_data, lines in self.fetchfn(self.proc.stdout.fileno()):
            if lines:
                # send the received data into the queue
                self.queue.put(lines)
            if not more_data:
                # time to close ourselves down
                print('We closed')
                self.running = False
                break
    def kill(self):
        try:
            self.proc.kill()
        except:
            print('Could not kill!')
            pass
        self.running = False
        return

# these classes were pulled from the internet under MIT license and modified to make them Windows friendly and freezable
class TextUpdater(object):
    def __init__(self, the_thread, the_queue, root, textwidget, wLog):
        self.the_thread = the_thread
        self.the_queue = the_queue
        self.textwidget = textwidget
        self.root = root
        if wLog:
            self.fo = open("Log--" + time.strftime("%Y-%m-%d-%H-%M") + ".txt", "wb")
        else:
            self.fo = None
        self.linecount = 0

    def update_text(self):
        while self.the_thread.running:
            # Argus specific stuff we don't want to show
            bad_phrases = ['iters','it/s', 'InsecureRequestWarning', 'axes3d.py', 'Python', '_createMenuRef', '0x', 'ApplePersistenceIgnoreState', 'self._edgecolors', 'objc', 'warnings.warn', 'UserWarning']
            try:
                self.root.update()
            except:
                pass
            try:
                # try to get data from the queue and write it to the text widget
                line = self.the_queue.get(timeout=0.2)
                # Delete line with bad phrase as they pop up
                for phrase in bad_phrases:
                    if phrase in line.decode('utf-8'):
                        self.textwidget.delete(str(self.linecount), str(self.linecount + 1))

                self.textwidget.insert(END,line.decode('utf-8'))
                if self.fo:
                    self.fo.write(line.decode('utf-8'))
                self.linecount += 1
                self.textwidget.see(END)
                self.textwidget.update_idletasks()
                self.root.update()
            except:
                pass

