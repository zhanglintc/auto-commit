#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
Check https://github.com/zhanglintc and get the day's contributions,
if everything goes right, send a mail to foxmail and exit with code 0.
Otherwise exit with code 100.

Exit code:
0  : success
100: fail

                   _ooOoo_ 
                  o8888888o 
                  88" . "88 
                  (| -_- |) 
                  O\  =  /O 
               ____/`---'\____ 
             .'  \\|     |//  `. 
            /  \\|||  :  |||//  \ 
           /  _||||| -:- |||||-  \ 
           |   | \\\  -  /// |   | 
           | \_|  ''\---/''  |   | 
           \  .-\__  `-`  ___/-. / 
         ___`. .'  /--.--\  `. . __ 
      ."" '<  `.___\_<|>_/___.'  >'"". 
     | | :  `- \`.;`\ _ /`;.`/ - ` : | | 
     \  \ `-.   \_ __\ /__ _/   .-` /  / 
======`-.____`-.___\_____/___.-`____.-'====== 
                   `=---=' 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
         佛祖保佑    iii    永无BUG
"""

from selenium import webdriver

import os, sys, urllib
import datetime, time
import subprocess
import platform
import re

import python_send

import warnings
warnings.filterwarnings("ignore")

PASSWORD = None

# try to get password in your user folder
try:
    with open(os.path.expanduser('~') + '/.smpass', 'rb') as fr:
        PASSWORD = fr.read().strip()
except:
    pass

# if failed, try to get password in the script's folder
if not PASSWORD:
    try:
        with open(sys.path[0] + '/.smpass', 'rb') as fr:
            PASSWORD = fr.read().strip()
    except:
        pass

# if still failed, use password in the script
if not PASSWORD:
    PASSWORD = "YOURPASSWORD"
else:
    pass

MailType = 'python' # 'sendemail' # 'mutt'
SENDFROM = "aliserv@163.com"
USERNAME = "aliserv@163.com"
SMTPSERV = "smtp.163.com"

GITHUB_URL = "https://github.com/zhanglintc?period=daily"

MailList = [
    "zhanglintc623@foxmail.com",
]

TODAY = str(datetime.date.today()) # something like: 2014-11-10
CUR_TIME = (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')) # 2014-11-10 15:12:40
LOG_FILE = (datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')) + '.log' # 20141110_151240.log

def make_commands(send_content):
    send_commands = []

    for mailto in MailList:
        if MailType == 'sendemail':
            send_commands.append(
                'sendEmail -f {0} -t {1} -s {2} -xu {3} -xp {4} -u "GitHub Report" -m "{5}"'.format(
                    SENDFROM, # 0
                    mailto,   # 1
                    SMTPSERV, # 2
                    USERNAME, # 3
                    PASSWORD, # 4
                    send_content, # 5
                    )
                )

        elif MailType == 'mutt':
            send_commands.append('echo "{0}" | mutt -s "GitHub Report" {1}'.format(send_content, mailto))

        elif MailType == 'python':
            send_commands = send_content

        else:
            pass

    return send_commands


def auto_commit(streak_detail):
    """
    make an auto-commit to GitHub

    return send_commands: a list of commands
    """

    cd_command = "cd {} &&".format(sys.path[0])

    os.system('{} git pull'.format(cd_command))
    os.system('{} date >> auto_commit_file'.format(cd_command))
    os.system('{} git add auto_commit_file'.format(cd_command))
    os.system('{} git commit -m "{} auto commit"'.format(cd_command, CUR_TIME))
    os.system('{} git push'.format(cd_command))

    send_content = "You have not made any contribution today\nso we did a auto-commit for you\n\n{0}\n{1}\n\n#GitHub reminder#".format(
        streak_detail,
        GITHUB_URL,
    )
    send_commands = make_commands(send_content)

    return send_commands

def github_reminder(MailList = MailList, GITHUB_URL = GITHUB_URL, Auto_Commit_Flag = True):
    reload(sys)
    sys.setdefaultencoding('utf8')

    content = ""
    count = -1

    driver = webdriver.PhantomJS()
    driver.get(GITHUB_URL)
    content = driver.page_source
    driver.close()

    mc = re.search('data-count="(\d)".*{0}'.format(TODAY), content)
    if mc:
        count = mc.group(1)

    fw = open(LOG_FILE, 'wb')
    fw.write(content)
    fw.close()

    send_content = "You have made {0} {1} until now\n{2}\n\n\n{3}\n\n#GitHub reminder#\n".format(
        count,
        "contribution" if int(count) < 2 else "contributions",
        CUR_TIME,
        GITHUB_URL,
    )
    send_commands = make_commands(send_content)

    ##########################################
    # if localtime is between 23:00 and 24:00 but still no commit
    # do automatically commit function

    if time.localtime().tm_hour == 23 and int(count) == 0 and Auto_Commit_Flag:
        send_content = send_commands = auto_commit(streak_detail)

    urllib.urlopen("http://zhanglintc.work:8000/send?text={0}".format(urllib.quote(send_content)))
    ##########################################

    # if don't want to see log file, use the code next line
    # if want to see log file, then comment the code below
    os.remove(LOG_FILE) # remove log file any way, zhanglin 2014.11.20

    if count != None: # if count is initialized, do command
        print("sending...\n")

        doSend = False # debug use only

        if not MailType == 'python':
            for send_command in send_commands:
                if doSend:
                    # sp = subprocess.Popen(["/bin/bash", "-i", "-c", send_command])
                    # sp.communicate()
                    os.system(send_command)

                print(send_command + '\n')

        else:
            if doSend:
                # sendEmail(to_addr, from_addr, alias, password, smtp_server, subject, contents)
                python_send.sendEmail(
                        to_addr = MailList,
                        from_addr = SENDFROM,
                        alias = "Lane-Aliyun",
                        password = PASSWORD,
                        smtp_server = SMTPSERV,
                        subject = "GitHub Report",
                        content = send_content
                    )

            print(send_content)

        return 0

    else: # else exit as 100
        return 100

if __name__ == '__main__':
    github_reminder()

    try:
        raw_input()
    except:
        pass


