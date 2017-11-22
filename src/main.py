#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import sys

class KDEInstance:
    def execute(self, cmd, options=[], data=''):
        optionsData = []
        for o in options:
            if type(o) == tuple:
                a, b = o
                optionsData.append(a)
                optionsData.append(b)
            else:
                optionsData.append(o)
        callList = ['loginctl', ' '.join(optionsData), cmd, data]
        callList = [x for x in callList if x != '']
        call = ' '.join(callList)
        out = os.popen(call).read().splitlines()
        return(out)

    def readTable(self, rawData):
        tableData = []
        for rawLine in rawData:
            line = []
            for word in rawLine.split(' '):
                if word == '':
                    continue
                line.append(word)
            if line != []:
                tableData.append(line)
        tableData.pop()
        data = []
        header = tableData[0]
        for line in tableData[1:]:
            assert(len(line) <= len(header))
            lineData = {}
            for i in range(len(line)):
                lineData[header[i]] = line[i]
            data.append(lineData)
        return(data)

    def listSessions(self):
        return(self.readTable(self.execute('list-sessions')))

    def listUsers(self):
        return(self.readTable(self.execute('list-users')))

    def lockSession(self, sid):
        self.execute('lock-session', data=str(sid))

    def unlockSession(self, sid):
        self.execute('unlock-session', data=str(sid))

    def findUserSessions(self, name):
        data = self.listSessions()
        sessions = []
        for session in data:
            if session['USER'] == name:
                sessions.append(int(session['SESSION']))
        return(sessions)

    def userLockAllSessions(self, name):
        sessions = self.findUserSessions(name)
        for session in sessions:
            self.lockSession(session)

    def userUnlockAllSessions(self, name):
        sessions = self.findUserSessions(name)
        for session in sessions:
            self.unlockSession(session)


KDE = KDEInstance()
args = sys.argv
args.pop(0)
try:
    if args[0]=="userLockAll":
        KDE.userLockAllSessions(args[1])
    if args[0]=="userUnlockAll":
        KDE.userUnlockAllSessions(args[1])
except IndexError:
    print("Check arguments!")
