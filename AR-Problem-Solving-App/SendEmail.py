# -*- coding: utf-8 -*-
import smtplib

sender = "blogyfolio@gmail.com"
reciever = "mariemmoalla@outlook.com"
password = "blogyfolio2021"


def send_help(message):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sender,password)
    print("login success")
    server.sendmail(sender,reciever,message)
    print("message sent!")
    server.quit()