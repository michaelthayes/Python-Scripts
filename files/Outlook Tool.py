# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 16:39:59 2021

@author: Mike
"""
#   https://stackoverflow.com/questions/26322255/parsing-outlook-msg-files-with-python



-- WIP
#  Use this to search attachments

import win32com.client
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
msg = outlook.OpenSharedItem(r"C:\test_msg.msg")

print msg.SenderName
print msg.SenderEmailAddress
print msg.SentOn
print msg.To
print msg.CC
print msg.BCC
print msg.Subject
print msg.Body

count_attachments = msg.Attachments.Count
if count_attachments > 0:
    for item in range(count_attachments):
        print msg.Attachments.Item(item + 1).Filename

del outlook, msg


#  need to run 
#  pip install extract-msg
#  pip install imapclient


import extract_msg

f = r'MS_Outlook_file.msg'  # Replace with yours
msg = extract_msg.Message(f)
msg_sender = msg.sender
msg_date = msg.date
msg_subj = msg.subject
msg_message = msg.body

print('Sender: {}'.format(msg_sender))
print('Sent On: {}'.format(msg_date))
print('Subject: {}'.format(msg_subj))
print('Body: {}'.format(msg_message))