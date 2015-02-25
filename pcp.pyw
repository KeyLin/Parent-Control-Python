#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import smtplib
import urllib2
import json
import ConfigParser  
from email.mime.text import MIMEText 
  
def send_mail(mail_host,mail_sender,mail_pass,mail_postfix,mail_receivers,sub,content):  
    sender="notify"+"<"+mail_sender+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')  
    msg['Subject'] = sub  
    msg['From'] = sender  
    msg['To'] = ";".join(mail_receivers)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_sender, mail_pass)  
        server.sendmail(sender, mail_receivers, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        #print str(e)  
        return False

def send_sms(sender,passwd,receivers,message):
    url="http://quanapi.sinaapp.com/fetion.php?u="+sender+"&p="+passwd+"&to="+receivers+"&m="+message
    try:  
        result= json.loads(urllib2.urlopen(url).read())
        if result["result"]==0:
            return True
        else:
            return False  
    except Exception, e:  
        #print str(e)  
        return False


def time_control(timeLimit):
    #判断文件是否存在
    if os.path.exists('.\\timeRecord.txt') == False:
        f = open('.\\timeRecord.txt', 'w')
        f.close
    #读取文本中记录的日期
    f = open('.\\timeRecord.txt', 'r+')
    f_date = f.readline()
    f.close
    #读取系统日期，并与文本日期进行比对,如果不相等，则清空文件，进行当日初始化
    n_date = time.strftime("%d/%m/%Y") + "\n"
    if f_date != n_date:
        f = open('.\\timeRecord.txt', 'r+')
        f.truncate()
        f.close
        f = open('.\\timeRecord.txt', 'r+')
        f.write((n_date))
        run_time = "0"
        f.write(run_time)
        f.close
        #死循环语句，当且仅当运行时间大于等于限制时间时跳出循环
    while True:
        f = open('.\\timeRecord.txt', 'r+')
        f_date = f.readline()
        run_time = f.readline()
        run = int(run_time)
        time.sleep(60)
        if run < timeLimit:
            run = run + 1
            f.truncate()
            f.close
            f = open('.\\timeRecord.txt', 'r+')
            f.write(f_date)
            run_time = str(run)
            f.write(run_time)
            f.close
        else:
            break

    while send_sms(sms_sender,feixin_pass,sms_receivers,"今天的上机时间用完了")==False:
        print ".",
        time.sleep(3)
        pass
    #关机命令       
    cmd = "cmd.exe /k shutdown -s -t 0";
    #执行关机命令
    os.system(cmd)

def main():
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    #根据是否工作日设置限制时间
    if datetime.date.today().weekday() < 5:
        timeLimit = config.get('Time', 'weekdays')
    else:
        timeLimit = config.get('Time', 'weekends')

    message = "XXX在" + time.strftime('%H:%M',time.localtime(time.time())) + "打开了电脑"

    sms_sender = config.get('SMS','sms_sender')
    feixin_pass = config.get('SMS','feixin_pass')
    sms_receivers = config.get('SMS','sms_receivers')
    while send_sms(sms_sender,feixin_pass,sms_receivers,message)==False:
        print ".",
        time.sleep(3)
        pass
    print "Send SMS Successfully"

    mail_sender = config.get('Mail','mail_sender')
    mail_pass = config.get('Mail','mail_pass')
    mail_host = config.get('Mail','mail_host')
    mail_receivers = config.get('Mail','mail_receivers')
    mail_postfix = config.get('Mail','mail_postfix')
    while send_mail(mail_host,mail_sender,mail_pass,mail_postfix,mail_receivers,message,message)==False:
        print ".",
        time.sleep(3)
        pass
    print "Send Mail Successfully"
    
    print "monitoring..."    
    time_control(timeLimit)


if __name__ == '__main__':
    main()
