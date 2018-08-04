# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import GitHubReminder
import traceback

from MmrzLog import log

#command = r"python {}\GitHubReminder.py".format(sys.path[0])

# if GitHubReminder.github_reminder() returned with not code 0, recall it
# Zhanglin_Github_URL = "https://github.com/zhanglintc?tab=overview&from={0}".format(GitHubReminder.TODAY)
try:
    raise RuntimeError('testError')
    Zhanglin_Github_URL = "https://github.com/zhanglintc"
    for i in range(3):
        if GitHubReminder.github_reminder(GITHUB_URL = Zhanglin_Github_URL, Auto_Commit_Flag = True):
            print('zhanglin failed, try again\n')
        else:
            break
except Exception as e:
    log.e(e)
    exstr = traceback.format_exc()
    log.e(exstr)

# exit after zhanglin, not execute any more
sys.exit()

# # below is WuHong special process...
# Wuhong_Mail_List = [
#     "yaodao5000@yahoo.co.jp",
#     # "zhanglintc623@foxmail.com",
# ]
# Wuhong_Github_URL = "https://github.com/sheriseanes?tab=overview&from={0}".format(GitHubReminder.TODAY)
# for i in range(3):
#     if GitHubReminder.github_reminder(MailList = Wuhong_Mail_List, GITHUB_URL = Wuhong_Github_URL, Auto_Commit_Flag = False):
#         print('wuhong failed, try again\n')
#     else:
#         break


# # below is Houliyuan special process...
# Houliyuan_Mail_List = [
#     "349655336@qq.com",
#     # "zhanglintc623@foxmail.com",
# ]
# Houliyuan_Github_URL = "https://github.com/Pang327?tab=overview&from={0}".format(GitHubReminder.TODAY)
# for i in range(3):
#     if GitHubReminder.github_reminder(MailList = Houliyuan_Mail_List, GITHUB_URL = Houliyuan_Github_URL, Auto_Commit_Flag = False):
#         print('houliyuan failed, try again\n')
#     else:
#         break



