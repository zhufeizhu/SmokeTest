#!/usr/bin/env python
# Copyright 2019 The Bytedance Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import argparse
import logging
import os
import shutil
import sys
import signal
import parse.icustomerunner

class SmokeTestRunner(parse.icustomerunner.ICustomRunner):
    successnum = 0
    failedNum = 0
    TaskNum = 0

    def __init__(self, taskInfo, uiDriver):
        parse.icustomerunner.ICustomRunner.__init__(self, taskInfo, uiDriver)

    def install_apk(self):
        Debug_Apk_DownloadUrl = self.taskInfo.custom['Debug_Apk_DownloadUrl']
        AndroidTest_Apk_DownloadUrl = self.taskInfo.custom['AndroidTest_Apk_DownloadUrl']
        Debug_Apk_Path = self.downloadFiles(Debug_Apk_DownloadUrl, 'app-debug.apk')
        AndroidTest_Apk_Path = self.downloadFiles(AndroidTest_Apk_DownloadUrl,'app-debug-androidTest.apk')
        self.installThirdApk(Debug_Apk_Path)
        self.installThirdApk(AndroidTest_Apk_Path)
        return 0

    def run_ut(self,test_class,test_case):
        self.TaskNum = self.TaskNum + 1
        run_cmd = 'am instrument -w -r   -e debug false -e class \'com.bytedance.ttwebview.shell.%s#%s\' com.bytedance.ttwebview.shell.test/android.support.test.runner.AndroidJUnitRunner' % (test_class,test_case)
        msg = self.uiDriver.adb.shell(run_cmd)
        ret = msg.find("OK (1 test)")
        if ret != -1:
            self.successnum = self.successnum + 1
        else:
            self.failedNum = self.failedNum + 1
        self.log(msg)
        return 0

    def testSmoke(self):
        self.install_apk()
        test_class = 'SmokeTest'
        smoke_ut = [
            'prepare_Smoke',
            'Smoke_Test_Load',
            'Smoke_Test_Download',
            'Smoke_Test_LoadUrl'
        ]
        test_so_amount = self.taskInfo.custom['test_so_amount']
        i = 0
        while i <= test_so_amount:
            if i == 0:
                self.run_ut(test_class,smoke_ut[0])
            self.run_ut(test_class,smoke_ut[1])
            if i != test_so_amount:
                self.run_ut(test_class,smoke_ut[2])
            self.run_ut(test_class,smoke_ut[3])
            i = i + 1

        logInfo={}
        logInfo['taskName'] = self.taskInfo.taskName
        logInfo['taskDeviceID'] = self.taskInfo.taskDevId
        lgoInfo['task'] = '%d tests runs' % self.TaskNum
        logInfo['Passed'] = '%d tests ' % self.successnum
        logInfo['lodUrl'] = self.logFileName
        self.sendLark(logInfo,groupReceiverId=self.taskInfo.custom['groud_id'])





